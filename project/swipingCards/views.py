import datetime
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import requests
from .models import *
from .forms import *
from .serializers import *
# Create your views here.

@csrf_exempt
def sendSMS(OTP, to):
    servicePlanId = "e63e326edadf470783464a02567e0d42"
    apiToken = "9852521f4fec497cb7a065012aae0400"
    sinchNumber = "+447520651288"
    toNumber = f"+91{to}"
    url = "https://us.sms.api.sinch.com/xms/v1/" + servicePlanId + "/batches"

    payload = {
        "from": sinchNumber,
        "to": [
            toNumber
        ],
        "body": f"Your login code is {OTP}"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + apiToken
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    print(data)

class Login(ViewSet):
    def list(self, request):
        return render(request, 'login page.html')

    # @method_decorator([])
    def post(self, request):
        to = request.POST.get('mobile')
        otp = request.POST.get('otp')
        print('-------------', to, otp)
        if to is not None:
            error = ''
            if len(to) < 10:
                error = 'Please enter 10 digit mobile number'
                return render(request, 'login page.html', {'error':error})

            OTP = ''.join(random.sample('012345689', 5))
            print(OTP)
            user = True
            # temp = User.objects.get(username=to)
            # print(temp.is_authenticated)
            try:
                users = User.objects.get(username=to)
                user_id = users.id
            except:
                user = False
            print(user)

            if user:
                data = LoginModel.objects.get(user_id=user_id)
                data.otp = OTP
                data.save()
                log = login(request, user = authenticate(username=to, password='authenticate'))
                print(log)
                sendSMS(OTP, to)
                print('-------------')
                return render(request, 'otp.html', {'mobile': to})

            return render(request, 'Login page.html', {'error':'mobile number is not existing kindly signup' })


        error=''
        to = request.POST.get('mobile1')
        user_id = User.objects.get(username=to).id
        generated_otp = LoginModel.objects.get(user_id=user_id).otp
        print(generated_otp, to, otp)
        if generated_otp == otp:
            return HttpResponseRedirect('main')
        return render(request, 'otp.html', {'mobile': to, 'error':'Incorrect OTP'})


@permission_classes([IsAuthenticated])
class Main(ViewSet):
    # serializer_class = ResultSerializer

    def list(self, request):
        print(self.request.user)
        return render(request, 'main.html', {'user': self.request.user.first_name})

    def post(self, request):
        print('-----------')
        statuses = request.POST.get('statuses')
        print(statuses)
        id = LoginModel.objects.get(user_id=self.request.user.id).id
        Results.objects.create(result1=statuses, attempted_on=datetime.datetime.now(), username_id=id)
        # print(Results.objects.all().values())
        # return HttpResponseRedirect(reverse('/results'))
        return HttpResponseRedirect('/results')

@permission_classes([IsAuthenticated])
class ResultsView(ViewSet):
    def list(self, request):
        return render(request, 'thanks.html', {'user':self.request.user.first_name})

    def post(self, request):
        user_id=self.request.user.id
        id = LoginModel.objects.get(user_id=user_id).id
        result = Results.objects.filter(username_id=id).order_by('result1', 'attempted_on').values()
        dates = []
        times = []
        results = []

        for i in result:
            print(i['result1'])
            dates.append(i['attempted_on'].date())
            times.append(i['attempted_on'].time())
            results.append(i['result1'].split(',')[:5])
        z = zip(dates, times, results)
        print(len(results))
        return render(request, 'results.html', {'dates':dates, 'times':times, 'results':results, 'range':range(len(dates)), 'z':z})


class Signup(ViewSet):
    form = SignupForm()
    def list(self, request):
        # print(self.form)
        return render(request, 'signup.html', {'form':self.form})

    def post(self, request):
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        mobile1 = request.POST.get('mobile1')
        if mobile is not None:
            OTP = ''.join(random.sample('0123456789', 5))
            if User.objects.filter(username=mobile).exists():
                return render(request, 'signup.html', {'error':'mobile number already exists kindly login'})
            form = SignupForm(request.POST)
            form.data = form.data.copy()
            form.data['user'] = User.objects.create_user(username=mobile, password='authenticate', first_name=name).id
            form.data['otp'] = OTP
            print(form.data)

            if form.is_valid():
                form.save()
                sendSMS(OTP, mobile)
                return render(request, 'otp.html', {'mobile':mobile})
            user = User.objects.get(username=mobile).delete()
            return render(request, 'signup.html', {'errors':form.errors})

        error=''
        to = request.POST.get('mobile1')
        otp = request.POST.get('otp')
        user_id = User.objects.get(username=to).id
        generated_otp = LoginModel.objects.get(user_id=user_id).otp
        print(generated_otp, to, otp)
        if generated_otp == otp:
            return HttpResponseRedirect('/main')
        return render(request, 'otp.html', {'mobile': to, 'error':'Incorrect OTP'})

