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





def index(request):
    return  HttpResponseRedirect("/google/auth/")


def logoutSuccess(request):
    return  HttpResponse('You have logged out!  <a href="/google/auth/">Login again</a>')

@login_required
def dashboard(request):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        userAdmin = False
        
    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'advancedSearch':True,
    }
    args.update(csrf(request))
        
    return render_to_response('dashboard.html', args )



@login_required
def add(request):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        return redirect('/dashboard/')
        
    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'addEmployee':True,
    }
    args.update(csrf(request))
        
    return render_to_response('addEmployee.html', args )



@login_required
def batchAdd(request):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        return redirect('/dashboard/')
        
    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'batchAdd':True,
    }
    args.update(csrf(request))
        
    return render_to_response('batchAdd.html', args )


@login_required
def myProfile(request):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        userAdmin = False
        
    #check to see if there is a userInfo for this user
    if UserInfo.objects.filter(email=request.user.email):
        userInfo = UserInfo.objects.get(email=request.user.email)
    else:
        userInfo = False
        
        
    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'userInfo':userInfo,
        'myProfile':True,
    }
    args.update(csrf(request))
        
    return render_to_response('myProfile.html', args )


@login_required
def profile(request):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        userAdmin = False
        
    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'addEmployee':True,
    }
    args.update(csrf(request))
        
    return render_to_response('profile.html', args )





@login_required
def searchResults(request):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        userAdmin = False
        
    if request.method == 'POST':
        
        userList = []
        
        try:
            searchTerm = request.POST['q'].strip()
            
            
            #Check to see if the term is a number.
            anyNumberList = re.findall(r'\d+', searchTerm)
            if anyNumberList:
                #it is a number Search room# and phone# first
                
                #first check phone extension if the number is less than four
                if UserInfo.objects.filter(phoneExtension__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(phoneExtension__istartswith=searchTerm)
                    for user in userInfo:
                        userList.append(user)
                
                #check room number
                if UserInfo.objects.filter(roomNumber__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(roomNumber__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
            else:
                #it's not a number
                if UserInfo.objects.filter(firstName__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(firstName__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
                if UserInfo.objects.filter(lastName__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(lastName__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
                if UserInfo.objects.filter(email__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(email__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
                if UserInfo.objects.filter(subject__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(subject__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                            
                if UserInfo.objects.filter(subject__icontains=searchTerm):
                    userInfo = UserInfo.objects.filter(subject__icontains=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
                if UserInfo.objects.filter(job__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(job__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
                if UserInfo.objects.filter(job__icontains=searchTerm):
                    userInfo = UserInfo.objects.filter(job__icontains=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
                if UserInfo.objects.filter(school__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(school__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
                if UserInfo.objects.filter(roomNumber__istartswith=searchTerm):
                    userInfo = UserInfo.objects.filter(roomNumber__istartswith=searchTerm)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
                
        except:
            firstName = request.POST['firstName'].strip()
            lastName = request.POST['lastName'].strip()
            email = request.POST['email'].strip()
            grade = request.POST['grade'].strip()
            subject = request.POST['subject'].strip()
            job = request.POST['job'].strip()
            school = request.POST['school'].strip()
            roomNumber = request.POST['roomNumber'].strip()
            phone = request.POST['phone']
            
            if firstName:
                if UserInfo.objects.filter(firstName__istartswith=firstName):
                    userInfo = UserInfo.objects.filter(firstName__istartswith=firstName)
                    for user in userInfo:
                        if user not in userList:
                            userList.append(user)
            log.info('After firstName: '+str(userList))
            
            if lastName:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.lastName.lower() == lastName.lower():
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(lastName__istartswith=lastName):
                        userInfo = UserInfo.objects.filter(lastName__istartswith=lastName)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After lastName: '+str(userList))
                    
            
            
            if email:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.email == email:
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(email=email):
                        userInfo = UserInfo.objects.filter(email=email)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After email: '+str(userList))
            
            
            if grade:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.grade == grade:
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(grade=grade):
                        userInfo = UserInfo.objects.filter(grade=grade)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After grade: '+str(userList))
            
            
            if subject:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.subject == subject:
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(subject=subject):
                        userInfo = UserInfo.objects.filter(subject=subject)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After subject: '+str(userList))
            
            
            if job:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.job.lower() == job.lower():
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(job__istartswith=job):
                        userInfo = UserInfo.objects.filter(job__istartswith=job)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After job: '+str(userList))
            
            
            if school:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.school == school:
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(school=school):
                        userInfo = UserInfo.objects.filter(school=school)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After school: '+str(userList))
            
            
            if roomNumber:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.roomNumber.lower() == roomNumber.lower():
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(roomNumber__istartswith=roomNumber):
                        userInfo = UserInfo.objects.filter(roomNumber__istartswith=roomNumber)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After roomNumber: '+str(userList))
            
            
            if phone:
                #check to see if there is someone in the userList
                if userList:
                    #check to see if the user in the list matches. If it doesn't then remove it from the list.
                    #Then check if the list is empty.  If it is the automatically end the search and give no matches found.
                    for user in userList:
                        if not user.phoneExtension == int(phone):
                            userList.remove(user)
                    if not userList:
                        return render_to_response('search_display.html', {'user':request.user,'userInfo':False} )
                else:
                    if UserInfo.objects.filter(phoneExtension=phone):
                        userInfo = UserInfo.objects.filter(phoneExtension=phone)
                        for user in userInfo:
                            if user not in userList:
                                userList.append(user)
            log.info('After phone: '+str(userList))
            
            
    
    
    else:
        return redirect('/dashboard/')
    
    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'userInfo':userList
    }
    args.update(csrf(request))
        
    return render_to_response('search_display.html', args )


def test(request):
    return  HttpResponse("test there!")


@login_required
def editEmployee(request, userID=False):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        return redirect('/dashboard/')
        
    if not userID:
        return redirect('/add/')
    
    else:
        if UserInfo.objects.filter(id=int(userID)):
            userInfo = UserInfo.objects.get(id=int(userID))
        else:
            return redirect('/add/')
            
            
        if GoogleUserInfo.objects.filter(google_id=userInfo.google_id):
            googleUser = GoogleUserInfo.objects.get(google_id=userInfo.google_id)
        else:
            googleUser = False

    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'userInfo':userInfo,
        'googleUser':googleUser,
    }
    args.update(csrf(request))
        
    return render_to_response('editEmployee.html', args )
    





















































################ AJAX CALLS #############################################################


@csrf_exempt
def search_bar(request):
    searchTerm = request.GET.get('term').strip().lower() #jquery-ui.autocomplete parameter
    
    
    res = []
    idList = []
    
    #Check to see if the term is a number.
    anyNumberList = re.findall(r'\d+', searchTerm)
    if anyNumberList:
        #it is a number Search room# and phone# first
        
        #first check phone extension if the number is less than four
        if UserInfo.objects.filter(phoneExtension__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(phoneExtension__istartswith=searchTerm)
            for user in userInfo:
                dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                res.append(dict)
                idList.append(user.id)
        
        #check room number
        if UserInfo.objects.filter(roomNumber__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(roomNumber__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
    else:
        #it's not a number
        if UserInfo.objects.filter(firstName__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(firstName__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
        if UserInfo.objects.filter(lastName__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(lastName__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
        if UserInfo.objects.filter(email__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(email__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
        if UserInfo.objects.filter(subject__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(subject__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
                    
        if UserInfo.objects.filter(subject__icontains=searchTerm):
            userInfo = UserInfo.objects.filter(subject__icontains=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
        if UserInfo.objects.filter(job__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(job__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
        if UserInfo.objects.filter(job__icontains=searchTerm):
            userInfo = UserInfo.objects.filter(job__icontains=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
        if UserInfo.objects.filter(school__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(school__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
        if UserInfo.objects.filter(roomNumber__istartswith=searchTerm):
            userInfo = UserInfo.objects.filter(roomNumber__istartswith=searchTerm)
            for user in userInfo:
                if user.id not in idList:
                    dict = {'id':user.id, 'label':user.firstName+' '+user.lastName+' - '+str(user.school), 'value':user.email}
                    res.append(dict)
                    idList.append(user.id)
        
         
    return HttpResponse(json.dumps(res))




@login_required
def addEmployeeAjax(request):
    if request.method == 'POST':
        addOrUpdate = request.POST['addOrUpdate']
        firstName = request.POST['firstName'].strip().title()
        lastName = request.POST['lastName'].strip()
        email = request.POST['email'].strip()
        grade = request.POST['grade'].strip()
        subject = request.POST['subject'].strip()
        job = request.POST['job'].strip().title()
        school = request.POST['school'].strip()
        roomNumber = request.POST['roomNumber'].strip()
        phone = request.POST['phone']
        
        #check to see if the email already exists
        if UserInfo.objects.filter(email=email):
            userInfo = UserInfo.objects.get(email=email)
            if addOrUpdate == 'add':
                return HttpResponse(json.dumps({'email':email+" already exists.  Do you want to update this person's information?"}))
            else:
                userInfo.firstName = firstName
                userInfo.lastName = lastName
                userInfo.grade = grade
                userInfo.subject = subject
                userInfo.job = job
                userInfo.school = school
                userInfo.roomNumber = roomNumber
                if phone:
                    userInfo.phoneExtension = int(phone)
                else:
                    userInfo.phoneExtension = None
                userInfo.save()
        else:
            userInfo = UserInfo.objects.create(
                firstName = firstName,
                lastName = lastName,
                email = email,
                grade = grade,
                subject = subject,
                job = job,
                school = school,
                roomNumber = roomNumber,
            )
            if phone:
                userInfo.phoneExtension = int(phone)
            else:
                userInfo.phoneExtension = None
            userInfo.save()
            
	if userInfo.user:
            if User.objects.filter(id=userInfo.user.id):
                user = User.objects.get(id=userInfo.user.id)
                user.last_name = lastName
                user.first_name = firstName
                user.save()
        
        
        data = {'success':'true'}
    else:
        data = {'error':"sorry, I'm so embarrased, but there seems to be a problem that is out of my control."}
                
    return HttpResponse(json.dumps(data))


@login_required
def uploadCSV(request):
    if request.method == 'POST':
        csvFile =request.FILES['CSVFile']
        name = request.FILES['CSVFile'].name
        '''
        lines = csvFile.read().splitlines()
        csvFile.close()
        '''
        
        lines = []
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            lines.append(row)
        
        try:
            firstNameIndex = lines[0].index('First Name')
            lastNameIndex = lines[0].index('Last Name')
            emailIndex = lines[0].index('Email')
            schoolIndex = lines[0].index('School')
            positionIndex = lines[0].index('Position')
            gradeIndex = lines[0].index('Grade')
            subjectIndex = lines[0].index('Subject')
            roomNumberIndex = lines[0].index('Room Number')
            phoneIndex = lines[0].index('Phone Extension')
        except:
            data = {'error':'Please use the correct grade report.',}
            return HttpResponse(json.dumps(data))
        
        counter = 0
        length_of_lines = len(lines)
        for i in range(1, len(lines)):
            counter += 1
            if UserInfo.objects.filter(email=lines[i][emailIndex]):
                userInfo = UserInfo.objects.get(email=lines[i][emailIndex])
            else:
                userInfo = UserInfo.objects.create(
                    firstName = lines[i][firstNameIndex],
                    lastName = lines[i][lastNameIndex],
                    email = lines[i][emailIndex],
                    school = lines[i][schoolIndex],
                    job = lines[i][positionIndex],
                    grade = lines[i][gradeIndex],
                    subject = lines[i][subjectIndex],
                    roomNumber = lines[i][roomNumberIndex],
                )
                if not lines[i][phoneIndex] == "":
                    userInfo.phoneExtension = int(lines[i][phoneIndex])
                userInfo.save()
            
        data = {
            'success': 'True',
        }
        
    
    else:
        data = {'error':'Did not post correctly',}
            
    return HttpResponse(json.dumps(data))




@login_required
def getUserInfo(request):
    if request.method == 'POST':
        userInfoID = request.POST['userID']
        
        if UserInfo.objects.filter(id=int(userInfoID)):
            userInfo = UserInfo.objects.get(id=int(userInfoID))
        else:
            userInfo = False
            
            
        if GoogleUserInfo.objects.filter(google_id=userInfo.google_id):
            googleUser = GoogleUserInfo.objects.get(google_id=userInfo.google_id)
        else:
            googleUser = False

    args = {
        'user':request.user,
        'userInfo':userInfo,
        'googleUser':googleUser,
    }
        
    return render_to_response('info_display.html', args )



@login_required
def updateEmployee(request):
    if request.method == 'POST':
        userID = int(request.POST['userID'])
        firstName = request.POST['firstName'].strip().title()
        lastName = request.POST['lastName'].strip()
        email = request.POST['email'].strip()
        grade = request.POST['grade'].strip()
        subject = request.POST['subject'].strip()
        job = request.POST['job'].strip().title()
        school = request.POST['school'].strip()
        roomNumber = request.POST['roomNumber'].strip()
        phone = request.POST['phone']
        
        #check to see if the email already exists
        if UserInfo.objects.filter(id=userID):
            userInfo = UserInfo.objects.get(id=userID)
            if firstName:
                userInfo.firstName = firstName
            if lastName:
                userInfo.lastName = lastName
            if email:
                userInfo.email = email
            if grade:
                userInfo.grade = grade
            if subject:
                userInfo.subject = subject
            if job:
                userInfo.job = job
            if school:
                userInfo.school = school
            if roomNumber:
                userInfo.roomNumber = roomNumber
            if phone:
                userInfo.phoneExtension = int(phone)
                
            userInfo.save()
        else:
            userInfo = UserInfo.objects.create(
                firstName = firstName,
                lastName = lastName,
                email = email,
                grade = grade,
                subject = subject,
                job = job,
                school = school,
                roomNumber = roomNumber,
                phoneExtension = phone,
            )
            
        
        
        data = {'success':'true'}
    else:
        data = {'error':"sorry, I'm so embarrased, but there seems to be a problem that is out of my control."}
                
    return HttpResponse(json.dumps(data))




@login_required
def deleteEmployee(request):
    if request.method == 'POST':
        userID = int(request.POST['userID'])


        #check to see if the email already exists
        if UserInfo.objects.filter(id=userID):
            userInfo = UserInfo.objects.get(id=userID)
            userInfo.delete()
            data = {'success':'true'}
        else:
            data = {'error':"sorry, I'm so embarrased, but that record does not exist."}
            
        
        
        
    else:
        data = {'error':"sorry, I'm so embarrased, but there seems to be a problem that is out of my control."}
                
    return HttpResponse(json.dumps(data))
























