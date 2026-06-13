from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('asset_manager', '资产管理员'),
        ('user', '普通用户'),
        ('viewer', '只读用户'),
    ]

    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField('手机号', max_length=20, blank=True, default='')
    department = models.ForeignKey(
        'base_data.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users',
        verbose_name='所属部门'
    )

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
