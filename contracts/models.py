from django.db import models
from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_profile',
        verbose_name='Аккаунт пользователя'
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    passport_data = models.CharField(max_length=255, blank=True, verbose_name='Паспорт')
    address = models.TextField(blank=True, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    Status = [
        ('active', 'active'),
        ('paid', 'paid'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    ]

    lead = models.OneToOneField('leads.Lead', on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='contracts')
    house = models.ForeignKey('houses.House', on_delete=models.PROTECT, related_name='contracts')
    number = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status, default='active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        ordering = ['-created_at']

    def __str__(self):
        return self.client.full_name


class Payment(models.Model):
    method = [
        ('cash', 'cash'),
        ('card', 'card'),
        ('bank', 'bank'),
    ]

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Договор'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=method, default='bank')
    payment_date = models.DateField(default=timezone.localdate)
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date', '-created_at']

    def __str__(self):
        return f'Платёж {self.amount} по договору №{self.contract.number}'