from django.db import models

# Create your models here.


class Product(models.Model):
    name                =models.CharField(max_length=20,null=True,unique=True)
    short_name          =models.CharField(max_length=10,null=True)
    def __str__(self):
        return "{}".format(self.name)
    class Meta:
        db_table='product'

class Idc(models.Model):
    name                =models.CharField(max_length=128,unique=True)
    short_name          =models.CharField(max_length=10,unique=True)
    address             =models.CharField(max_length=255)
    contact_user        =models.CharField(max_length=50)
    user_phone          =models.CharField(max_length=50)
    user_email          =models.EmailField(unique=True)
    update_time         =models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return "{} {}".format(self.name, self.short_name)
    class Meta:
        db_table='idc'


class Server(models.Model):
    STATUS_CHOICE=(
        ('1','ONLINE'),
        ('2','OFFLINE'),
        ('3','FAILURE'),
    )
    supplier            = models.IntegerField(null=True)
    manufacturers       = models.CharField(max_length=50, null=True)
    manufacture_date    = models.DateField(null=True)
    server_type         = models.CharField(max_length=20, null=True)
    sn                  = models.CharField(max_length=60, db_index=True, null=True)
    idc                 = models.ForeignKey(Idc, null=True)
    os                  = models.CharField(max_length=50, null=True)
    hostname            = models.CharField(max_length=50, unique=True, null=True)
    inner_ip            = models.CharField(max_length=32, null=True, unique=True)
    mac_address         = models.CharField(max_length=50, null=True)
    ip_info             = models.CharField(max_length=255, null=True)
    server_cpu          = models.CharField(max_length=250, null=True)
    server_disk         = models.CharField(max_length=100, null=True)
    server_mem          = models.CharField(max_length=100, null=True)
    status              = models.CharField(max_length=100,db_index=True, null=True)
    remark              = models.TextField(null=True)
    #service_id         = models.IntegerField(db_index=True, null=True)
    product             = models.ForeignKey(Product,null=True)
    status              = models.CharField(choices=STATUS_CHOICE,null=True,max_length=20)
    check_update_time   = models.DateTimeField(auto_now=True,null=True)
    vm_status           = models.IntegerField(db_index=True, null=True)
    uuid                = models.CharField(max_length=100, db_index=True,null=True)
    def __str__(self):
        return "{} {}".format(self.hostname, self.inner_ip)

    class Meta:
        db_table = "server"