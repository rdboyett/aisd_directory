import json
import csv
import re

from django.shortcuts import render, render_to_response, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from directory_app.models import UserInfo, UserAdmin
from google_login.models import GoogleUserInfo


import logging
log = logging.getLogger(__name__)





@csrf_exempt
def checkSessionLogin(request):
    if request.method == 'POST':
        bLogin = request.POST["bLogin"].strip()
        
        data = {'success':'success'}
        
        if bLogin == 'True':
            if 'googleExtension_id' in request.session:
                google_id = request.session['googleExtension_id']
                if UserInfo.objects.filter(google_id=google_id):
                    userInfo = UserInfo.objects.get(google_id=google_id)
                    googleUserInfo = GoogleUserInfo.objects.get(google_id=google_id)
                
                    data['user'] = 'loggedIn'
		    data['google_id'] = userInfo.google_id
                    data['firstName'] = userInfo.firstName
                    data['lastName'] = userInfo.lastName
                    data['school'] = userInfo.school
                    data['grade'] = userInfo.grade
                    data['job'] = userInfo.job
                    data['subject'] = userInfo.subject
                    data['roomNumber'] = userInfo.roomNumber
                    data['phoneExtension'] = userInfo.phoneExtension
                    data['picture'] = googleUserInfo.googleAvatar
                    
                    # for testing purposes
                    #request.session.delete()
                    
                else:
                    data = {'error': "no user in system",}
            else:
                data = {'error': "no session id",}
        else:
            data = {'error': "no login password",}
    else:
        data = {'error': "no post made",}
        
            
    return HttpResponse(json.dumps(data))






@csrf_exempt
def login(request):
    if request.method == 'POST':
        google_id = request.POST["google_id"]
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        google_email = request.POST["email"]
        picture = request.POST["picture"]
        
        data = {'success':'success'}
        
        emailEnding = google_email.split("@")[1]
        userName = "@"+google_email.split("@")[0]
        
        if User.objects.filter(email=google_email):
            # Make sure that the e-mail is unique.
            user = User.objects.get(email=google_email)
            #userInfo = UserInfo.objects.get(user=user)
        else:
            if 'alvaradoisd.net' in emailEnding:
                if 'student' in emailEnding:
                    data = {'error': "Please sign in with an Alvarado ISD Employee Email Account.",}
                    return HttpResponse(json.dumps(data))
                else:
                    bTeacher = True
                
                    user = User.objects.create(
                        username = userName,
                        first_name = firstName,
                        last_name = lastName,
                        email = google_email,
                        password = 'password',
                    )
                    
                    data['account'] = 'created'
            else:
                data = {'error': "Please sign in with your Alvarado ISD account.",}
                return HttpResponse(json.dumps(data))
        
        '''
        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            data['user'] = 'loggedIn'
            
        '''
        if UserInfo.objects.filter(email=google_email):
	    userInfo = UserInfo.objects.get(google_id=google_id)
        else:
            userInfo = UserInfo.objects.create(
                user = user,
                google_id = google_id,
                lastName = lastName,
                firstName = firstName,
                email=google_email,
            )
            
        # create google user 
        #Check to see if a google account has been setup yet
        if GoogleUserInfo.objects.filter(google_id=google_id):
            googleUserInfo = GoogleUserInfo.objects.get(google_id=google_id)
        else:
            googleUserInfo = GoogleUserInfo.objects.create(
                user = user,
                google_id = google_id,
                googleAvatar = picture,
            )
        
        
        data['user'] = 'loggedIn'
        data['firstName'] = userInfo.firstName
        data['lastName'] = userInfo.lastName
        data['school'] = userInfo.school
        data['grade'] = userInfo.grade
        data['job'] = userInfo.job
        data['subject'] = userInfo.subject
        data['roomNumber'] = userInfo.roomNumber
        data['phoneExtension'] = userInfo.phoneExtension
        data['picture'] = googleUserInfo.googleAvatar
        
        #Now save id into a session cookie
        request.session['googleExtension_id'] = google_id
        request.session.set_expiry(3000000)
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))




@csrf_exempt
def search_bar(request):
    if request.method == 'POST':
        originalTerm = request.POST["term"]
        if len(originalTerm)>2 or originalTerm[0].isdigit():
            term = originalTerm
            term = term.strip()
            wordList = term.split()
            
            #test is term contains more than one word
            allUsersList = []
            userIds = []
            
                #Here is the order
                #Try startswith first and the contains
                #Last name
                #first name
                #school
                #job
                #subject
                
                
                
            for term in wordList:
                if len(term)>2 or term[0].isdigit():
                    if UserInfo.objects.filter(lastName__istartswith=term):
                        allUsersLast = UserInfo.objects.filter(lastName__istartswith=term).order_by("lastName")
                    else:
                        allUsersLast = False
                    
                    #Get all allUsersLast Id's in a list to exclude from the allUsersFirst Id's
                    if allUsersLast:
                        for user in allUsersLast:
                            if user.id in userIds:
                                allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                            else:
                                userIds.append(user.id)
                                allUsersList.append(user)
                    
                    if UserInfo.objects.filter(firstName__istartswith=term):
                        allUsersFirst = UserInfo.objects.filter(firstName__istartswith=term).order_by("lastName")
                    else:
                        allUsersFirst = False
                        
                    if allUsersFirst:
                        for user in allUsersFirst:
                            if user.id in userIds:
                                allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                            else:
                                userIds.append(user.id)
                                allUsersList.append(user)
                    
                    if UserInfo.objects.filter(lastName__icontains=term):
                        allUsersContainsLast = UserInfo.objects.filter(lastName__icontains=term).order_by("lastName")
                    else:
                        allUsersContainsLast = False
                    
                    if allUsersContainsLast:
                        for user in allUsersContainsLast:
                            if user.id in userIds:
                                allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                            else:
                                userIds.append(user.id)
                                allUsersList.append(user)
                                
                    # UserInfo ID# *********************************************************
                    anyNumbersList = re.findall(r'\d+', term)
                    if anyNumbersList:
                        checkNumber = int(anyNumbersList[0])
                        #then it is a number
                        if UserInfo.objects.filter(roomNumber=checkNumber):
                            allUsersID = UserInfo.objects.filter(roomNumber=checkNumber)
                        else:
                            allUsersID = False
                        if allUsersID:
                            for user in allUsersID:
                                if user.id in userIds:
                                    allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                                else:
                                    userIds.append(user.id)
                                    allUsersList.append(user)
                        
                        #Now check phone
                        if UserInfo.objects.filter(phoneExtension=checkNumber):
                            allUsersID = UserInfo.objects.filter(phoneExtension=checkNumber)
                        else:
                            allUsersID = False
                        if allUsersID:
                            for user in allUsersID:
                                if user.id in userIds:
                                    allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                                else:
                                    userIds.append(user.id)
                                    allUsersList.append(user)
                                
                    #Check for user with school---------------------------------------------
                    if UserInfo.objects.filter(school__icontains=term):
                        allUsersContainsLast = UserInfo.objects.filter(school__icontains=term).order_by("lastName")
                    else:
                        allUsersContainsLast = False
                    
                    if allUsersContainsLast:
                        for user in allUsersContainsLast:
                            if user.id in userIds:
                                allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                            else:
                                userIds.append(user.id)
                                allUsersList.append(user)
                        
                    #Check for user with subject---------------------------------------------
                    if UserInfo.objects.filter(subject__icontains=term):
                        allUsersContainsLast = UserInfo.objects.filter(subject__icontains=term).order_by("lastName")
                    else:
                        allUsersContainsLast = False
                    
                    if allUsersContainsLast:
                        for user in allUsersContainsLast:
                            if user.id in userIds:
                                allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                            else:
                                userIds.append(user.id)
                                allUsersList.append(user)
                    
                    #Check for user with job---------------------------------------------
                    if UserInfo.objects.filter(job__icontains=term):
                        allUsersContainsLast = UserInfo.objects.filter(job__icontains=term).order_by("lastName")
                    else:
                        allUsersContainsLast = False
                    
                    if allUsersContainsLast:
                        for user in allUsersContainsLast:
                            if user.id in userIds:
                                allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                            else:
                                userIds.append(user.id)
                                allUsersList.append(user)
                    
                res = []
                for user in allUsersList:
                    dict = {'user_id':user.id, 'html':user.firstName + ' ' + user.lastName + ' - ' + user.school}
                    res.append(dict)
         
    return HttpResponse(json.dumps(res))



@csrf_exempt
def search(request):
    if request.method == 'POST':
        originalTerm = request.POST["q"]
        if len(originalTerm)>2 or originalTerm[0].isdigit():
            term = originalTerm
            term = term.strip()
            wordList = term.split()
            
            #test is term contains more than one word
            allUsersList = []
            userIds = []
            
                #Here is the order
                #Try startswith first and the contains
                #Last name
                #first name
                #school
                #job
                #subject
                
                
                
            for term in wordList:
                if UserInfo.objects.filter(lastName__istartswith=term):
                    allUsersLast = UserInfo.objects.filter(lastName__istartswith=term).order_by("lastName")
                else:
                    allUsersLast = False
                
                #Get all allUsersLast Id's in a list to exclude from the allUsersFirst Id's
                if allUsersLast:
                    for user in allUsersLast:
                        if user.id in userIds:
                            allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                        else:
                            userIds.append(user.id)
                            allUsersList.append(user)
                
                if UserInfo.objects.filter(firstName__istartswith=term):
                    allUsersFirst = UserInfo.objects.filter(firstName__istartswith=term).order_by("lastName")
                else:
                    allUsersFirst = False
                    
                if allUsersFirst:
                    for user in allUsersFirst:
                        if user.id in userIds:
                            allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                        else:
                            userIds.append(user.id)
                            allUsersList.append(user)
                
                if UserInfo.objects.filter(lastName__icontains=term):
                    allUsersContainsLast = UserInfo.objects.filter(lastName__icontains=term).order_by("lastName")
                else:
                    allUsersContainsLast = False
                
                if allUsersContainsLast:
                    for user in allUsersContainsLast:
                        if user.id in userIds:
                            allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                        else:
                            userIds.append(user.id)
                            allUsersList.append(user)
                
                # UserInfo ID# *********************************************************
                anyNumbersList = re.findall(r'\d+', term)
                if anyNumbersList:
                    checkNumber = int(anyNumbersList[0])
                    #then it is a number
                    if UserInfo.objects.filter(id=checkNumber):
                        allUsersID = UserInfo.objects.filter(id=checkNumber)
                    else:
                        allUsersID = False
                    if allUsersID:
                        for user in allUsersID:
                            if user.id in userIds:
                                allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                            else:
                                userIds.append(user.id)
                                allUsersList.append(user)
                
                #Check for user with school---------------------------------------------
                if UserInfo.objects.filter(school__icontains=term):
                    allUsersContainsLast = UserInfo.objects.filter(school__icontains=term).order_by("lastName")
                else:
                    allUsersContainsLast = False
                
                if allUsersContainsLast:
                    for user in allUsersContainsLast:
                        if user.id in userIds:
                            allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                        else:
                            userIds.append(user.id)
                            allUsersList.append(user)
                    
                #Check for user with subject---------------------------------------------
                if UserInfo.objects.filter(subject__icontains=term):
                    allUsersContainsLast = UserInfo.objects.filter(subject__icontains=term).order_by("lastName")
                else:
                    allUsersContainsLast = False
                
                if allUsersContainsLast:
                    for user in allUsersContainsLast:
                        if user.id in userIds:
                            allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                        else:
                            userIds.append(user.id)
                            allUsersList.append(user)
                
                #Check for user with job---------------------------------------------
                if UserInfo.objects.filter(job__icontains=term):
                    allUsersContainsLast = UserInfo.objects.filter(job__icontains=term).order_by("lastName")
                else:
                    allUsersContainsLast = False
                
                if allUsersContainsLast:
                    for user in allUsersContainsLast:
                        if user.id in userIds:
                            allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                        else:
                            userIds.append(user.id)
                            allUsersList.append(user)

                #Check for user with email---------------------------------------------
                if UserInfo.objects.filter(email__istartswith=term):
                    allUsersContainsLast = UserInfo.objects.filter(email__istartswith=term).order_by("lastName")
                else:
                    allUsersContainsLast = False
                
                if allUsersContainsLast:
                    for user in allUsersContainsLast:
                        if user.id in userIds:
                            allUsersList.insert(0, allUsersList.pop(allUsersList.index(user)))
                        else:
                            userIds.append(user.id)
                            allUsersList.append(user)
                
            
            args = {
                'userInfo':allUsersList,
            }
                
            return render_to_response('table_display.html', args )
            
            
            
            
            
        else:
            data = {
                'error': "Search term too short.",
            }
            
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))



@csrf_exempt
def submitProfileUpdate(request):
    if request.method == 'POST':
        google_id = str(request.POST["google_id"]).strip()
        firstName = str(request.POST["firstName"]).strip()
        lastName = str(request.POST["lastName"]).strip()
        school = str(request.POST["school"]).strip()
        grade = str(request.POST['grade']).strip()
        job = str(request.POST["job"]).strip()
        subject = str(request.POST["subject"]).strip()
        roomNumber = str(request.POST["roomNumber"])
        phoneExtension = request.POST["phoneExtension"]
        
        data = {'success':'success'}
        
        if UserInfo.objects.filter(google_id=google_id):
	    userInfo = UserInfo.objects.get(google_id=google_id)
            userInfo.school = school
            userInfo.lastName = lastName
            userInfo.firstName = firstName
            userInfo.grade = grade
            userInfo.job = job
            userInfo.subject = subject
            userInfo.roomNumber = roomNumber
            if phoneExtension:
                userInfo.phoneExtension = int(phoneExtension)
            else:
                userInfo.phoneExtension = None
            userInfo.save()
            
            
            if User.objects.filter(id=userInfo.user.id):
                user = User.objects.get(id=userInfo.user.id)
                user.last_name = lastName
                user.first_name = firstName
                user.save()
            
            data['firstName'] = userInfo.firstName
            data['lastName'] = userInfo.lastName
            data['school'] = userInfo.school
            data['grade'] = userInfo.grade
            data['job'] = userInfo.job
            data['subject'] = userInfo.subject
            data['roomNumber'] = userInfo.roomNumber
            data['phoneExtension'] = userInfo.phoneExtension
        
        else:
            data = {
                'error': "There was an error posting this request. Please try again.",
            }
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))






























