"""
Add 多媒体 (Multimedia) as a top-level asset category.
Safe to run on existing databases — skips already-existing categories.
"""
from django.core.management.base import BaseCommand
from base_data.models import AssetCategory


MULTIMEDIA_SUBCATEGORIES = [
    ('投影仪', 'mm_projector', 1),
    ('音响设备', 'mm_audio', 2),
    ('摄像头', 'mm_camera', 3),
    ('会议设备', 'mm_conference', 4),
    ('显示设备', 'mm_display', 5),
]


class Command(BaseCommand):
    help = 'Add 多媒体 as a Level-1 asset category (idempotent)'

    def handle(self, *args, **options):
        multimedia, created = AssetCategory.objects.get_or_create(
            code='multimedia',
            defaults={'name': '多媒体', 'sort_order': 4}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created 多媒体 top-level category.'))
        else:
            # Fix name/sort_order in case of partial data
            if multimedia.name != '多媒体':
                multimedia.name = '多媒体'
                multimedia.save(update_fields=['name'])
            self.stdout.write('多媒体 top-level category already exists.')

        for name, code, sort_order in MULTIMEDIA_SUBCATEGORIES:
            child, child_created = AssetCategory.objects.get_or_create(
                code=code,
                defaults={'name': name, 'parent': multimedia, 'sort_order': sort_order}
            )
            if child_created:
                self.stdout.write(f'  + Created subcategory: {name}')
            else:
                # Ensure it's under the multimedia parent
                if child.parent_id != multimedia.pk:
                    child.parent = multimedia
                    child.save(update_fields=['parent'])
                    self.stdout.write(f'  ~ Moved {name} under 多媒体')

        # Rebuild MPTT tree to keep hierarchy intact
        AssetCategory.objects.rebuild()
        self.stdout.write(self.style.SUCCESS('Done. 多媒体 category tree is ready.'))
