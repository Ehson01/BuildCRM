from django.db import models
from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_profile',
        verbose_name='User account'
    )
    full_name = models.CharField(max_length=100, verbose_name='Full name')
    phone = models.CharField(max_length=100, verbose_name='Phone number')
    email = models.EmailField(blank=True, verbose_name='Email address')
    passport_data = models.CharField(max_length=255, blank=True, verbose_name='Passport details')
    address = models.TextField(blank=True, verbose_name='Address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    Status = [
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    lead = models.OneToOneField(
        'leads.Lead',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Lead'
    )
    client = models.ForeignKey('contracts.Client', on_delete=models.PROTECT, related_name='contracts')
    house = models.ForeignKey(
        'projects.HouseType',
        on_delete=models.PROTECT,
        related_name='contracts',
        verbose_name='House project'
    )
    number = models.CharField(max_length=100, unique=True, verbose_name='Contract number')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total amount')
    start_date = models.DateField(auto_now_add=True, verbose_name='Start date')
    end_date = models.DateField(verbose_name='End date')
    status = models.CharField(
        max_length=20,
        choices=Status,
        default='active',
        verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        ordering = ['-created_at']

    def __str__(self):
        return self.client.full_name


class Payment(models.Model):
    method = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank transfer'),
    ]

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Contract'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Payment amount')
    payment_method = models.CharField(
        max_length=20,
        choices=method,
        default='bank',
        verbose_name='Payment method'
    )
    payment_date = models.DateField(default=timezone.localdate, verbose_name='Payment date')
    comment = models.CharField(max_length=255, blank=True, verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date', '-created_at']

    def __str__(self):
        return f'Payment {self.amount} for contract #{self.contract.number}'