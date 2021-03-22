from django.db import models


# Create your models here.
class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='User ID', unique=True,)
    name = models.TextField(verbose_name='Username',)

    def __str__(self):
        return f'@{self.name}'

    class Meta:
        verbose_name = 'Profile'


class Message(models.Model):
    profile = models.ForeignKey(to='bottest.Profile', verbose_name='Profile', on_delete=models.PROTECT,)
    text = models.TextField(verbose_name='Text',)
    created_at = models.DateTimeField(verbose_name='Time', auto_now_add=True,)

    def __str__(self):
        return f'Message{self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Message'