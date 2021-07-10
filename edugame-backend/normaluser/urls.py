from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.homePage,name="normalUserHomepage"),
    path("login/",views.LoginPage,name="normalUserLoginPage"),
    path("register/",views.RegisterPage,name="normalUserRegisterPage"),
    path("logoutUser/",views.logoutUser,name="normalUserLogout"),
    path('resetpass/',views.ResetPass),
    path('resetlink/<uuid:id>/',views.ResetPassVerify),
    path("battle/selectsubject/",views.chooseSubjectForBattle,name="normalUserChooseSubjectForBattle"),
    path('battle/category/<int:subject_id>/',views.chooseBattleCategoryPage,name="normalUserBattleCategory"),
    path('battle/start/<uuid:id>/',views.startWelcomeBattle,name="normalUserStartBattle"),
    path("battle/result/<uuid:id>/", views.battle_result,name="normalUserBattleresult"),
    path("contest/list/",views.contest_list,name="normalUserContestsList"),
    path("contest/welcome/<uuid:id>/",views.contest_welcome_page,name="normalUserContestWelcome"),
    path("contest/start/<uuid:id>/",views.contest_middleware_page,name="normalUserContestMiddleware"),
    path("contest/play/<uuid:id>/", views.contest_playing_page, name="normalUserContestPlaying"),
    path('contest/submit/<uuid:id>/',views.contestSumissionApi),
    path('contest/result/<uuid:id>/',views.contest_result,name="normalUserContestResult"),
    path('recharge/',views.coin_pack_list,name="normalUserRechargeWallet"),
    path('payment/',views.coin_recharge,name="normalUserCoinPaymentPage"),
    path('verfiypayment/',views.verfiypayment),
    path('profile/',views.profileDetails,name="normalUserProfile"),
    path('wallet/',views.profileWallet,name="normalUserWallet"),
    path('profile/settings/',views.profileSettings,name="normalUserProfileSettings"),
    path('profile/stats/',views.profileStats,name="normalUserProfileStats"),
    path('leaderboard/',views.leaderboard,name="normalUserLeaderboard")

]