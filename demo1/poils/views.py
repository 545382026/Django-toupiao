from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Questions,Choices
# Create your views here.

def index(request):

    que = Questions.objects.all()

    return render(request, 'poils/index.html',{'que':que})
    # return HttpResponse('首页')


def choice(request, id):
    choice = Questions.objects.get(pk=int(id))
    return render(request,'poils/choice.html',{'ques':choice})
    # return HttpResponse('选择页')

def choicehand(request):
    chid = request.POST['chid']
    qid = request.POST['id']
    print(qid)
    print(chid)

    que = Questions.objects.get(pk=qid)
    ch = Choices.objects.get(pk=chid)
    ch.num += 1
    # ch.cquesid = que
    ch.save()

    return render(request,'poils/choicehand.html',{'que':que})
    # return HttpResponse('h1')

def result(request):
    ch = Choices.objects.all()
    q = Questions.objects.all()

    return render(request,'poils/result.html', {'que':q})
