from django.core.mail import BadHeaderError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import IsAdminOrAssetManager
from .models import AlertRule, AlertLog, EmailConfig, EmailTemplate
from .serializers import AlertRuleSerializer, AlertLogSerializer, EmailConfigSerializer, EmailTemplateSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer
    filterset_fields = ['is_enabled', 'event_type']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrAssetManager()]
        return []


class AlertLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertLog.objects.select_related('rule', 'asset').all()
    serializer_class = AlertLogSerializer
    filterset_fields = ['is_read', 'rule', 'asset']

    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        log = self.get_object()
        log.is_read = True
        log.save()
        return Response({'detail': '已标记为已读'})

    @action(detail=False, methods=['patch'])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'detail': '全部标记为已读'})


class EmailConfigViewSet(viewsets.GenericViewSet):
    """Email config singleton — get first or create, update."""
    queryset = EmailConfig.objects.all()
    serializer_class = EmailConfigSerializer

    def get_permissions(self):
        return [IsAdminOrAssetManager()]

    def list(self, request):
        config = EmailConfig.get_config()
        if config:
            return Response(EmailConfigSerializer(config).data)
        return Response({})

    def create(self, request):
        config = EmailConfig.get_config()
        if config:
            serializer = EmailConfigSerializer(config, data=request.data)
        else:
            serializer = EmailConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_config(self, request):
        config = EmailConfig.get_config()
        if config:
            serializer = EmailConfigSerializer(config, data=request.data)
        else:
            serializer = EmailConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def test_email(self, request):
        """Send a test email using current config."""
        config = EmailConfig.get_config()
        if not config:
            return Response({'error': '请先保存邮件配置'}, status=status.HTTP_400_BAD_REQUEST)
        if not config.is_enabled:
            return Response({'error': '邮件配置未启用'}, status=status.HTTP_400_BAD_REQUEST)

        recipient = request.data.get('recipient', '')
        if not recipient:
            return Response({'error': '请输入收件人邮箱'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from django.core.mail import get_connection, EmailMessage
            connection = get_connection(
                host=config.smtp_host,
                port=config.smtp_port,
                username=config.username,
                password=config.password,
                use_tls=config.use_tls,
                use_ssl=config.use_ssl,
            )
            email = EmailMessage(
                subject='【IT资产管理系统】测试邮件',
                body='这是一封测试邮件，恭喜您邮件配置成功！',
                from_email=config.sender_email or config.username,
                to=[recipient],
                connection=connection,
            )
            email.send(fail_silently=False)
            return Response({'message': f'测试邮件已发送至 {recipient}'})
        except BadHeaderError:
            return Response({'error': '邮件头信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'邮件发送失败：{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailTemplateViewSet(viewsets.GenericViewSet):
    """Email template singleton — get or update."""
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

    def get_permissions(self):
        return [IsAdminOrAssetManager()]

    def list(self, request):
        template = EmailTemplate.get_template()
        if template:
            return Response(EmailTemplateSerializer(template).data)
        return Response({})

    def create(self, request):
        template = EmailTemplate.get_template()
        if template:
            serializer = EmailTemplateSerializer(template, data=request.data)
        else:
            serializer = EmailTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
