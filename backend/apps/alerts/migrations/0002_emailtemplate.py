# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='【IT资产管理系统】资产告警通知', max_length=200, verbose_name='邮件主题')),
                ('body', models.TextField(default='<h3>资产告警通知</h3>\n<p>您好，以下资产触发了告警：</p>\n<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%">\n<tr><td><b>资产编号</b></td><td>{{asset_number}}</td></tr>\n<tr><td><b>资产名称</b></td><td>{{asset_name}}</td></tr>\n<tr><td><b>资产类型</b></td><td>{{asset_type}}</td></tr>\n<tr><td><b>事件类型</b></td><td>{{event_type}}</td></tr>\n<tr><td><b>详情</b></td><td>{{detail}}</td></tr>\n<tr><td><b>时间</b></td><td>{{datetime}}</td></tr>\n</table>\n<p>请及时处理。此邮件由 IT 资产管理系统自动发送。</p>', verbose_name='邮件正文')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '邮件模板',
                'verbose_name_plural': '邮件模板',
                'db_table': 'alert_email_template',
            },
        ),
    ]
