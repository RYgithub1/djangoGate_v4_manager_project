from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from manager.managers import PersonManager


# モデルのクラスは基本的にmodels.Modelを継承
# class Person(models.Model):
# ログイン用に、AbstractBaseUserを継承
class Person(AbstractBaseUser):
    # PersonManagerの定義
    objects = PersonManager()

    MAN = 0
    WOMAN = 1

    HOKKAIDO = 0
    TOHOKU = 5
    TOKYO = 10
    CHIBA = 11
    KANAGAWA = 12
    SAITAMA = 13
    TOCHIGI = 14
    IBARAGI = 15
    CHUBU = 20
    KANSAI = 25
    CHUGOKU = 30
    SHIKOKU = 35
    KYUSHU = 40
    OKINAWA = 45

    # ======== ログイン認証用に定義追加,ログイン時のusernameカラムの代用 =======
    identifier = models.CharField(max_length=64, unique=True, blank=False)

    # 名前 ->文字列（メモリ管理上、max_lengthの指定必須）
    name = models.CharField(max_length=128)
    # メールアドレス ->メール
    email = models.EmailField()
    # 誕生日 ->時刻
    birthday = models.DateTimeField()
    # 性別 ->整数
    sex = models.IntegerField(editable=False)
    # 出身地
    address_from = models.IntegerField()
    # 現住所
    current_address = models.IntegerField()

    # ======== ログイン認証用に２行追加 ========
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'identifier'


class Manager(models.Model):
    # 部署の定数
    DEP_ACCOUNTING = 0  # 経理
    DEP_SALES = 5  # 営業
    DEP_PRODUCTION = 10  # 製造
    DEP_DEVELOPMENT = 15  # 開発
    DEP_HR = 20  # 人事
    DEP_FIN = 25  # 財務
    DEP_AFFAIRS = 30  # 総務
    DEP_PLANNING = 35  # 企画
    DEP_BUSINESS = 40  # 業務
    DEP_DISTR = 45  # 流通
    DEP_IS = 50  # 情報システム

    # ForeignKey()は1対多関係や、ManyToMany
    # 人 -> 生データでなく外部キー。Managerクラスゆえ、personとmanagerが「1 : 多」（同一人物が違う部署のマネージャーを複数もある得るため）
    # Django2.0からは、ForeignKeyにはon_delete引数が必須ゆえ追記
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    # 部署
    department = models.IntegerField()
    # 着任時期
    joined_at = models.DateTimeField()
    # やめた時期
    quited_at = models.DateTimeField(null=True, blank=True)


class Worker(models.Model):
    # 人
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    # 着任時期
    joined_at = models.DateTimeField()
    # やめた時期
    quited_at = models.DateTimeField(null=True, blank=True)
    # 担当上司
    manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
