from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from encrypted_model_fields.fields import EncryptedCharField, encrypt_str
from django.contrib.postgres.fields import JSONField
from enum import IntEnum


class BlockchainState(IntEnum):
    PENDING = 0
    STARTED = 1
    COMPLETED = 2
    ERROR = 3


class User(AbstractUser):
    pass


# Create your models here.
class Project(models.Model):
    repo_name = models.CharField(max_length=40)
    dao_address = models.CharField(max_length=42, unique=True)
    merge_module_address = models.CharField(max_length=42)
    last_merge_event_block = models.PositiveIntegerField(default=0)
    is_mycro_dao = models.BooleanField(default=False)
    symbol = models.CharField(max_length=10, default=None, blank=False,
                              null=True)
    decimals = models.IntegerField(default=-1)
    blockchain_state = models.IntegerField(
        choices=[(state.value, state.name) for state in BlockchainState],
        default=BlockchainState.PENDING.value
    )
    # TODO disable updates to this field
    initial_balances = JSONField(null=False, blank=False)


    # TODO use django managers
    @staticmethod
    def get_mycro_dao():
        try:
            return Project.objects.get(is_mycro_dao=True)
        except:
            return None

    @staticmethod
    def create_mycro_dao(address, symbol, decimals):
        Project.objects.filter().update(is_mycro_dao=False)
        return Project.objects.create(
            repo_name='mycro',
            dao_address=address,
            is_mycro_dao=True,
            symbol=symbol,
            decimals=decimals,
            blockchain_state=BlockchainState.COMPLETED,
            initial_balances={})

    def __str__(self):
        return f'{self.repo_name}@{self.dao_address}'

    def __repr(self):
        return self.__str__()


class ASC(models.Model):
    address = models.CharField(max_length=42, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rewardee = models.CharField(max_length=42)
    reward = models.IntegerField()
    pr_id = models.IntegerField(null=True, blank=True)
    blockchain_state = models.IntegerField(
        choices=[(state.value, state.name) for state in BlockchainState],
        default=BlockchainState.PENDING.value
    )


class Wallet(models.Model):
    """
    NOTE!! Since private_key is encrypted no filtering of any sort works on it
    If you need to query for specific wallets, use their address for the query
    """
    private_key = EncryptedCharField(max_length=66, unique=True, blank=False,
                                     null=False)
    address = models.CharField(max_length=42, unique=True, blank=False,
                               null=False)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    hash = models.CharField(max_length=66, unique=True)
    value = models.IntegerField()
    chain_id = models.IntegerField(blank=True, null=True)
    nonce = models.IntegerField()
    gas_limit = models.IntegerField()
    gas_price = models.IntegerField()
    data = models.TextField()
    to = models.TextField()
    block_number = models.IntegerField()
    contract_address = models.CharField(max_length=44, unique=True, null=True, blank=True)
    cumulative_gas_used = models.IntegerField()
    gas_used = models.IntegerField()
    status = models.IntegerField()
