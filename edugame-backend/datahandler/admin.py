from django.contrib import admin
from django.contrib.auth.models import Group
from datahandler.models import *

admin.site.unregister(Group)
admin.site.register(CustomUser)
admin.site.register(UserExtendedProfile)
admin.site.register(TransactionLogs)
admin.site.register(ReferralLogs)
admin.site.register(ResetPasswordDB)
admin.site.register(SchoolClass)
admin.site.register(SchoolSubject)
admin.site.register(QuestionBrunch)
admin.site.register(Battle)
admin.site.register(BattleCategory)
admin.site.register(BattleHistory)
admin.site.register(Contest)
admin.site.register(QuestionAnswerForContest)
admin.site.register(ContestHistory)
admin.site.register(PointsLog)
admin.site.register(PointsDepositByBattleContest)
admin.site.register(CoinPackages)
