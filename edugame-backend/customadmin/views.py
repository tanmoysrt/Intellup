import datetime

from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from customadmin.decorators import admin_user_login_required
from datahandler.models import *


# TODO
@admin_user_login_required
def dashboard(request):
    return redirect("/admin/question/all/")
    return render(request, "customadmin/dashboard.html")


# TODO
@admin_user_login_required
def master_dashboard(request):
    return render(request, "customadmin/master_dashboard.html")


@admin_user_login_required
def all_questions(request):
    data = {
        "questions": QuestionBrunch.objects.all()
    }
    if "delete_id" in request.GET:
        delete_id = request.GET["delete_id"]
        try:
            record = QuestionBrunch.objects.get(id=delete_id)
            record.delete()
            data[
                "message"] = f"""<div class="alert alert-success" role="alert">Question No {delete_id} has been deleted Successfully !!</div>"""
        except:
            data[
                "message"] = f"""<div class="alert alert-warning" role="alert">Questipon No {delete_id} not exsist</div>"""

    return render(request, "customadmin/all_questions.html", data)


@admin_user_login_required
def add_new_quesion(request):
    data = {
        "classes": SchoolClass.objects.all(),
        "subjects": SchoolSubject.objects.all(),
        "levels": DIFFICULTY_LEVEL
    }
    if request.method == "POST":
        try:
            question = str(request.POST.get("question", "")).strip()
            option1 = str(request.POST.get("option1", "")).strip()
            option2 = str(request.POST.get("option2", "")).strip()
            option3 = str(request.POST.get("option3", "")).strip()
            option4 = str(request.POST.get("option4", "")).strip()
            correct_answer_option = int(request.POST.get("correct_answer_option", -1))
            subject_id = request.POST.get("subject")
            class_id = request.POST.get("class")
            difficulty = request.POST.get("difficulty")
            points = request.POST.get("points")

            record = QuestionBrunch.objects.create(
                school_class_id=class_id,
                school_subject_id=subject_id,
                question=question,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_answer_option=correct_answer_option,
                points=points,
                difficulty=difficulty
            )
            record.save()
            data[
                "message"] = f"""<div class="alert alert-success" role="alert">Question No {record.id} has been created Successfully !!</div>"""
        except:
            data["message"] = f"""<div class="alert alert-danger" role="alert">Failed To Create Question</div>"""
    return render(request, "customadmin/add_new_question.html", data)


@admin_user_login_required
def edit_question(request, id):
    data = {
        "classes": SchoolClass.objects.all(),
        "subjects": SchoolSubject.objects.all(),
        "levels": DIFFICULTY_LEVEL
    }
    try:
        record = QuestionBrunch.objects.get(id=id)
        data["record"] = record

        if request.method == "POST":
            try:
                question = str(request.POST.get("question", "")).strip()
                option1 = str(request.POST.get("option1", "")).strip()
                option2 = str(request.POST.get("option2", "")).strip()
                option3 = str(request.POST.get("option3", "")).strip()
                option4 = str(request.POST.get("option4", "")).strip()
                correct_answer_option = int(request.POST.get("correct_answer_option", -1))
                subject_id = request.POST.get("subject")
                class_id = request.POST.get("class")
                difficulty = request.POST.get("difficulty")
                points = request.POST.get("points")

                record.question = question
                record.option1 = option1
                record.option2 = option2
                record.option3 = option3
                record.option4 = option4
                record.correct_answer_option = correct_answer_option
                record.school_subject_id = subject_id
                record.school_class_id = class_id
                record.difficulty = difficulty
                record.points = points
                record.save()

                data[
                    "message"] = f"""<div class="alert alert-success" role="alert">Question No {record.id} has been updated Successfully !!</div>"""
            except:
                data["message"] = f"""<div class="alert alert-danger" role="alert">Failed To Update Question</div>"""

        return render(request, "customadmin/edit_question.html", data)
    except:
        return redirect("/newadmin/question/all/")


@admin_user_login_required
def battle_category(request):
    data = {
        "categories": BattleCategory.objects.all(),
    }
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            time_bound = int(request.POST.get("time_bound"))
            max_time = request.POST.get("max_time")
            no_of_questions = request.POST.get("no_of_questions")

            record = BattleCategory.objects.create(
                title=title,
                time_bound=True if time_bound == 1 else False,
                max_time=max_time,
                no_of_questions=no_of_questions
            )
            record.save()
            data[
                "message"] = f"""<div class="alert alert-success" role="alert">Battle Category with ID {record.id} Added Successfully.</div>"""
        except Exception as e:
            print(e)
            data["message"] = f"""<div class="alert alert-danger" role="alert">Failed</div>"""

    return render(request, "customadmin/battle_category.html", data)


@admin_user_login_required
def battles(request):
    data = {
        "battle_categories": BattleCategory.objects.all(),
        "subjects": SchoolSubject.objects.all(),
        "classes": SchoolClass.objects.all(),
        "difficulty_level": DIFFICULTY_LEVEL
    }

    if "id" in request.GET and "task" in request.GET:
        try:
            id = request.GET["id"]
            task = str(request.GET["task"]).strip()
            battle = Battle.objects.get(id=id)
            if task == "enable":
                battle.is_active = True
            elif task == "disable":
                battle.is_active = False
            battle.save()
            data[
                "message"] = f"""<div class="alert alert-success" role="alert">Battle Id {battle.id} has been updated Successfully !!</div>"""
        except ObjectDoesNotExist:
            data["message"] = f"""<div class="alert alert-danger" role="alert">Battle ID Not Found</div>"""
        except Exception as e:
            print(e)
            data["message"] = f"""<div class="alert alert-danger" role="alert">Unknown Error</div>"""

    if request.method == "POST":
        try:
            battle_category = int(request.POST["battle_category"])
            school_class = int(request.POST["class"])
            subject = int(request.POST["subject"])
            difficulty_level = request.POST["difficulty_level"]
            total_points = int(request.POST["total_points"])

            record = Battle.objects.create(
                total_points=total_points,
                difficulty=difficulty_level,
                category_id=battle_category,
                school_class_id=school_class,
                school_subject_id=subject
            )
            record.save()

            data[
                "message"] = f"""<div class="alert alert-success" role="alert">Battle Id {record.id} has been created Successfully !!</div>"""
        except Exception as e:
            print(e)
            data["message"] = f"""<div class="alert alert-danger" role="alert">Unknown Error</div>"""
    data["activeBattles"] = Battle.objects.filter(is_active=True)
    data["expiredBattles"] = Battle.objects.filter(is_active=False)

    return render(request, "customadmin/battles.html", data)


@admin_user_login_required
def create_contest(request):
    data = {
        "classes": SchoolClass.objects.all(),
        "subjects": SchoolSubject.objects.all(),
        "levels": CONTEST_DIFFICULTY_LEVEL,
    }
    if request.method == "POST":
        try:
            title = str(request.POST.get("title", "")).strip()
            subject_id = request.POST.get("subject")
            class_id = request.POST.get("class")
            difficulty = request.POST.get("difficulty")
            points = request.POST.get("points")
            validity = request.POST.get("validity")
            points_to_deduct = request.POST.get("points_to_deduct")
            starting_from = request.POST.get("starting_from")

            record = Contest.objects.create(
                school_class_id=class_id,
                school_subject_id=subject_id,
                title=title,
                max_point=points,
                difficulty=difficulty,
                valid_till=validity,
                point_to_deduct=points_to_deduct,
                starting_from=starting_from
            )
            record.save()
            data[
                "message"] = f"""<div class="alert alert-success" role="alert">Contest ID {record.id} & Name {record.title} has been created Successfully !!</div>"""
        except:
            data["message"] = f"""<div class="alert alert-danger" role="alert">Failed To Create Contest</div>"""
    return render(request, "customadmin/create_contest.html", data)


@admin_user_login_required
def config_contest_questions(request):
    data = {
        "contests": Contest.objects.all().order_by("-created_on")
    }
    return render(request, "customadmin/contestList.html", data)


@admin_user_login_required
def config_contest_questions_seperate(request, id):
    try:
        contest_record = Contest.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse("No Contest Found With This ID", status=404)
    data = {}
    if request.method == "POST":
        try:
            question = request.POST.get("question")
            option1 = request.POST.get("option1")
            option2 = request.POST.get("option2")
            option3 = request.POST.get("option3")
            option4 = request.POST.get("option4")
            correct_answer_option = int(request.POST.get("correct_answer_option"))

            question_record = QuestionAnswerForContest.objects.create(
                question=question,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_answer_option=correct_answer_option,
                contest=contest_record
            )

            question_record.save()
            data["message"] = f"""<div class="alert alert-success" role="alert">Question Added Successfully !!</div>"""
        except:
            data["message"] = f"""<div class="alert alert-danger" role="alert">Failed To Create Question</div>"""

    data["contest"] = contest_record

    return render(request, "customadmin/add_edit_contest_questions.html", data)


@admin_user_login_required
def today_contest_stat(request):
    now = datetime.datetime.now()
    data = {
        "histories": ContestHistory.objects.filter(created_on__month=now.month, created_on__year=now.year,
                                                   created_on__day=now.day).order_by("-points")
    }
    return render(request, "customadmin/today_contest_stat.html", data)


@admin_user_login_required
def old_contest_stat(request):
    data = {
        "histories": ContestHistory.objects.filter()
    }
    return render(request, "customadmin/old_contest_stat.html", data)


@admin_user_login_required
def logout_admin(request):
    logout(request)
    return redirect("/")
