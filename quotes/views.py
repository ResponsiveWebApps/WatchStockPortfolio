from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
# for post requests
import requests
import json

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
        ticker = Stock.objects.all()
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