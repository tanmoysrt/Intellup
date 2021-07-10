import json

import razorpay
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from datahandler.templates_email import RESET_PASSWORD_TEMPLATE
from normaluser.decorators import normal_user_login_required
from datahandler.models import *
from utils.communication import send_mail
from utils.generators import randomStringGenerator, generate_random_filename
from utils.validators import check_mail
from edugame.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


def LoginPage(request):
    data = {}
    next = None
    if "next" in request.GET:
        next = request.GET["next"]

    if request.user.is_authenticated:
        if next is not None:
            return redirect(next)
        return redirect("/")

    if request.method == "POST":
        userid = str(request.POST.get("userid", "")).strip()
        password = str(request.POST.get("pass", "")).strip()
        is_email = check_mail(userid)

        if userid != "" and password != "":
            data["userid"] = userid
            try:
                user = None
                if is_email:
                    user = CustomUser.objects.get(email=userid)
                else:
                    user = CustomUser.objects.get(username=userid)
                if user.check_password(password):
                    login(request, user)
                    if next is not None:
                        return redirect(next)
                    return redirect("/")
                else:
                    data[
                        "message"] = """<div class="alert alert-danger" role="alert">Username or Password not matched.</div>"""

            except Exception as e:
                print(e)
                data[
                    "message"] = """<div class="alert alert-danger" role="alert">Username or Password not matched.</div>"""
    return render(request, "normaluser/login.html", data)


def RegisterPage(request):
    failed_verification = False
    next = None
    if "next" in request.GET:
        next = request.GET["next"]
    data = {
        "school_classes": SchoolClass.objects.all()
    }

    if request.method == "POST":
        username = str(request.POST.get("username", "")).strip().replace(" ", "").replace("<", "").replace(">", "")
        first_name = str(request.POST.get("first_name", "")).strip()
        last_name = str(request.POST.get("last_name", "")).strip()
        email = str(request.POST.get("email", "")).strip()
        dob = str(request.POST.get("dob", "")).strip()
        print(dob)
        present_class = str(request.POST.get("present_class", "")).strip()
        password = str(request.POST.get("pass", "")).strip()
        confirm_password = str(request.POST.get("confirm_pass", "")).strip()

        data["username"] = username
        data["first_name"] = first_name
        data["last_name"] = last_name
        data["email"] = email
        data["dob"] = dob
        data["class"] = present_class

        if password != confirm_password:
            failed_verification = True
            data[
                "message"] = """<div class="alert alert-danger" role="alert">Password & Confirm Password Not Matched</div>"""

        elif not check_mail(email):
            failed_verification = True
            data["message"] = """<div class="alert alert-danger" role="alert">Email address not valid</div>"""

        elif len(CustomUser.objects.filter(username=username)) != 0 or len(CustomUser.objects.filter(email=email)) != 0:
            failed_verification = True
            data["message"] = """<div class="alert alert-danger" role="alert">Username or Email Already Exsists</div>"""

        if not failed_verification:
            try:
                baseProfile = CustomUser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                baseProfile.save()
                extendedProfile = UserExtendedProfile.objects.create(
                    user_base_profile=baseProfile,
                    dob=dob,
                    present_class_id=present_class,
                    total_points=10000
                )
                extendedProfile.save()
                login(request, user=baseProfile)
                if next is not None:
                    return redirect(next)
                return redirect("/")

            except Exception as e:
                print(e)
                data["message"] = """<div class="alert alert-danger" role="alert">User already Exsists</div>"""

    return render(request, "normaluser/signup.html", data)


@csrf_exempt
def ResetPass(request):
    if request.method == "POST":
        userid = str(json.loads(request.body)["userid"]).strip()
        is_email = check_mail(userid)
        try:
            user = None
            if is_email:
                user = CustomUser.objects.get(email=userid)
            else:
                user = CustomUser.objects.get(username=userid)

            print(user)
            record = ResetPasswordDB.objects.create(
                user=user.userextendedprofile,
                key=randomStringGenerator(length=50),
            )
            record.save()
            mail_body = RESET_PASSWORD_TEMPLATE.format(record.user.user_base_profile.first_name,
                                                       record.user.user_base_profile.last_name, record.id, record.key)
            send_mail(record.user.user_base_profile.email, mail_body)
            return JsonResponse(
                {"message": "If you have an account, a reset link has been sent to your email id", "success": True},
                status=200)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"message": "If you have an account, a reset link has been sent to your email id", "success": True},
                status=200)
        except Exception as e:
            print(e)

    return JsonResponse({"message": "Method Not Allowed", "success": False}, status=405)


def ResetPassVerify(request, id):
    key = None
    data = {}
    if "key" in request.GET:
        key = request.GET.get("key", "")

    else:
        return HttpResponse("Key Missing", status=401)

    try:
        resetDBRecord = ResetPasswordDB.objects.get(id=id)
        if resetDBRecord.is_used:
            return HttpResponse("Link Already Used")

        elif resetDBRecord.key != key:
            return HttpResponse("Invalid Reset Link")
        else:
            if request.method == "POST":
                password = str(request.POST.get("pass", "")).strip()
                confirm_password = str(request.POST.get("confirm_pass", "")).strip()

                if password != confirm_password:
                    data["message"] = "Password Not Matched"

                else:
                    user = resetDBRecord.user.user_base_profile
                    user.set_password(password)
                    user.save()
                    resetDBRecord.is_used = True
                    resetDBRecord.save()

                    data["message"] = "Password Changed Successfully"
                    login(request, user)
                    return redirect("/login/")

            return render(request, "normaluser/resetPassVerify.html", data)
    except:
        return HttpResponse("Reset link is not correct", status=404)


@normal_user_login_required
def chooseSubjectForBattle(request):
    data = {
        "subjects": Battle.objects.filter(school_class_id=request.user.userextendedprofile.present_class_id).values(
            "school_subject_id", "school_subject__title")
    }
    return render(request, "normaluser/selectSubject.html", data)


@normal_user_login_required
def chooseBattleCategoryPage(request, subject_id):
    data = {
        "battleCategories": Battle.objects.filter(
            school_class_id=request.user.userextendedprofile.present_class_id).filter(school_subject_id=subject_id)
    }

    return render(request, "normaluser/battle-type.html", data)


@normal_user_login_required
def startWelcomeBattle(request, id):
    battle_record = Battle.objects.get(id=id)
    if request.user.userextendedprofile.total_points < battle_record.total_points or request.user.userextendedprofile.total_points == 0:
        return render(request,"normaluser/more_coins_need.html")
    data = {
        "battle_data": battle_record
    }
    seconds = battle_record.category.max_time
    minutes = int(seconds / 60)
    seconds = seconds % 60

    data["minutes"] = minutes
    data["seconds"] = seconds

    data["maxTime"] = battle_record.category.max_time

    data["classId"] = battle_record.school_class.id
    data["subjectId"] = battle_record.school_subject.id

    return render(request, "normaluser/game.html", data)


@normal_user_login_required
def battle_result(request, id):
    try:
        battle_history = BattleHistory.objects.get(id=id)
        data = {
            "battle": battle_history,
            "coins_earned": 0
        }
        print(request.user.userextendedprofile.id)
        print(battle_history.winner_user_id)

        if battle_history.is_running:
            return render(request, "normaluser/battlerunning.html", data)
        else:
            if str(request.user.userextendedprofile.id) == str(battle_history.winner_user_id):
                data["coins_earned"] = battle_history.battle.total_points
                return render(request, "normaluser/winner.html", data)
            elif str(battle_history.winner_user_id) == "00000000-0000-0000-0000-000000000000" or str(
                    battle_history.winner_user_id) == "":
                return render(request, "normaluser/draw.html", data)
            else:
                return render(request, "normaluser/loser.html", data)
    except:
        return HttpResponse("<h1>404 Not Found</h1>")


@normal_user_login_required
def contest_list(request):
    data = {
        "contest_list": Contest.objects.filter(school_class_id=request.user.userextendedprofile.present_class_id,
                                               valid_till__gte=timezone.now())
    }
    return render(request, "normaluser/eventslist.html", data)


@normal_user_login_required
def contest_welcome_page(request, id):
    contest = Contest.objects.get(id=id)
    already_started_playing = False
    alreadyPlayed = False
    battle_history_id = None
    contestHistoryRecord = ContestHistory.objects.filter(user_id=request.user.userextendedprofile.id, contest_id=id)
    print(contestHistoryRecord)
    if len(contestHistoryRecord) > 0:
        already_started_playing = True
        if not contestHistoryRecord.first().is_running:
            alreadyPlayed = True
            battle_history_id = contestHistoryRecord.first().id

    print(alreadyPlayed)
    data = {"contest": contest, "is_started": contest.starting_from.__lt__(timezone.now()),
            "is_ended": contest.valid_till.__lt__(timezone.now()), "already_started_playing": already_started_playing, "alreadyPlayed":alreadyPlayed,"battle_history_id":battle_history_id}

    # print(f'started : {data["is_started"]} ended : {data["is_ended"]}')
    return render(request, "normaluser/contestWelcome.html", data)


@normal_user_login_required
def contest_middleware_page(request, id):
    try:
        contestHistory = ContestHistory.objects.get(user_id=request.user.userextendedprofile.id, contest_id=id)
        return redirect("/contest/play/{}".format(contestHistory.id))
    except ObjectDoesNotExist:
        record = ContestHistory.objects.create(
            user=request.user.userextendedprofile,
            contest_id=id
        )
        return redirect("/contest/play/{}".format(record.id))
    except:
        return HttpResponse("Unexpected Error 500", status=500)


@normal_user_login_required
def contest_playing_page(request, id):
    contest_history = ContestHistory.objects.get(id=id)

    # If already submitted then redirect to result page
    if not contest_history.is_running:
        return redirect(f"/contest/result/{id}/")
    contest = contest_history.contest
    data = {"is_started": contest.starting_from.__lt__(timezone.now()),
            "is_ended": contest.valid_till.__lt__(timezone.now()),
            "exsistingTimeForContest": (contest.valid_till - timezone.now()).total_seconds()}

    if not data["is_started"] and data["is_ended"]:
        # TODO Add html page
        return HttpResponse("Expired contest")

    question_set = contest.questionanswerforcontest_set.all()

    question_answer_set = {}
    for i in question_set:
        question_answer_set[str(i.id)] = {
            "question": i.question,
            "option1": i.option1,
            "option2": i.option2,
            "option3": i.option3,
            'option4': i.option4
        }

    data["question_answer_set"] = json.dumps(question_answer_set)

    return render(request, "normaluser/contestPlaying.html", data)


@normal_user_login_required
@require_http_methods(["POST"])
@csrf_exempt
def contestSumissionApi(request, id):
    contest_history_record = ContestHistory.objects.get(id=id)

    if not contest_history_record.is_running:
        return JsonResponse({
            "message": "Succesfully Saved",
            "success": True,
            "redirect_url": f"/contest/result/{id}/"
        })

    if str(contest_history_record.user.user_base_profile.id) == str(request.user.id):
        # print(f"User {request.user}")
        req_body = json.loads(request.body)
        question_ids = [int(i) for i in req_body["questions_id"]]
        answers_ids = req_body["answers_id"]
        question_set = contest_history_record.contest.questionanswerforcontest_set.all()
        total_questions = len(question_set)

        # This is re-creating to avoid any type of erro in sequence of elements
        result_answers = []
        answers_ids_final = []
        for i in question_set:
            q_index = question_ids.index(i.id)
            user_given_answer = answers_ids[q_index]
            answers_ids_final.append(answers_ids[q_index])
            if i.correct_answer_option == user_given_answer:
                print("Correct {}".format(user_given_answer))
                result_answers.append(1)
            else:
                print("OOPS")
                result_answers.append(0)

        percentage_score = result_answers.count(1) / total_questions

        contest_history_record.answers = json.dumps(answers_ids)
        contest_history_record.result_answers = json.dumps(result_answers)
        contest_history_record.percentage_of_correct_answers = percentage_score
        contest_history_record.is_running = False
        contest_history_record.save()

        contest_user = request.user.userextendedprofile
        contest_user.score_contest = contest_user.score_contest + percentage_score
        contest_user.save()

        return JsonResponse({
            "message": "Succesfully Saved",
            "success": True,
            "redirect_url": f"/contest/result/{id}/"
        })
    return JsonResponse({"message": "you are not authorized"}, status=401)



@normal_user_login_required
def contest_result(request, id):
    contest_history_record = ContestHistory.objects.get(id=id)
    data = {
        "percentage" : contest_history_record.percentage_of_correct_answers*100
    }
    return render(request, "normaluser/contestResult.html",data)


@normal_user_login_required
def coin_pack_list(request):
    data = {
        "coinPackages": CoinPackages.objects.all(),
    }
    return render(request, "normaluser/coins.html", data)


@normal_user_login_required
def coin_recharge(request):
    if "coinPackId" in request.GET:
        coinPackId = request.GET["coinPackId"]
        coin_pack_record = CoinPackages.objects.get(id=coinPackId)
        transaction_log_record = TransactionLogs.objects.create(
            user=request.user.userextendedprofile,
            price=coin_pack_record.price * 100,
            coins_to_be_deposited=coin_pack_record.coins
        )
        data = {
            "razorpay_key_id": RAZORPAY_KEY_ID,
            "transaction_log_record": transaction_log_record
        }
        return render(request, "normaluser/coinspayment.html", data)

    return HttpResponse("Not accepted")


@normal_user_login_required
def verfiypayment(request):
    if "payment_id" in request.GET and "transaction_id" in request.GET:
        payment_id = request.GET["payment_id"]
        transaction_id = request.GET["transaction_id"]
        transaction_log_record = TransactionLogs.objects.get(id=transaction_id)
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        razorpay_client.payment.capture(payment_id=payment_id, amount=transaction_log_record.price)
        log = razorpay_client.payment.fetch(payment_id)

        if log["status"] == "captured":
            transaction_log_record.transaction_id = payment_id
            transaction_log_record.status = True
            profile = UserExtendedProfile.objects.get(user_base_profile__id=request.user.id)
            profile.total_points = profile.total_points + transaction_log_record.coins_to_be_deposited
            profile.save()
        else:
            transaction_log_record.transaction_id = payment_id
        transaction_log_record.save()
        return redirect("/recharge/")

    return HttpResponse("OK")



@normal_user_login_required
def profileDetails(request):
    data = {
        "classes" : SchoolClass.objects.all()
    }
    if request.FILES:
        profile_picture = request.FILES["profile_picture"]
        fs = FileSystemStorage(location='media/profile/')
        filename = fs.save(generate_random_filename(profile_picture.name), profile_picture)
        profile_picture_name = fs.generate_filename(filename)
        profile_picture_name = "profile/"+profile_picture_name

        profile = request.user.userextendedprofile
        profile.profileimage = profile_picture_name
        profile.save()

    elif request.method == "POST":
        first_name = request.POST.get("first_name","")
        last_name = request.POST.get("last_name","")
        dob = request.POST.get("dob","")
        present_class = request.POST.get("class","")

        base_user = request.user
        base_user.first_name = first_name
        base_user.last_name = last_name
        base_user.save()

        profile = base_user.userextendedprofile
        profile.dob = dob
        profile.present_class = SchoolClass.objects.get(id=present_class)
        profile.save()

    return render(request, "normaluser/prof-details.html",data)



@normal_user_login_required
def profileWallet(request):
    return render(request, "normaluser/prof-wallet.html")



@normal_user_login_required
def profileSettings(request):
    data = {}
    if request.method == "POST":
        old_password = str(request.POST.get("old_password", "")).strip()
        new_password = str(request.POST.get("new_password", "")).strip()
        confirm_new_password = str(request.POST.get("confirm_new_password", "")).strip()

        if new_password != confirm_new_password:
            data["message"] = """<div class="alert alert-warning">Password & Confirm Password Not Matched</div>"""
        elif request.user.check_password(old_password):
            user = request.user
            user.set_password(new_password)
            data["message"] = """<div class="alert alert-success">Password Changed Successfully</div>"""
        else:
            data["message"] = """<div class="alert alert-danger">Wrong Password ! Try Again</div>"""

    return render(request, "normaluser/prof-settings.html", data)



@normal_user_login_required
def profileStats(request):
    battle_records_history = BattleHistory.objects.filter(Q(user1_id=request.user.userextendedprofile.id) | Q(user2_id=request.user.userextendedprofile.id)).order_by("-id")
    won_in_battles = 0
    last_20_battle_win_or_loose = []
    for i in battle_records_history[0:21]:
        if str(i.winner_user_id) == str(request.user.userextendedprofile.id):
            last_20_battle_win_or_loose.append(1)
            won_in_battles += 1
        else : last_20_battle_win_or_loose.append(0)

    data = {
        "total_battles_played_count" : len(battle_records_history),
        "total_won_battle_count" : won_in_battles,
        "last_20_battle_win_or_loose" : last_20_battle_win_or_loose
    }
    return render(request, "normaluser/prof-stats.html", data)


def logoutUser(request):
    logout(request)
    return redirect("/")


def homePage(request):
    return render(request,"normaluser/homepage.html")

@normal_user_login_required
def leaderboard(request):
    data = {
        "leaderboardMembers" : UserExtendedProfile.objects.all().order_by("-score_contest")
    }
    return render(request,"normaluser/universalLeaderBoard.html",data)