import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from datahandler.managers import CustomUserManager
from django.utils.translation import ugettext_lazy

from datahandler.choices import DIFFICULTY_LEVEL, CATEGORY_POINTS_CREDITED, CONTEST_DIFFICULTY_LEVEL


# List of all class
class SchoolClass(models.Model):
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title


# List of all subjects
class SchoolSubject(models.Model):
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title


# Question & Answer Brunch Mainly For Battle Purpose
class QuestionBrunch(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    question = models.TextField(null=True)
    option1 = models.TextField(null=True)
    option2 = models.TextField(null=True)
    option3 = models.TextField(null=True)
    option4 = models.TextField(null=True)
    correct_answer_option = models.IntegerField(null=True, default=-1) # Note that it is option , not index , start from 1
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL, null=True, default="easy")
    points = models.IntegerField(null=True, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

# This is the main customuser models which will use django for user auth
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, editable=False)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    is_normalUser = models.BooleanField(null=True, default=True)
    is_normalAdmin = models.BooleanField(null=True, default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)


# Extended Profile For NormalUser
class UserExtendedProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_base_profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    present_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    is_premium_user = models.BooleanField(null=True, default=False)
    total_points = models.IntegerField(null=True, default=0)
    score_contest = models.FloatField(null=True,default=0)
    profileimage = models.TextField(null=True,default="default/profileavatar.jpg")

    def __str__(self):
        return self.user_base_profile.username


# Transaction log for points buy
class TransactionLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE)
    coins_to_be_deposited = models.IntegerField(null=True,default=0)
    price = models.IntegerField(null=True, default=0)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False, null=True)
    ordered_on = models.DateTimeField(auto_now_add=True)
    verified_on = models.DateTimeField(auto_now=True)

    # Status false means transaction failed else Successful

    def __str__(self):
        return self.transaction_id


# Referral Logs for referral bonus
class ReferralLogs(models.Model):
    referred_by_user = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE, related_name="referred_by_user")
    referred_to_user = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE, related_name="referred_to_user")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.referred_by_user.user_base_profile.username} To {self.referred_to_user.user_base_profile.username}"


# Reset Password Database
class ResetPasswordDB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE)
    key = models.TextField(null=True)
    is_used = models.BooleanField(null=True, default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# Model for battle category
class BattleCategory(models.Model):
    title = models.TextField(null=True)
    # Whether everyone will get unlimited time to solve or not
    time_bound = models.BooleanField(null=True)
    # If time_bound is true then need to provide max_time , max_time will be in seconds
    max_time = models.BigIntegerField(null=True)
    no_of_questions = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.title


# Model For Battle | Hold all configuration
class Battle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_points = models.IntegerField(null=True, default=0)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_LEVEL, null=True)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    is_active = models.BooleanField(null=True, default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# Battle History
class BattleHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE, related_name="user2")
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    questions = models.TextField(null=True,
                                 default="[]")  # List of ID's of questions that has been chosed randomly at the time
    user1_answers = models.TextField(null=True,default="[]")
    user2_answers = models.TextField(null=True,default= "[]")
    winner_user_id = models.TextField(null=True,default="")
    is_running = models.BooleanField(null=True,default=True)
    created_on = models.DateTimeField(auto_now_add=True)


# Contest
class Contest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(null=True)
    point_to_deduct = models.IntegerField(null=True,default=0)
    max_point = models.IntegerField(null=True, default=0)
    valid_till = models.DateTimeField(null=True)
    starting_from = models.DateTimeField(null=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20,choices=CONTEST_DIFFICULTY_LEVEL,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# Question Answer Model For Contest
class QuestionAnswerForContest(models.Model):
    question = models.TextField(null=True)
    option1 = models.TextField(null=True)
    option2 = models.TextField(null=True)
    option3 = models.TextField(null=True)
    option4 = models.TextField(null=True)
    correct_answer_option = models.IntegerField(null=True, default=-1)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)


# History of user participating in contest
class ContestHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    points = models.IntegerField(null=True,default=0)
    answers = models.TextField(null=True,default="[]")
    result_answers = models.TextField(null=True,default="[]")
    percentage_of_correct_answers = models.FloatField(null=True,default=0.0)
    is_running = models.BooleanField(null=True,default=True)
    is_evaluated = models.BooleanField(null=True, default=False)
    created_on = models.DateTimeField(auto_now_add=True)


# Points Log Model For Only Depositing Coin by battle or contest [Has ForeignKey relation]
class PointsDepositByBattleContest(models.Model):
    points = models.IntegerField(null=True, default=0)  # We expect only positive values
    category = models.CharField(max_length=20, choices=CATEGORY_POINTS_CREDITED, null=True)
    contest = models.ForeignKey(ContestHistory, on_delete=models.CASCADE, null=True, blank=True)
    battle = models.ForeignKey(BattleHistory, on_delete=models.CASCADE, null=True, blank=True)


# Points log It will log all type of buy/sell in coins . [ It will only connect to userprofile through foreignkey &
# the else part will be in string ]
class PointsLog(models.Model):
    user = models.ForeignKey(UserExtendedProfile, on_delete=models.CASCADE)
    points = models.IntegerField(null=True, default=0)  # Points can be in negative and positive
    description = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)


# This model to define the coin purchase packs
class CoinPackages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coins = models.IntegerField(null=True,default=0)
    price = models.IntegerField(null=True,default=0)
    created_on = models.DateTimeField(auto_now_add=True)
