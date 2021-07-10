from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.dashboard, name="adminMainDashboard"),
    path("masterdashboard/", views.master_dashboard, name="adminMasterDashboard"),
    path("question/all/", views.all_questions, name="adminAllQuestions"),
    path("question/new/", views.add_new_quesion, name="adminAddNewQuestion"),
    path("question/edit/<int:id>/",views.edit_question,name="adminEditQuestion"),
    path("battle/category/", views.battle_category, name="adminBattleCategory"),
    path("battle/", views.battles, name="adminBattles"),
    path("contest/", views.today_contest_stat, name="adminTodayContestStat"),
    path("contest/config/",views.config_contest_questions,name="adminContestConfig"),
    path("contest/config/<uuid:id>/",views.config_contest_questions_seperate,name="adminContestConfigSeperate"),
    path("contest/create/", views.create_contest, name="adminCreateContest"),
    path("contest/old/", views.old_contest_stat, name="adminOldContestStat"),
    path("logout/", views.logout_admin, name="adminLogoutPage"),
]