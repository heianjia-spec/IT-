"""
Seed data management command.
Creates default admin user, asset categories, sample departments, locations, and suppliers.
Idempotent — safe to run multiple times.
"""
from django.core.management.base import BaseCommand
from base_data.models import AssetCategory, Department, Location, Supplier
from accounts.models import User


class Command(BaseCommand):
    help = 'Initialize seed data (idempotent)'

    def handle(self, *args, **options):
        self._create_admin()
        self._create_categories()
        self._create_departments()
        self._create_locations()
        self._create_suppliers()
        self.stdout.write(self.style.SUCCESS('Seed data initialized successfully.'))

    @staticmethod
    def _create_admin():
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@example.com',
                role='admin',
                phone='13800000000'
            )
            print('Created default admin user: admin / admin123')

    @staticmethod
    def _create_categories():
        if AssetCategory.objects.exists():
            return

        # Level 1
        hardware = AssetCategory.objects.create(name='硬件', code='hardware', sort_order=1)
        software = AssetCategory.objects.create(name='软件', code='software', sort_order=2)
        consumable = AssetCategory.objects.create(name='IT耗材', code='consumable', sort_order=3)

        # Level 2 under 硬件
        AssetCategory.objects.create(name='服务器', code='hw_server', parent=hardware, sort_order=1)
        AssetCategory.objects.create(name='PC', code='hw_pc', parent=hardware, sort_order=2)
        AssetCategory.objects.create(name='打印机', code='hw_printer', parent=hardware, sort_order=3)
        net_dev = AssetCategory.objects.create(name='网络设备', code='hw_network', parent=hardware, sort_order=4)

        # Level 3 under 网络设备
        AssetCategory.objects.create(name='路由器', code='hw_router', parent=net_dev, sort_order=1)
        AssetCategory.objects.create(name='交换机', code='hw_switch', parent=net_dev, sort_order=2)
        AssetCategory.objects.create(name='防火墙', code='hw_firewall', parent=net_dev, sort_order=3)
        AssetCategory.objects.create(name='无线控制器', code='hw_wlc', parent=net_dev, sort_order=4)

        print('Created asset categories.')

    @staticmethod
    def _create_departments():
        if Department.objects.exists():
            return

        tech = Department.objects.create(name='技术部', code='tech', sort_order=1)
        finance = Department.objects.create(name='财务部', code='finance', sort_order=2)
        hr = Department.objects.create(name='人事部', code='hr', sort_order=3)
        admin_dept = Department.objects.create(name='行政部', code='admin', sort_order=4)

        Department.objects.create(name='运维组', code='tech_ops', parent=tech, sort_order=1)
        Department.objects.create(name='研发组', code='tech_dev', parent=tech, sort_order=2)

        print('Created departments.')

    @staticmethod
    def _create_locations():
        if Location.objects.exists():
            return

        Location.objects.create(name='A1机房', code='room_a1', location_type='server_room',
                                address='A栋1楼数据中心')
        Location.objects.create(name='B2机房', code='room_b2', location_type='server_room',
                                address='B栋2楼数据中心')
        Location.objects.create(name='主库房', code='wh_main', location_type='warehouse',
                                address='A栋B1层')
        Location.objects.create(name='备件库', code='wh_spare', location_type='warehouse',
                                address='B栋1层')

        print('Created locations.')

    @staticmethod
    def _create_suppliers():
        if Supplier.objects.exists():
            return

        Supplier.objects.create(name='联想（北京）有限公司', code='lenovo',
                                contact_person='张经理', contact_phone='010-58868888')
        Supplier.objects.create(name='戴尔（中国）有限公司', code='dell',
                                contact_person='李经理', contact_phone='0592-8188000')
        Supplier.objects.create(name='惠普贸易（上海）有限公司', code='hp',
                                contact_person='王经理', contact_phone='021-38508888')
        Supplier.objects.create(name='北京京东世纪贸易有限公司', code='jd',
                                contact_person='赵经理', contact_phone='400-606-5500')

        print('Created suppliers.')
