import json

from django.conf import settings

from django.core.management import BaseCommand

from authapp.models import ShopUser, ShopUserProfile
from mainapp.models import ProductCategory, Product




class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            users_profile = ShopUserProfile.objects.create(user=user)
            users_profile.save()