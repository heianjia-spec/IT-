from django.db import models
from django.conf import settings


class AlertRule(models.Model):
    EVENT_CHOICES = [
        ('asset_created', '资产新增'),
        ('status_changed', '资产异动'),
        ('warranty_expiry', '维保到期'),
        ('license_expiry', '许可证到期'),
        ('low_stock', '低库存'),
    ]
    name = models.CharField('规则名称', max_length=100)
    event_type = models.CharField('事件类型', max_length=30, choices=EVENT_CHOICES)
    is_enabled = models.BooleanField('是否启用', default=True)
    notify_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True,
        verbose_name='通知用户'
    )
    notify_email = models.BooleanField('邮件通知', default=False)
    notify_system = models.BooleanField('系统通知', default=True)
    description = models.TextField('描述', blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'alert_rule'
        verbose_name = '告警规则'
        verbose_name_plural = '告警规则'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {'[启用]' if self.is_enabled else '[禁用]'}"


class AlertLog(models.Model):
    rule = models.ForeignKey(
        AlertRule, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='logs',
        verbose_name='告警规则'
    )
    asset = models.ForeignKey(
        'assets.Asset', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='alert_logs',
        verbose_name='关联资产'
    )
    title = models.CharField('标题', max_length=200)
    message = models.TextField('消息内容')
    is_read = models.BooleanField('是否已读', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'alert_log'
        verbose_name = '告警日志'
        verbose_name_plural = '告警日志'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EmailConfig(models.Model):
    """Email server configuration (singleton)."""
    smtp_host = models.CharField('SMTP服务器', max_length=100)
    smtp_port = models.IntegerField('端口', default=587)
    username = models.CharField('用户名', max_length=100)
    password = models.CharField('密码', max_length=100)
    use_tls = models.BooleanField('使用TLS', default=False)
    use_ssl = models.BooleanField('使用SSL', default=True)
    sender_email = models.CharField('发件人邮箱', max_length=100, blank=True, default='')
    is_enabled = models.BooleanField('是否启用', default=False)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'alert_email_config'
        verbose_name = '邮件配置'
        verbose_name_plural = '邮件配置'

    def __str__(self):
        return f"邮件配置 {'[启用]' if self.is_enabled else '[禁用]'}"

    @classmethod
    def get_config(cls):
        return cls.objects.first()


class EmailTemplate(models.Model):
    """Email alert template (singleton). Supports variables:
    {{asset_number}}, {{asset_name}}, {{asset_type}}, {{event_type}},
    {{status}}, {{department}}, {{responsible_person}}, {{detail}}, {{datetime}}
    """
    subject = models.CharField('邮件主题', max_length=200, default='【IT资产管理系统】资产告警通知')
    body = models.TextField('邮件正文', default='''<h3>资产告警通知</h3>
<p>您好，以下资产触发了告警：</p>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%">
<tr><td><b>资产编号</b></td><td>{{asset_number}}</td></tr>
<tr><td><b>资产名称</b></td><td>{{asset_name}}</td></tr>
<tr><td><b>资产类型</b></td><td>{{asset_type}}</td></tr>
<tr><td><b>事件类型</b></td><td>{{event_type}}</td></tr>
<tr><td><b>详情</b></td><td>{{detail}}</td></tr>
<tr><td><b>时间</b></td><td>{{datetime}}</td></tr>
</table>
<p>请及时处理。此邮件由 IT 资产管理系统自动发送。</p>''')
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'alert_email_template'
        verbose_name = '邮件模板'
        verbose_name_plural = '邮件模板'

    def __str__(self):
        return self.subject

    @classmethod
    def get_template(cls):
        return cls.objects.first()

    def render(self, **kwargs):
        """Render subject and body with given variables."""
        subject = self.subject
        body = self.body
        for key, value in kwargs.items():
            placeholder = '{{%s}}' % key
            subject = subject.replace(placeholder, str(value or ''))
            body = body.replace(placeholder, str(value or ''))
        return subject, body
