
from django.db import models
from asset.models import Product
from user.models import UserProfile
from service.models import Service
# Create your models here.

class Workorder(models.Model):

    STATUS_CHOICE=(
        (1,'Approved'),
        (2,'Reject'),
        (3,'Undecided'),
    )
    ORDER_STATUS_CHOICE=(
        (1,'Apply'),
        (2,'ready'),
        (3,'Processing'),
        (4,'Failed'),
        (5,'Finish'),

    )
    title                   =models.CharField(max_length=40)
    applicant               =models.ForeignKey(UserProfile,related_name='applicant')
    product                 =models.ForeignKey(Product)
    assign_to_sa            =models.ForeignKey(UserProfile,default=None,null=True,related_name='assign_to_sa')
    assign_to_test          =models.ForeignKey(UserProfile,default=None,null=True,related_name='assign_to_test')
    assign_to_dev           =models.ForeignKey(UserProfile,default=None,null=True,related_name='assign_to_dev')
    update_reason           =models.TextField(max_length=1000,default=None,null=True)
    reject_reason           = models.TextField(max_length=1000, default=None, null=True)
    # test_manager            =models.ForeignKey(User,related_name='test_manager')
    # sa_manager              =models.ForeignKey(User,related_name='sa_manager')
    # director                =models.ForeignKey(User,related_name='director')
    # dev_manager             =models.ForeignKey(User,related_name='dev_manager')
    service            =models.ForeignKey(Service)
    order_contents          =models.TextField(max_length=1000)
    dba_status              =models.CharField(max_length=20,choices=STATUS_CHOICE,default=3,null=True)
    test_manager_status     =models.IntegerField(choices=STATUS_CHOICE,default=3,null=True)
    dev_manager_status      =models.IntegerField(choices=STATUS_CHOICE,default=3,null=True)
    sa_manager_status       =models.IntegerField(choices=STATUS_CHOICE,default=3,null=True)
    director_status         =models.IntegerField(choices=STATUS_CHOICE,default=3,null=True)
    order_status            =models.IntegerField(choices=ORDER_STATUS_CHOICE,default=1)

    operation_time          =models.DateTimeField()
    apply_time              =models.DateTimeField(auto_now_add=True)
    complete_time           =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table='workorder'
        ordering=['complete_time']


