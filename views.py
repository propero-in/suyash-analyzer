from django.shortcuts import render
import re
from . import task
#import threading

def index(request):
    return render(request, 'index.html')

def analyzer(request):
    context = {}
    regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    txt = request.GET.get('website', 'please enter your website here')
    email = request.GET.get('email', 'please enter your email here')
    context["website"] = txt
    context["email"] = email
    website_matches = ["https://www."]
    if any(x not in txt for x in website_matches) and (re.search(regex,email)) == None:#any(x not in mail for x in email_matches):
        return render(request, 'badcredentials.html')
    if any(x not in txt for x in website_matches):
        return render(request, 'badwebsite.html')
    if(re.search(regex,email)) == None:
        return render(request, 'bademail.html')
    else:
        #t = threading.Thread(target = task.driver, args = [txt, email])
        #t.start()
        task.driver(txt, email)
        return render(request, 'goodrequest.html', context=context)