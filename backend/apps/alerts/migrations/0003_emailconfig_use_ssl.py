# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0002_emailtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailconfig',
            name='use_ssl',
            field=models.BooleanField(default=True, verbose_name='使用SSL'),
        ),
        migrations.AlterField(
            model_name='emailconfig',
            name='use_tls',
            field=models.BooleanField(default=False, verbose_name='使用TLS'),
        ),
    ]
