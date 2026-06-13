from rest_framework import serializers
from .models import AlertRule, AlertLog, EmailConfig, EmailTemplate


class AlertRuleSerializer(serializers.ModelSerializer):
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)

    class Meta:
        model = AlertRule
        fields = [
            'id', 'name', 'event_type', 'event_type_display',
            'is_enabled', 'notify_users', 'notify_email', 'notify_system',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AlertLogSerializer(serializers.ModelSerializer):
    rule_name = serializers.CharField(source='rule.name', read_only=True, default=None)
    asset_name = serializers.CharField(source='asset.name', read_only=True, default=None)
    asset_number = serializers.CharField(source='asset.asset_number', read_only=True, default=None)

    class Meta:
        model = AlertLog
        fields = [
            'id', 'rule', 'rule_name', 'asset', 'asset_name', 'asset_number',
            'title', 'message', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EmailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfig
        fields = [
            'id', 'smtp_host', 'smtp_port', 'username', 'password',
            'use_tls', 'use_ssl', 'sender_email', 'is_enabled', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'subject', 'body', 'updated_at']
        read_only_fields = ['id', 'updated_at']
