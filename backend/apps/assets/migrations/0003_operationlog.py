# Generated manually
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_alter_asset_asset_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('create', '新增资产'), ('update', '编辑资产'), ('delete', '删除资产'), ('batch_delete', '批量删除'), ('import', '导入资产'), ('export', '导出资产')], db_index=True, max_length=20, verbose_name='操作类型')),
                ('asset_count', models.IntegerField(default=0, verbose_name='资产数量')),
                ('detail', models.TextField(blank=True, default='', verbose_name='操作详情')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='操作时间')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_logs', to='assets.asset', verbose_name='关联资产')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_logs', to=settings.AUTH_USER_MODEL, verbose_name='操作人')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
                'db_table': 'asset_operation_log',
                'ordering': ['-created_at'],
            },
        ),
    ]
