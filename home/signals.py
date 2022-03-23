
from .models import User,Blog
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from .helper import send_mail_registration,unique_slug_generator
import uuid

#this function run when user created
@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        # Profile.objects.create(user=instance) => if Profile model ma there is user foreign key
        
        email = (instance.email)
        token=str(uuid.uuid4())
        instance.email_verification_token=token
        instance.is_active=True#making staff true which is default false we have set
        instance.save()
        send_mail_registration(email,token)
        print("Email Sent")
        
        
# This function run when user is updated
# '''@receiver(post_save, sender=User)
# def new_booking(sender, instance, **kwargs):
#     if instance.email:
#         email = (instance.email)
#         token=str(uuid.uuid4())
#         send_mail_registration(email,token, fail_silently=False)'''

# This function run when user is updated
@receiver(pre_save, sender=Blog)
def slug_generator(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)





#For generating auth token for Django_restframework
from django.conf import settings#we can also import user from models as custom here
from rest_framework.authtoken.models import Token

#this function run when user created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
    
       Token.objects.create(user=instance)
       instance.is_active=True#making staff true which is default false we have set
       
        
        
        
        
# This function run when user is updated
# '''@receiver(post_save, sender=User)
# def new_booking(sender, instance, **kwargs):
#     if instance.email:
#         email = (instance.email)
#         token=str(uuid.uuid4())
#         send_mail_registration(email,token, fail_silently=False)'''

# This function run when user is updated
@receiver(pre_save, sender=Blog)
def slug_generator(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)