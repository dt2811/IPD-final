from pickle import TRUE
from django import http
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import AddUser,SetUserValues,ListUsers,RecommendItemsToItem,AddDetailView,AddBookmark,AddPurchase
from recombee_api_client.api_requests import RecommendItemsToUser,Batch,GetItemValues

from health.models import Profile
from django.contrib.auth.models import auth, User
# Create your views here.
from .forms import CreateUserForm
from vokaturi.api.Record import record
from Video_Model import VideoAnalysis



@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'health/audioorvideo.html', context)



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('audvid')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                user_id=User.objects.get(username=user)
                print(user_id.id)
                add_user(user_id.id,user)
                messages.success(request, 'Account was created for ' + user)
                return redirect('health:login')

        context = {'form': form}
        return render(request, 'health/register1.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('health:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                global user_name 
                user_name=user.get_username()
                login(request, user)
                return redirect('health:home')
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, 'health/login1.html', context)


def logoutUser(request):
    logout(request)
    return redirect('health:login')


@login_required(login_url='login')
def audvid(request):
    context = {}
    return render(request, 'health/audioorvideo.html', context)


@login_required(login_url='login')
def audio(request):
    context = {}
    return render(request, 'health/audio.html', context)


def audio_record(request):
    emot = record("output.wav")
    #Neutral: 74.803 Happy: 0.288 Sad: 15.084 Angry: 8.281 Fear: 1.545
    print(emot)
    emotion=emot
    user_id=getUserId(user_name,emotion)    
    data=get_recommendation(user_id)
    movieAndTvshow=[]
    music=[]
    for i in range(0,len(data)):
        if(data[i]['data']['type']=='TvShow' or data[i]['data']['type']=='Movie'):
         data[i]['data']['poster_path']="https://image.tmdb.org/t/p/original"+data[i]['data']['poster_path']
         movieAndTvshow.append(data[i])
        elif(data[i]['data']['type']=='Music'):
            music.append(data[i])
    print(data)
    context = {'data':data,"id":user_id,"movie":movieAndTvshow,"music":music}
    return render(request,'health/main.html', context)

def video_record(request):
    emotion=VideoAnalysis.analyze_video()
    user_id=getUserId(user_name,emotion)   
    data=get_recommendation(user_id)
    movieAndTvshow=[]
    music=[]
    for i in range(0,len(data)):
        if(data[i]['data']['type']=='TvShow' or data[i]['data']['type']=='Movie'):
         data[i]['data']['poster_path']="https://image.tmdb.org/t/p/original"+data[i]['data']['poster_path']
         movieAndTvshow.append(data[i])
        elif(data[i]['data']['type']=='Music'):
            music.append(data[i])
    print(data)
    context = {'data':data,"id":user_id,"movie":movieAndTvshow,"music":music}
    return render(request,'health/main.html', context)

@login_required(login_url='login')
def video(request):
    context = {}
    return render(request, 'health/video.html', context)

def get_recommendation(user_id):
    client = RecombeeClient("abcs-dev", "FoS65UOrCdnud6K3OC6uwGwIDQyzDYGst0dfQcRvzFHpJXBgaxuiphOTEwQJJIgH")
    res=client.send(RecommendItemsToUser(user_id,50,logic={'name':'recombee:personal'})) 
    data=res['recomms']
    product_ids=[]
    for i in range(0,len(data)):
        print(data[i])
        product_ids.append(GetItemValues(data[i]['id']))
    recommendations=client.send(Batch(product_ids))
    final_data=[]
    for i in range(0,len(recommendations)):
        final={"id":data[i]['id'],"data":recommendations[i]['json']}
        final_data.append(final)
    return final_data
        

def add_user(id,username):
    client = RecombeeClient("abcs-dev", "FoS65UOrCdnud6K3OC6uwGwIDQyzDYGst0dfQcRvzFHpJXBgaxuiphOTEwQJJIgH")
    client.send(AddUser(id))
    client.send(SetUserValues((7*id),{'username':username,'current_emotion':'angry'},cascade_create= True))    #angry, fear, neutral, sad, disgust, happy and surprise
    client.send(SetUserValues((7*id)+1,{'username':username,'current_emotion':'fear'},cascade_create= True))    #angry, fear, neutral, sad, disgust, happy and surprise
    client.send(SetUserValues((7*id)+2,{'username':username,'current_emotion':'neutral'},cascade_create= True))    #angry, fear, neutral, sad, disgust, happy and surprise
    client.send(SetUserValues((7*id)+3,{'username':username,'current_emotion':'sad'},cascade_create= True))    #angry, fear, neutral, sad, disgust, happy and surprise
    client.send(SetUserValues((7*id)+4,{'username':username,'current_emotion':'disgust'},cascade_create= True))    #angry, fear, neutral, sad, disgust, happy and surprise
    client.send(SetUserValues((7*id)+5,{'username':username,'current_emotion':'happy'},cascade_create= True))    #angry, fear, neutral, sad, disgust, happy and surprise
    client.send(SetUserValues((7*id)+6,{'username':username,'current_emotion':'suprise'},cascade_create= True))    #angry, fear, neutral, sad, disgust, happy and surprise
    return True

def getItemDetails(request,obj_id,user_id):   
    print(obj_id)
    recommendations=get_user_item_recommendation(obj_id,user_id)
    data=singleItemDetails(obj_id)
    final_recommendations=[]
    for i in range(0,len(recommendations)):
        if(recommendations[i]['data']['type']=='TvShow' or recommendations[i]['data']['type']=='Movie'):
         recommendations[i]['data']['poster_path']="https://image.tmdb.org/t/p/original"+recommendations[i]['data']['poster_path']
        final_recommendations.append(recommendations[i])
    print(final_recommendations[0])
    context={"obj_id":obj_id,"user_id":user_id,"recommendations":final_recommendations,"mainData":data}
    return render(request, 'health/detail.html', context)

def getUserId(username,emotion):
    client = RecombeeClient("abcs-dev", "FoS65UOrCdnud6K3OC6uwGwIDQyzDYGst0dfQcRvzFHpJXBgaxuiphOTEwQJJIgH")
    result = client.send(ListUsers(return_properties=True))
    uid=0
    print("we are in user id function")
    print(username,emotion)
    for i in result:
        print(i)
        if(i['username'] == username and i['current_emotion']== emotion):
            uid=int(i['userId'])
            break
    print('user id is',uid)
    return uid

def get_user_item_recommendation(item_id,user_id):
    item_id=int(item_id)
    user_id=int(user_id)
    
    client = RecombeeClient("abcs-dev", "FoS65UOrCdnud6K3OC6uwGwIDQyzDYGst0dfQcRvzFHpJXBgaxuiphOTEwQJJIgH")
    client.send(AddDetailView(user_id, item_id))
    res = client.send(RecommendItemsToItem(item_id, user_id, 10))
    #res=client.send(RecommendItemsToUser(user_id,10,logic={'name':'recombee:personal'})) 
    data=res['recomms']
    product_ids=[]
    for i in range(0,len(data)):
        print(data[i])
        product_ids.append(GetItemValues(data[i]['id']))
    recommendations=client.send(Batch(product_ids))
    final_data=[]
    for i in range(0,len(recommendations)):
        final={"id":data[i]['id'],"data":recommendations[i]['json']}
        final_data.append(final)
    return final_data

def singleItemDetails(id):
    id=int(id)
    client = RecombeeClient("abcs-dev", "FoS65UOrCdnud6K3OC6uwGwIDQyzDYGst0dfQcRvzFHpJXBgaxuiphOTEwQJJIgH")
    data=client.send(GetItemValues(id))
    data['poster_path']="https://image.tmdb.org/t/p/original"+data['poster_path']
    print(data)
    return data

def like_Item(request,obj_id,user_id):
    client = RecombeeClient("abcs-dev", "FoS65UOrCdnud6K3OC6uwGwIDQyzDYGst0dfQcRvzFHpJXBgaxuiphOTEwQJJIgH")
    client.send(AddBookmark(user_id, obj_id))
    client.send(AddPurchase(user_id,obj_id))
    print(obj_id)
    recommendations=get_user_item_recommendation(obj_id,user_id)
    data=singleItemDetails(obj_id)
    final_recommendations=[]
    for i in range(0,len(recommendations)):
        if(recommendations[i]['data']['type']=='TvShow' or recommendations[i]['data']['type']=='Movie'):
         recommendations[i]['data']['poster_path']="https://image.tmdb.org/t/p/original"+recommendations[i]['data']['poster_path']
        final_recommendations.append(recommendations[i])
    print(final_recommendations[0])
    context={"obj_id":obj_id,"user_id":user_id,"recommendations":final_recommendations,"mainData":data}
    return render(request, 'health/detail.html', context)
    

