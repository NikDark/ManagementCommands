import os
import re
import shutil

from django.core.management.base import BaseCommand, CommandError
from wagtail.images.models import Image


class Command(BaseCommand):
    help = 'Add Image from folder that you indicate'

    IMAGE_FORMAT = (
        'jpg',
        'jpeg',
        'webp',
        'png',
        'gif',
    )

    def add_arguments(self,parser):
        parser.add_argument(
            '-f',
            '--folder',
            nargs=1,
            required=True,
            help='Path to the folder with different images',
        )

    def handle(self, *args, **options):
        path_folder = options['folder'][0]
        if not os.path.exists(r'media'):
            os.mkdir(r'media')
        if os.path.exists(path_folder) and os.path.isdir(path_folder):
            files_dir = os.listdir(path_folder)
            images = []
            image_names = []
            for file in files_dir:
                try:
                    format = re.search(r'\.(.*)$', file).group(1)
                except:
                    continue
                if format in self.IMAGE_FORMAT:
                    images.append(path_folder+'/'+file)
                    image_names.append(file)
            for image in images:
                shutil.copy2(image,r'media')
            for name in image_names:
                self.stdout.write(name + '  ---  ' + self.style.SUCCESS('OK'))
                Image.objects.create(file=name,title=name.split('.')[0])
        else:
            self.stdout.write(self.style.ERROR('Not dir or not exists'))
