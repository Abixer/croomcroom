from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from allauth.account.decorators import verified_email_required
from demo.forms import *
from demo import models as m
from datetime import datetime
from django.core.urlresolvers import reverse
from operator import attrgetter
from django.forms.models import inlineformset_factory
from django.forms.models import formset_factory

def loadMostRecentCanvas(context, project):
	loadCanvas(context, project, -1)

def loadCanvas(context, project, canvasId):

	canvasId = int(canvasId)

	if canvasId < 0:
		canvasId += len(context['business_model'])
	
	#Fixes weird model caching bug, edit at your own risk
	for cur in context['business_model']:
		tmp=cur.business_model_name
		
	context['canvasId'] = canvasId
		


	key_partners = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'key_partners')
	key_activities = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'key_activities')
	key_resources = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'key_resources')
	value_propositions = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'value_propositions')
	customer_relationships = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'customer_relationships')
	channels = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'channels')
	customer_segments = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'customer_segments')
	cost_structure = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'cost_structure')
	revenue_streams = m.Business_model_notes.getBusiness_model_notes(context['business_model'][canvasId], 'revenue_streams')
		
	context['key_partners'] = key_partners
	context['key_activities'] = key_activities
	context['key_resources'] = key_resources
	context['value_propositions'] = value_propositions
	context['customer_relationships'] = customer_relationships
	context['channels'] = channels
	context['customer_segments'] = customer_segments
	context['cost_structure'] = cost_structure
	context['revenue_streams'] = revenue_streams

class redirect_profile_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):	
		if not request.user.profile.skills:
			return redirect('profile_edit')
		return self.orig_func(request, *args, **kwargs)
	
class logged_in_setup_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
		


		
			
		#Mark appropriate notifications as read
		#Maybe a weird race condition with this pattern
		seenNotifications = m.Notifications.objects.filter(user_id=request.user, urlToRemove=request.path)
		for seenNotification in seenNotifications:
			seenNotification.hasSeen = True
			seenNotification.save()
		
		notifications = m.Notifications.objects.filter(user_id=request.user)
		
		forms = []
		for notification in notifications:
			forms.append(NotificationForm(initial={'notification' : notification.notification_id}))		
			
		context['notificationCount'] = len([x for x in notifications if x.hasSeen == False])
		context['notifications'] = [list(x) for x in zip(notifications, forms)]
		
		context['unread_messages'] = getAllUnreadMessagesRelevantToUser(request.user)
		kwargs['context'] = context
		return self.orig_func(request, *args, **kwargs)
		
class project_setup_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
			
		project_name = kwargs['project_name']
			
		project = m.Project.objects.get(title=project_name)
		context['project_name'] = project_name
		context['project'] = project
		
		kwargs['context'] = context
		return self.orig_func(request, *args, **kwargs)

		
class project_participant_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		
		project_name = kwargs['project_name']
		project = m.Project.objects.get(title=project_name)
		
		allowed = m.Project.getTeamMembers(project)
		
		if request.user in allowed:
			return self.orig_func(request, *args, **kwargs)
		else:
			if request.user in [x.user_id for x in m.Spectators.objects.all()]:
				return self.orig_func(request, *args, **kwargs)
			return redirect('startups')

class business_model_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']		
		
		canvas_id = kwargs['canvas_id']		
	
		project_name = kwargs['project_name']	
		project = m.Project.objects.get(title=project_name)
		
		business_models = m.Business_model.getBusiness_model(project)
		context['business_model'] = business_models
		
		##NEW
		"""i = 0
		for model in business_models:
			context['key_partners_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'key_partners')
			context['key_activities_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'key_activities')
			context['key_resources_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'key_resources')
			context['value_propositions_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'value_propositions')
			context['customer_relationships_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'customer_relationships')
			context['channels_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'channels')
			context['customer_segments_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'customer_segments')
			context['cost_structure_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'cost_structure')
			context['revenue_streams_' + str(i)] = m.Business_model_notes.getBusiness_model_notes(model, 'revenue_streams')
			i+=1"""
			
		
		loadCanvas(context, context['project'], canvas_id)
		
		return self.orig_func(request, *args, **kwargs)
	
class milestones_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
		
		project_name = kwargs['project_name']	
		project = m.Project.objects.get(title=project_name)
		
		milestones = m.Milestone.getProjectMilestones(project)
		context['milestones'] = milestones
		
		return self.orig_func(request, *args, **kwargs)
	

class user_messages_for_user_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
		
		messagesToUser = m.Messages_from_user_to_user.getMessagesToUser(request.user)
		messagesFromUser = m.Messages_from_user_to_user.getMessagesFromUser(request.user)
		combinedMessages = []
		for message in messagesToUser:
			combinedMessages.append(message)
		for message in messagesFromUser:
			combinedMessages.append(message)
		combinedMessages = sorted(combinedMessages, key=attrgetter('timestamp'), reverse=True)
		#setup the relevant users for messaging
		uniquePeople = set()
		people = []
		for message in combinedMessages:
			if message.user_id_from != request.user:
				uniquePeople.add(message.user_id_from)
			else:
				uniquePeople.add(message.user_id_to)
		
		#setup the messages per people
		for person in uniquePeople:
			messageListForPerson = []
			people.append( [ person, messageListForPerson ] )
			for message in combinedMessages:
				if message.user_id_from == request.user and message.user_id_to == person:
					messageListForPerson.append(message)
				elif message.user_id_to == request.user and message.user_id_from == person:
					messageListForPerson.append(message)
					
		#setup the message convo forms for each person			
		messageFormSet = formset_factory(MessageConvoForm, extra=len(people))
		context['userMessageFormSetFactory'] = messageFormSet
		userMessageFormSet = messageFormSet(prefix='users')
		for form, person in zip(userMessageFormSet, people):
			form.fields['recipient'].initial = person[0].username
			person.append(form)
		context['userMessageFormSet'] = userMessageFormSet
		
		#set the context
		context['people'] = people
		m.Messages_from_user_to_user.messagesRead(request.user)
		return self.orig_func(request, *args, **kwargs)
	
class project_messages_for_user_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
			
		messagesFromUser = m.Messages_from_user_to_project.getMessagesFromUser(request.user)
		for message in messagesFromUser:
			message.type = 1 #set this as a user sender message
			
		messagesFromProject = m.Messages_from_project_to_user.getMessagesToUser(request.user)
		for message in messagesFromProject:
			message.type = 2 #set this as a project sender message
			
		combinedMessages = []
		for message in messagesFromUser:
			combinedMessages.append(message)
		for message in messagesFromProject:
			combinedMessages.append(message)
		combinedMessages = sorted(combinedMessages, key=attrgetter('timestamp'), reverse=True)
		#setup the relevant recipients for messaging
		uniqueRecipientProject = set()
		for message in combinedMessages:
			if message.type == 1:
				uniqueRecipientProject.add(message.project_id_to)
			else:
				uniqueRecipientProject.add(message.project_id_from)
		
		projects = []
		#setup the messages per recipient of interest
		for recipientProject in uniqueRecipientProject:
			messageListForProject = []
			projects.append( [ recipientProject, messageListForProject ] )
			for message in combinedMessages:
				if message.type == 1 and message.project_id_to == recipientProject:
					messageListForProject.append(message)
				elif message.type == 2 and message.project_id_from == recipientProject:
					messageListForProject.append(message)
		context['projects'] = projects
		
		#setup the message convo forms for each project			
		messageFormSet = formset_factory(MessageConvoForm, extra=len(projects))
		context['projectMessageFormSetFactory'] = messageFormSet
		projectMessageFormSet = messageFormSet(prefix='projects')
		for form, project in zip(projectMessageFormSet, projects):
			form.fields['recipient'].initial = project[0].title
			project.append(form)
		context['projectMessageFormSet'] = projectMessageFormSet
		
		m.Messages_from_project_to_user.messagesRead(request.user)
		return self.orig_func(request, *args, **kwargs)

		
class user_messages_for_project_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
		
		project_name = kwargs['project_name']
		project = m.Project.objects.get(title=project_name)
		
		messagesFromProject = m.Messages_from_project_to_user.getMessagesFromProject(project)
		messagesToProject = m.Messages_from_user_to_project.getMessagesToProject(project)
		combinedMessages = []
		for message in messagesToProject:
			message.type = 1 #set this as a user sender message
			combinedMessages.append(message)
		for message in messagesFromProject:
			message.type = 2 #set this as a project sender message
			combinedMessages.append(message)
		combinedMessages = sorted(combinedMessages, key=attrgetter('timestamp'), reverse=True)
		
		#setup the relevant users for messaging
		uniquePeople = set()
		people = []
		for message in combinedMessages:
			if message.type == 1:
				uniquePeople.add(message.user_id_from)
			else: #type == 2
				uniquePeople.add(message.user_id_to)
		
		#setup the messages per people
		for person in uniquePeople:
			messageListForPerson = []
			people.append( [ person, messageListForPerson ] )
			for message in combinedMessages:
				if message.type == 1 and message.user_id_from == person:
					messageListForPerson.append(message)
				elif message.type == 2 and message.user_id_to == person:
					messageListForPerson.append(message)
					
		#setup the message convo forms for each person			
		messageFormSet = formset_factory(MessageConvoForm, extra=len(people))
		context['userMessageFormSetFactory'] = messageFormSet
		userMessageFormSet = messageFormSet(prefix='users')
		for form, person in zip(userMessageFormSet, people):
			form.fields['recipient'].initial = person[0].username
			person.append(form)
		context['userMessageFormSet'] = userMessageFormSet
		context['people'] = people
		
		m.Messages_from_user_to_project.messagesRead(project)
		return self.orig_func(request, *args, **kwargs)		
		
class project_messages_for_project_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
		
		project_name = kwargs['project_name']
		project = m.Project.objects.get(title=project_name)
		
		messagesFromProject = m.Messages_from_project_to_project.getMessagesFromProject(project)	
		messagesToProject = m.Messages_from_project_to_project.getMessagesToProject(project)

		combinedMessages = []
		for message in messagesFromProject:
			message.type = 1 #type 1 means the project is the sender
			combinedMessages.append(message)
		for message in messagesToProject:
			message.type = 2 #type 2 means the project is the receiver
			combinedMessages.append(message)
		combinedMessages = sorted(combinedMessages, key=attrgetter('timestamp'), reverse=True)
		
		#setup the relevant recipients for messaging
		uniqueRecipientProject = set()
		for message in combinedMessages:
			if message.type == 1:
				uniqueRecipientProject.add(message.project_id_to)
			else:
				uniqueRecipientProject.add(message.project_id_from)
		
		projects = []
		#setup the messages per recipient of interest
		for recipientProject in uniqueRecipientProject:
			messageListForProject = []
			projects.append( [ recipientProject, messageListForProject ] )
			for message in combinedMessages:
				if message.type == 1 and message.project_id_to == recipientProject:
					messageListForProject.append(message)
				elif message.type == 2 and message.project_id_from == recipientProject:
					messageListForProject.append(message)
					
		#setup the message convo forms for each project			
		messageFormSet = formset_factory(MessageConvoForm, extra=len(projects))
		context['projectMessageFormSetFactory'] = messageFormSet
		projectMessageFormSet = messageFormSet(prefix='projects')
		for form, currProject in zip(projectMessageFormSet, projects):
			form.fields['recipient'].initial = currProject[0].title
			currProject.append(form)
		context['projectMessageFormSet'] = projectMessageFormSet			
		context['projects'] = projects
		
		m.Messages_from_project_to_project.messagesRead(project)
		return self.orig_func(request, *args, **kwargs)	
		
class message_modal_decorator(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, *args, **kwargs):
		context = {}
		if 'context' in kwargs:
			context = kwargs['context']
		
		context['message_form'] = ModalMessageForm()
		
		return self.orig_func(request, *args, **kwargs)
		
def getAllUnreadMessagesRelevantToUser(user_id):
	messagesFromUser = m.Messages_from_user_to_user.getUnreadMessages(user_id)	
	messagesFromProject = m.Messages_from_project_to_user.getUnreadMessages(user_id)
	
	result = []
	for message in messagesFromUser:
		message.type = 1;
		if len(message.content) > 40:
			message.content = message.content[0:38] + "..."
		result.append(message)
	for message in messagesFromProject:
		message.type = 2;
		result.append(message)
	result = sorted(result, key=attrgetter('timestamp'), reverse=True)
	if len(result) > 10:
		result = result[0:10]
	return result

def index(request):
	context = {}
	return render(request, 'demo/index.html', context) 
	
def new_profile(request):
	context = {}
	return render(request, 'demo/new_profile.html', context)
	
def register(request):
	context = {}
	return render(request, 'demo/register.html', context)
	
@verified_email_required 	
@logged_in_setup_decorator
@redirect_profile_decorator
def dashboard(request, context):
	context['FeedPosts'] = m.FeedPosts.objects.filter(user_id=request.user)
	return render(request, 'demo/dashboard.html', context)

	
@verified_email_required 	
@logged_in_setup_decorator
def about(request, context):
	return render(request, 'demo/about.html', context)
	
@verified_email_required 
@logged_in_setup_decorator
@project_messages_for_user_decorator
@user_messages_for_user_decorator
def messaging(request, context):
	if request.method == 'GET':
		message_form = MessageForm()
		context['message_form'] = message_form
	else: #post
		message_form = MessageForm(request.POST)
		context['message_form'] = message_form
		userMessageFormSet = context['userMessageFormSetFactory'](request.POST, prefix='users')
		projectMessageFormSet = context['projectMessageFormSetFactory'](request.POST, prefix='projects')
		if message_form.is_valid():
			if message_form.cleaned_data['recipient_type'] == 'User':
				recipientUser = User.objects.get(username=message_form.cleaned_data['recipient'])
				if recipientUser:
					m.Messages_from_user_to_user.newMessage(request.user, recipientUser, message_form.cleaned_data['content'])
					return redirect('messaging')
			else: #project
				recipientProject = m.Project.objects.get(title=message_form.cleaned_data['recipient'])
				if recipientProject:
					m.Messages_from_user_to_project.newMessage(request.user, recipientProject, message_form.cleaned_data['content']) 
					return redirect('messaging')
		else:
			context['error'] = "Could not find recipient"
		#form handling for user convos
		for form in userMessageFormSet:
			if form.is_valid():
				content = form.cleaned_data['content']
				recipientUser = User.objects.get(username=form.cleaned_data['recipient'])
				if recipientUser:
					m.Messages_from_user_to_user.newMessage(request.user, recipientUser, form.cleaned_data['content'])
		#form handling for project convos
		for form in projectMessageFormSet:
			if form.is_valid():
				content = form.cleaned_data['content']
				recipientProject = m.Project.objects.get(title=form.cleaned_data['recipient'])
				if recipientProject:
					m.Messages_from_user_to_project.newMessage(request.user, recipientProject, form.cleaned_data['content'])
					
		return redirect('messaging')		
	return render(request, 'demo/messaging.html', context)	
	
@verified_email_required 
@logged_in_setup_decorator
def new_project(request, context):
	if request.method=='GET':
		project_form=ProjectForm()
		pitch_form=ProjectPitchForm()
		context['project_form'] = project_form
		context['pitch_form'] = pitch_form
	else:
		project_form=ProjectForm(request.POST)
		context['project_form'] = project_form
		pitch_form=ProjectPitchForm(request.POST)
		context['pitch_form'] = pitch_form
		
		if project_form.is_valid() and pitch_form.is_valid():
			if m.Project.newProject(pitch_form.cleaned_data['description'], pitch_form.cleaned_data['solution'], pitch_form.cleaned_data['industry'], pitch_form.cleaned_data['video'], project_form.cleaned_data['title'], request.user):
				project_name = project_form.cleaned_data['title']
				linkTo = reverse('project_filter')
				content = "<a href='" + linkTo + "'>" + str(request.user.first_name) + " " + str(request.user.last_name) + " created a new project, " + project_name + "</a>"
				m.FeedPosts.postToEveryone(content)
				return redirect('startups')
			
		context['error'] = "Could not create startup, make sure form is valid and title is not taken."
	
	return render(request, 'demo/new_project.html', context)
	
@verified_email_required 
@logged_in_setup_decorator
def startups(request, context):

	if request.method == 'POST':
	
	
		quit_form=LeaveProjectForm(request.POST)
		if quit_form.is_valid():
			project = m.Project.objects.get(title=quit_form.cleaned_data['project_to_leave'])
			project.remove(request.user)
			return redirect('startups')
	
		invite_form=AcceptProjectInviteForm(request.POST)
		if invite_form.is_valid():
			project = m.Project.objects.get(title=invite_form.cleaned_data['project'])
			if m.ProjectInvite.getInvite(project, request.user) is not None:
			
				
				m.ProjectInvite.deleteInvite(project, request.user)
				m.Project.addMember(project.title, request.user.email)
			
				linkTo = reverse('team_profile', kwargs={'project_name': invite_form.cleaned_data['project']})
				content = "<a href='" + linkTo + "'>" + "Added " + str(request.user.first_name) + " " + str(request.user.last_name) + " to " + invite_form.cleaned_data['project'] + "</a>"
				m.Notifications.notifyTeam(project, content, linkTo)
				
				
				#m.ProjectPosts.postProject(project, content)
				
				context['success'] = "Successfully joined team"
			else:
				context['error'] = "No invite found"
		
			
		else:
			
			context['error'] = "Could not accept invite"
			
	project_ids = m.Project_members.objects.filter(user_id=request.user)
	
	projects = []
	project_quit_forms=[]
	for id in project_ids:
		projects.append(id.project_id)
		project_quit_forms.append(LeaveProjectForm(initial={'project_to_leave' : id.project_id.title}))
			
	invites = m.ProjectInvite.objects.filter(user_id=request.user)
	
	context['projects'] = [list(x) for x in zip(projects, project_quit_forms)]
	
	
	forms = []
	for invite in invites:
		forms.append(AcceptProjectInviteForm(initial={'project' : invite.project_id.title}))
			
	context['invites'] = [list(x) for x in zip(invites, forms)]


	
	return render(request, 'demo/startups.html', context)
	
	
@verified_email_required 
@logged_in_setup_decorator
def project_filter(request, context):
	return render(request, 'demo/project_filter.html', context)
	
	
@verified_email_required 
@logged_in_setup_decorator
@message_modal_decorator
def project_list(request, filter, context):

	if request.method == 'POST':
		message_form=ModalMessageForm(request.POST)
		
		if message_form.is_valid():
			target = message_form.cleaned_data['recipient']
			content = message_form.cleaned_data['content']
			
			targetProject = m.Project.objects.get(title=target)
			
			m.Messages_from_user_to_project.newMessage(request.user, targetProject, content)
			
			return redirect('project_filter')
		else:
			context['error'] = "No such recipient"

	projects = m.Project.objects.filter()
	project_leaders = []
	for leader in projects:
		project_leaders.append(leader.getLeader())
	
	all_projects = [list(x) for x in zip(projects, project_leaders)]
	
	filter = filter.upper()
	
	if filter == '*':
		filtered_projects = all_projects
	else:
		filtered_projects = []
		for project in all_projects:
			if filter in project[0].title.upper():
				filtered_projects.append(project)
				continue
				
			if filter in project[0].pitch_id.industry.upper():
				filtered_projects.append(project)
				continue
			
			

	context['projects'] = filtered_projects
	
	return render(request, 'demo/project_list.html', context)
	

@verified_email_required 
@logged_in_setup_decorator
def new_profile(request, context):
	return render(request, 'demo/new_profile.html', context)
	
@verified_email_required 
@logged_in_setup_decorator
def profile(request, context):
	user = request.user
	profile = user.profile
	context['profile'] = profile

	return render(request, 'demo/profile.html', context)
	
@verified_email_required 
@logged_in_setup_decorator
def profile_edit(request, context):

	if request.method == 'POST':
		profile_form = UserProfileForm(request.POST, instance=request.user.profile)
		user_form = UserForm(request.POST, instance=request.user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('profile')
	else:
		user = request.user
		profile = user.profile
		user_form = UserForm(instance=user)
		profile_form = UserProfileForm(instance=profile)
		
	context['user_form'] = user_form
	context['profile_form'] = profile_form

	return render(request, 'account/profile_edit.html', context)

@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
@business_model_decorator
def businessModel(request, project_name, canvas_id, context):

	NotesFormSet = inlineformset_factory(Business_model, Business_model_notes, form = business_model_noteForm, extra=1)
	
	canvasID = context['canvasId']
	
	print(context['business_model'][canvasID].business_model_name)
	
	
	if request.method=='POST':
		businessModels = [(x, context['business_model'][x].business_model_name or x) for x in range(len(context['business_model']))]
		businessModels.insert(0, businessModels.pop(canvasID))
		selectForm = BusinessModelSelectForm(request.POST,businessModels=businessModels)
		if selectForm.is_valid():
			return redirect('businessModel', project_name, selectForm.businessModel()[1])
		
		newCanvasForm = BusinessModelCreateForm(request.POST)
		if newCanvasForm.is_valid():
			newCanvas = context['project'].addCanvas(newCanvasForm.cleaned_data['business_model_name'])
			
			notes = m.Business_model_notes.getAllBusiness_model_notes(context['business_model'][canvasID])
			for note in notes:
				m.Business_model_notes.newBusiness_model_note(newCanvas, note.table, note.title, note.description, note.color, note.order)
			
			return redirect('businessModel', project_name, -1)
			
		formset = NotesFormSet(request.POST, instance=context['business_model'][canvasID])
		context['formset'] = formset
		
		if formset.is_valid():
			editedNotes = formset.save(commit=False)
			for editedNote in editedNotes:
				editedNote.business_model_id = context['business_model'][canvasID]
				editedNote.save()
			return redirect('businessModel', project_name, canvasID)
			
		else:
			formset = NotesFormSet(instance=context['business_model'][canvasID])
			context['formset'] = formset
			context['error'] = "Could not create or edit note"
		
	else:
		formset = NotesFormSet(instance=context['business_model'][canvasID])
		context['formset'] = formset
		
		
	businessModels = [(x, context['business_model'][x].business_model_name or x) for x in range(len(context['business_model']))]
	businessModels.insert(0, businessModels.pop(canvasID))
	context['selectForm'] = BusinessModelSelectForm(businessModels=businessModels)
	
	context['canvasName'] = context['business_model'][canvasID].business_model_name
	context['newModelForm'] = BusinessModelCreateForm()
	
	
	return render(request, 'demo/businessmodel.html', context)

@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def project(request, project_name, context):
	context['ProjectPosts'] = m.ProjectPosts.objects.filter(project_id=context['project'])
	return render(request, 'demo/project.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def project_pitch(request, project_name, context):
	
	project_pitch = context['project'].pitch_id
	context['project_pitch'] = project_pitch
	
	if request.method=='GET':
		pitch_form=ProjectPitchForm(instance=project_pitch)
	else:
		pitch_form=ProjectPitchForm(request.POST, instance=project_pitch)
		
		if pitch_form.is_valid():
			linkTo = reverse('project_pitch', kwargs={'project_name': project_name})
			content = "<a href='" + linkTo + "'>" + "Project pitch changed for " + project_name + "</a>"
			m.Notifications.notifyTeam(context['project'], content, linkTo)
			context['project'].newPost(content)
			pitch_form.save()
	
	context['pitch_form'] = pitch_form
				
	return render(request, 'demo/project_pitch.html', context)

#helper function to get teammates and their profiles in a tuple list
def getTeammateProfilesFromProject(project_id):
	teammates = m.Project_members.getTeamMembers(project_id)
	
	profiles = []
	for teammate in teammates:
		profiles.append(teammate.profile)
	
	return [list(x) for x in zip(teammates, profiles)]

@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def team_profile(request, project_name, context):	
	context['teammates'] = getTeammateProfilesFromProject(context['project'])
	return render(request, 'demo/team_profile.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
@message_modal_decorator
def recruit_team(request, project_name, context):

	teammates = m.Project_members.getTeamMembers(context['project'])

	if request.method == 'POST':
	
		project_form=InviteToProjectForm(request.POST)
		
		if project_form.is_valid():
			email = project_form.cleaned_data['email']
			user = m.User.objects.get(email=email)
			
			m.ProjectInvite.invite(context['project'], user)	
			
			linkTo = reverse('startups')
			content = "<a href='" + linkTo + "'>" + "Invited to " + project_name + "</a>"
			m.Notifications.notify(user, content, linkTo)	

			linkTo = reverse('project', kwargs={'project_name': project_name})
			teamContent = "<a href='" + linkTo + "'>" + "Invited " + user.first_name + " " + user.last_name + " to " + project_name + "</a>"
			m.Notifications.notifyTeam(context['project'], teamContent, linkTo)

			context['project'].newPost(teamContent)
			return redirect('team_profile', project_name)
			
		
		message_form=ModalMessageForm(request.POST)
		
		if message_form.is_valid():
			target = message_form.cleaned_data['recipient']
			content = message_form.cleaned_data['content']
			
			targetUser = m.User.objects.get(username=target)
			
			m.Messages_from_project_to_user.newMessage(context['project'], targetUser, content)
			
			return redirect('recruit_team', project_name)
			
		
		
	else:
		users = m.User.objects.all()
		
		profiles = []
		forms = []
		notInTeam = []
		for user in users:
			if user in teammates:
				continue
			profiles.append(user.profile)
			forms.append(InviteToProjectForm(initial={'email' : user.email}))
			notInTeam.append(user)
			
		context['potentials'] = [list(x) for x in zip(notInTeam, profiles, forms)]
	
	return render(request, 'demo/recruit_team.html', context)
	
@verified_email_required
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
@user_messages_for_project_decorator
@project_messages_for_project_decorator
def project_messaging(request, project_name, context):
	if request.method == 'GET':
		message_form = MessageForm()
		context['message_form'] = message_form
	else: #post
		message_form = MessageForm(request.POST)
		context['message_form'] = message_form
		userMessageFormSet = context['userMessageFormSetFactory'](request.POST, prefix='users')
		projectMessageFormSet = context['projectMessageFormSetFactory'](request.POST, prefix='projects')
		if message_form.is_valid():
			if message_form.cleaned_data['recipient_type'] == 'User':
				recipientUser = User.objects.get(username=message_form.cleaned_data['recipient'])
				if recipientUser:
					m.Messages_from_project_to_user.newMessage(context['project'], recipientUser, message_form.cleaned_data['content'])
					return redirect('project_messaging', project_name)
			else: #project
				recipientProject = m.Project.objects.get(title=message_form.cleaned_data['recipient'])
				if recipientProject:
					m.Messages_from_project_to_project.newMessage(context['project'], recipientProject, message_form.cleaned_data['content']) 
					return redirect('project_messaging', project_name)
		else:
			context['error'] = "Could not find recipient"			
		#form handling for user convos
		for form in userMessageFormSet:
			if form.is_valid():
				content = form.cleaned_data['content']
				recipientUser = User.objects.get(username=form.cleaned_data['recipient'])
				if recipientUser:
					m.Messages_from_project_to_user.newMessage(context['project'], recipientUser, form.cleaned_data['content'])
		#form handling for project convos
		for form in projectMessageFormSet:
			if form.is_valid():
				content = form.cleaned_data['content']
				recipientProject = m.Project.objects.get(title=form.cleaned_data['recipient'])
				if recipientProject:
					m.Messages_from_project_to_project.newMessage(context['project'], recipientProject, form.cleaned_data['content'])
					
		return redirect('project_messaging', project_name)

	return render(request, 'demo/project_messaging.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
@milestones_decorator
def businessPlan(request, project_name, context):

	MilestoneFormSet = inlineformset_factory(m.Project, m.Milestone, form=MilestoneForm, extra=1)
	
	if request.method=='POST':
		file_form = UploadFileForm(request.POST, request.FILES)
		context['file_upload'] = file_form
		formset = MilestoneFormSet(request.POST, instance=context['project'])
		context['formset'] = formset
		
		if file_form.is_valid():
			uploaded_file = UploadedFile(uploaded = request.FILES['file'])
			#not a transaction but it should be
			uploaded_file.save()
			
			context['project'].addProjection(uploaded_file)
			#transaction end
			return redirect('businessPlan', project_name)	
		else:
			context['error'] = "Could not upload projections file"
		
		if formset.is_valid():
			linkTo = reverse('businessPlan', kwargs={'project_name': project_name})
			content = "<a href='" + linkTo + "'>" + "Milestone(s) changed for " + project_name + "</a>"
			m.Notifications.notifyTeam(context['project'], content, linkTo)
			
			context['project'].newPost(content)
			#m.ProjectPosts.postProject(context['project'], content)
			
			editedMilestones = formset.save(commit=False)
			for editedMilestone in editedMilestones:
				editedMilestone.project_id = context['project']
				editedMilestone.save()
			return redirect('businessPlan', project_name)	
		else:
			context['error'] = "Could not save milestones"
		
	else:
		file_form=UploadFileForm()
		context['file_upload'] = file_form
		
		formset = MilestoneFormSet(instance=context['project'])
		context['formset'] = formset
		

		
	context['uploaded_projections'] = context['project'].getProjections()
	
	return render(request, 'demo/businessplan.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def ecosystem(request, project_name, context):
	return render(request, 'demo/ecosystem.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
@business_model_decorator
def pitchCard(request, project_name, canvas_id, context):
	context['project_pitch'] = context['project'].pitch_id
	context['teammates'] = getTeammateProfilesFromProject(context['project'])
	return render(request, 'demo/pitchCard.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def mvp(request, project_name, context):
	project_pitch = context['project'].pitch_id
	context['project_pitch'] = project_pitch
	
	if request.method=='GET':
		video_form=ProjectVideoForm(instance=project_pitch)
	else:
		video_form=ProjectVideoForm(request.POST, instance=project_pitch)
		
		if video_form.is_valid():
			linkTo = reverse('project_pitch', kwargs={'project_name': project_name})
			content = "<a href='" + linkTo + "'>" + "Video presentation changed for " + project_name + "</a>"
			m.Notifications.notifyTeam(context['project'], content, linkTo)
			
			context['project'].newPost(content)
			#m.ProjectPosts.postProject(context['project'], content)
			video_form.save()
	
	context['video_form'] = video_form
	return render(request, 'demo/mvp.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def project_validation(request, project_name, context):

	if request.method == 'POST':
	
		summary_form = ValidationSummaryForm(request.POST)
		if summary_form.is_valid():
			context['project'].validation = summary_form.cleaned_data['validation']
			context['project'].save()
			redirect('project_validation', project_name)
	
		questionnaire_form = ProjectValidationForm(request.POST)
			
		if questionnaire_form.is_valid():
			questionnaire = ProjectValidation(questionaireURL=questionnaire_form.cleaned_data['questionaireURL'], questionaireSummary=questionnaire_form.cleaned_data['questionaireSummary'], project_id=context['project'])
			questionnaire.save()

			linkTo = reverse('project_validation', kwargs={'project_name': project_name})
			content = "<a href='" + linkTo + "'>" + "New questionnaire added for " + project_name + "</a>"
			m.Notifications.notifyTeam(context['project'], content, linkTo)
			
			
			#m.ProjectPosts.postProject(context['project'], content)
			redirect('project_validation', project_name)	
			
			
		file_questionnaire_form = ProjectFileValidationForm(request.POST, request.FILES)
		if file_questionnaire_form.is_valid():
			
			uploaded_file = UploadedFile(uploaded = request.FILES['file'])
			uploaded_file.save()
			
			context['project'].addFileValidation(uploaded_file, questionnaire_form.cleaned_data['questionaireSummary'])

			linkTo = reverse('project_validation', kwargs={'project_name': project_name})
			content = "<a href='" + linkTo + "'>" + "New validation added for " + project_name + "</a>"
			m.Notifications.notifyTeam(context['project'], content, linkTo)
			
			redirect('project_validation', project_name)	
			

	questionnaire_form = ProjectValidationForm()		
	file_questionnaire_form = ProjectFileValidationForm()
	
	context['questionnaire_form'] = questionnaire_form	
	context['file_questionnaire_form'] = file_questionnaire_form
	context['file_validations'] = context['project'].getFileValidations()
	context['validations'] = context['project'].getValidations()
	context['summary_form'] = ValidationSummaryForm(instance=context['project'])
	

	return render(request, 'demo/project_validation.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def investors(request, project_name, context):
	return render(request, 'demo/investors.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def services(request, project_name, context):
	return render(request, 'demo/services.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def resource_center(request, project_name, context):
	return render(request, 'demo/resource_center.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def ecosystem_projects(request, project_name, context):
	return render(request, 'demo/ecosystem_projects.html', context)
	
@verified_email_required 
@project_participant_decorator
@logged_in_setup_decorator
@project_setup_decorator
def ecosystem_experts(request, project_name, context):
	return render(request, 'demo/ecosystem_experts.html', context)