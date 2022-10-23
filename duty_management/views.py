from atexit import register
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Reservation,Register,ReservationJudge
from datetime import datetime, timedelta,date
from django.utils.timezone import make_aware
import calendar
import environ

# Create your views here.

env = environ.Env()
env.read_env(".env")

def index(request):
    reservation_list = Reservation.objects.all()
    event_list = []
    for r in reservation_list:
        event_list.append(
            {
                "title" : r.reserver,
                "start" : r.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "end" : r.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    context = {"event_list":event_list}
    return render(request, "duty_management/calendar.html", context)

def reserve(request):
    reservation_list = ReservationJudge.objects.filter(state=3)
    event_list = []
    for r in reservation_list:
        event_list.append(
            {
                "date" : r.date.strftime("%Y-%m-%d"),
            }
        )
    context = {"event_list":event_list}
    return render(request, "duty_management/reserve.html", context)

def reserve_decision(request):
    #空の入力の場合、エラーを返す
    if not request.POST["start_date"]:
        return HttpResponse("日時を入力してください")
    elif not request.POST["end_date"]:
        return HttpResponse("日時を入力してください")
    else:
        posted_start_date = datetime.strptime(request.POST["start_date"]+"  12:00:00","%Y-%m-%d %H:%M:%S")
        posted_end_date = datetime.strptime(request.POST["end_date"]+" 12:00:00","%Y-%m-%d %H:%M:%S")
        
        #ReservationJudgeを定期的に作成
        if len(ReservationJudge.objects.filter(date__gte=posted_end_date))==0:
            days_in_month = calendar.monthrange(posted_end_date.year,posted_end_date.month)[1]
            print(days_in_month)
            for d in range(days_in_month):
                ReservationJudge.objects.create(
                    date = datetime(posted_end_date.year, posted_end_date.month, d+1,12,0,0),
                    state = 0
                )
        
        #予約日程が空いているか否か判定
        day_counter = posted_start_date
        flag = False
        while True:
            print(day_counter)
            state = ReservationJudge.objects.get(date=day_counter).state
            if day_counter == posted_start_date:
                if bin(state & 1) != "0b0":
                    print("pass1")
                    break
            elif day_counter == posted_end_date:
                if bin(state & 2) != "0b0":
                    print("pass2")
                    break
                else:
                    flag = True
                    print("pass4")
                    break
            else:
                if bin(state & 3) != "0b0":
                    print("pass3")
                    break
            day_counter += timedelta(days=1)
        

        # 空いていた場合、ResevationとReservationJudgeに予約情報を追加
        if flag:
            #ReservationJudgeに予約情報を追加
            s = ReservationJudge.objects.get(date=posted_start_date)
            s.state = int(bin(s.state | 1),2) 
            s.save()
            e = ReservationJudge.objects.get(date=posted_end_date)
            e.state = int(bin(e.state | 2),2) 
            e.save()
            ReservationJudge.objects.filter(date__range=[posted_start_date+timedelta(days=1),posted_end_date-timedelta(days=1)]).update(state=3)
            

           

            #Reservationに予約情報を追加
            Reservation.objects.create(reserver=request.user,
                        start_date=posted_start_date,
                        end_date=posted_end_date
                        )

            #メールの送信
            # subject = "Test Mail!!"
            # message = "test"
            # from_email = env('EMAIL_HOST_USER')
            # recipient_list = [env("EMAIL_RESERVER")]
            # send_mail(subject, message, from_email, recipient_list)



            return HttpResponse("new_reservation")
        else:
            return HttpResponse("false")

   
        