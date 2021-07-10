import random, json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from datahandler.models import *


@csrf_exempt
def test(request):
    return HttpResponse("Server Online")


def get_random_questions(request, no_of_questions,class_id,subject_id):
    questions = QuestionBrunch.objects.all().filter(school_subject_id=subject_id,school_class_id=class_id).order_by('?')[0:no_of_questions]
    data_to_be_sent = {}
    question_ids = []
    correct_answer_options = []  # Note that it is option , not index , start from 1
    question_answer_set = {}
    for i in questions:
        question_ids.append(i.id)
        correct_answer_options.append(i.correct_answer_option)  # Note that it is option , not index , start from 1
        question_answer_set[str(i.id)] = {
            "question": i.question,
            "option1": i.option1,
            "option2": i.option2,
            "option3": i.option3,
            'option4': i.option4
        }
    data_to_be_sent["question_ids"] = question_ids
    data_to_be_sent['correct_answer_options'] = correct_answer_options
    data_to_be_sent["question_answer_set"] = question_answer_set
    return JsonResponse(data_to_be_sent, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def register_battle_history(request):
    data = {}
    status = 500
    if request.method == "POST":
        try:
            body_data = json.loads(request.body)
            user1_id = body_data["user1_id"]
            user2_id = body_data["user2_id"]
            battle_id = body_data["battle_id"]
            questions = body_data["questions"]

            user1 = UserExtendedProfile.objects.get(id=user1_id)
            user2 = UserExtendedProfile.objects.get(id=user2_id)
            battle = Battle.objects.get(id=battle_id)

            points_to_be_deducted = battle.total_points/2
            user1.total_points = user1.total_points - points_to_be_deducted
            user2.total_points = user2.total_points - points_to_be_deducted

            user1.save()
            user2.save()

            PointsLog.objects.create(
                user=user1,
                points= -points_to_be_deducted,
                description= f"Deducted for {battle.category.title} "
            )

            PointsLog.objects.create(
                user=user2,
                points= -points_to_be_deducted,
                description= f"Deducted for {battle.category.title} "
            )

            record = BattleHistory.objects.create(
                user1_id=user1_id,
                user2_id=user2_id,
                battle_id=battle_id,
                questions=json.dumps(questions)
            )
            record.is_running = True
            record.save()
            data["success"] = True
            data["message"] = "Battle Created Successfully"
            data["battle_history_id"] = str(record.id)

            status = 200
        except Exception as e:
            print(e)
            data["success"] = False
            data["message"] = "Failed to create "
            status = 500
    return JsonResponse(data, status=status)


@csrf_exempt
@require_http_methods(["POST"])
def battle_update(request):
    data = {}
    status = 500
    try:
        body_data = json.loads(request.body)
        battle_history_id = body_data["battle_history_id"]
        print(battle_history_id)
        winner_user_id = str(body_data["winner_user_id"]).strip()
        user1_answers = body_data["user1_answers"]
        user2_answers = body_data["user2_answers"]
        print(winner_user_id)

        battel_history_record = BattleHistory.objects.get(id=battle_history_id)
        matchdraw = False
        if winner_user_id == "00000000-0000-0000-0000-000000000000" : matchdraw = True
        # print(matchdraw)
        if not matchdraw:
            winner_user = UserExtendedProfile.objects.get(id=winner_user_id)
            PointsDepositByBattleContest.objects.create(
                points=battel_history_record.battle.total_points,
                battle=battel_history_record,
                category="battle"
            )
            PointsLog.objects.create(
                user=winner_user,
                points=battel_history_record.battle.total_points,
                description=f"Added From {battel_history_record.battle.category.title}"
            )

            winner_user.total_points += battel_history_record.battle.total_points
            winner_user.save()

            battel_history_record.winner_user_id = winner_user_id
        battel_history_record.user1_answers = json.dumps(user1_answers)
        battel_history_record.user2_answers = json.dumps(user2_answers)
        battel_history_record.is_running = False
        battel_history_record.save()
        status = 200
        data["success"] = True
        data["message"] = "Game Completed"
    except Exception as e:
        print(e)
    return JsonResponse(data, status=status)


@require_http_methods(["GET"])
def battle_category_details(request, id):
    battle = Battle.objects.get(id=id)
    data = {}

    data["no_of_questions"] = battle.category.no_of_questions
    data["max_time"] = battle.category.no_of_questions

    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def getProifleInfo(request):

    user = None
    data = {}

    data["message"] = "Based on given query no user exists"
    status = 404

    if "username" in request.GET:
        try :
            username = str(request.GET["username"]).strip()
            user = CustomUser.objects.get(username=username)
        except :
            print("Not found by username")

    elif "id" in request.GET:
        try :
            id = str(request.GET["id"]).strip()
            user = UserExtendedProfile.objects.get(id=id).user_base_profile
        except :
            print("Not found by username")

    if user is not None:
        data["full_name"] = f"{user.first_name} {user.last_name}"
        data["username"] = str(user.username)
        data["profileimage"] = str(user.userextendedprofile.profileimage)
        data["message"] = "success"
        status = 200

    return JsonResponse(data,safe=False,status=status)