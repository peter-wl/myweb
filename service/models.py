from django.db import models
from user.models import UserProfile
from asset.models import Server
# Create your models here.

class Service(models.Model):
    SCRIPT_CHOICE       = (
        (1,'java_core_restart.sh'),
        (2,'tomcat_restart.sh'),
        (3,'nginx_restart.sh'),
        (4,'php_restart.sh'),
        (5,'fastdfs_restart.sh'),
        (6,'redis_restart.sh'),
    )
    service_name        = models.CharField(max_length=30,null=True,unique=True)
    short_name          = models.CharField(max_length=10,null=True,unique=True)
    dev_name            = models.ForeignKey(UserProfile,null=True)
    script              = models.IntegerField(choices=SCRIPT_CHOICE,null=True)

class ServiceModels(models.Model):
    model_base_path     = models.CharField(max_length=30,null=True)
    model_data_path     = models.CharField(max_length=30,null=True)
    model_restart_script= models.CharField(max_length=30,null=True)
    model_server_ip     = models.ForeignKey(Server,null=True)
    model_service       = models.ForeignKey(Service,null=True)


