from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
# for post requests
import requests
import json
# Needed for User
from django.contrib.auth.models import User

def home(request):
    

    if request.method == 'POST':
        ticker = request.POST['ticker']

        api_request = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_4f52bccf84804a059a27dfbc8c5a7e01".format(ticker))
    
        try: 
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
        
    else:
        return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above."})

    
def about(request):
    return render(request, 'about.html', {})

def stock_info(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']

        api_request = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_4f52bccf84804a059a27dfbc8c5a7e01".format(ticker))
    
        try: 
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'stock_info.html', {'api': api})
        
    else:
        return render(request, 'stock_info.html', {'ticker': "Enter a Ticker Symbol Above."})  

# Watch stock and delete

def watch_stock(request):
    import requests
    import json

    if request.method == 'POST':
       form  = StockForm(request.POST or None) 

       if form.is_valid():
           form.save()
           messages.success(request, ("Stock is being watched"))
           return redirect('watch_stock')

    else:
        ticker = Stock.objects.filter(user=request.user)
        output = []

        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_4f52bccf84804a059a27dfbc8c5a7e01".format(str(ticker_item)))
    
            try: 
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
    
        return render(request, 'watch_stock.html', {'ticker': ticker, 'output': output})

def delete(request, symbol):
    item = Stock.objects.get(ticker=str(symbol.lower())) # Needs to be lower case
    item.delete()
    messages.success(request, ("Stock unwatched"))
    return redirect(watch_stock)

# Email registration

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Works?
#from django.utils import six
from six import text_type

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')