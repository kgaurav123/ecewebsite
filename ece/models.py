from django.db import models
from datetime import date,time
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.core.exceptions import ValidationError


def validate_image_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')


class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

	yr_choices = [
        (1,'First Year'),
        (2,'Second Year'),
        (3,'Third Year'),
        (4,'Final Year'),
    ]


	
	image=models.ImageField(default='default.jpg', upload_to='profile_pics')
	year=models.IntegerField(choices=yr_choices, default=1)
	email=models.EmailField(null=True,blank=True)
	fb=models.URLField(null=True,blank=True)
	phone=models.CharField(max_length=15,null=True,blank=True)
	linkedIn=models.URLField(null=True,blank=True)


	def __str__(self):
		return (self.user.first_name+" "+self.user.last_name)


@receiver(post_save,sender=User)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Notice(models.Model):
	heading=models.CharField(max_length=100,null=True,blank=True)
	text=models.TextField(null=True,blank=True)
	notice_date=models.DateField(null=True)

	def __str__(self):
		return(str(self.heading))
