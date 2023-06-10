from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
import random 
import datetime

def verifyToken(token):
    verifica = False
    for userTk in Token.objects.all():
        if(token==userTk.key):
            verifica = True
            
    return verifica
    

@api_view(['GET'])
def login(request):
    try: 
        name=(request.GET['username'])
        password=(request.GET['password'])
    except:
        name=""
        password=""
        _token="null"
    _name=False
    if (name==""):
        _message = "email is required"
        _status = "ERROR"
        _token = 'null'
    for user in User.objects.all():
        if (name == user.username):
            name=True
            if (check_password(password,user.password)):
                try:    
                    token = Token.objects.create(user=user)
                except: 
                    token = Token.objects.get(user=user)
                    _token = token.key
                if(status.HTTP_200_OK):
                    _status = "OK"
                    _message = "OK"
                else:
                    _status = "ERROR"
            else:
                _message = "wrong credentials"
                _status = "ERROR"
                _token = "null" 
    if(_name==False):
         _message = "Wrong credentials"
         _status = "ERROR" 
         _token = 'null'
    
    return JsonResponse({"status":_status,"message":_message,"token":_token  })

@api_view(['GET'])
def logout(request):
    try:
        token = (request.GET['token'])
    except:
        token = "null"
    verifica = verifyToken(token)
    if (verifica):
        _status = "OK"
        _message = "Session succesfully closed."
    else:        
        _status = "ERROR"
        _message = "session_token is required"
   
    return JsonResponse({'status': _status, "message":_message})