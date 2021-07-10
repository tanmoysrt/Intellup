from django.urls import path

from api import views

urlpatterns = [
    path("",views.test),
    path("questions/<int:no_of_questions>/<int:class_id>/<int:subject_id>/",views.get_random_questions),
    path("battle/register/",views.register_battle_history),
    path("battle/update/", views.battle_update),
    path("battle/<uuid:id>/",views.battle_category_details),
    path("userdetails/",views.getProifleInfo)
]