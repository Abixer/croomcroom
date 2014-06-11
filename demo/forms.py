from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from demo.models import *
from django.forms.extras.widgets import SelectDateWidget

MESSAGE_RECIPIENT_TYPE = (('User', 'User'), ('Project', 'Project'))

class SignupForm(forms.Form):	
	first_name = forms.CharField(required=True, max_length=30, label='First name')
	last_name = forms.CharField(required=True, max_length=30, label='Last name')
	#city = forms.CharField(required=True, max_length=30, label='city')
	
	#Will add all user profile fields soon
	
	def save(self, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()
		
		#profile = user.profile
		#profile.city = self.cleaned_data['city']
		#profile.save()
		
class InviteToProjectForm(forms.Form):	
	email = forms.CharField(widget=forms.HiddenInput())

class AcceptProjectInviteForm(forms.Form):
	project = forms.CharField(widget=forms.HiddenInput())
	
class NotificationForm(forms.Form):
	notification = forms.CharField(widget=forms.HiddenInput())

class UserProfileForm(forms.ModelForm):

	PROVINCE_CHOICES = (('',''),('Ontario', 'Ontario'), ('Quebec', 'Quebec'))
	COUNTRY_CHOICES = (('',''),('Canada', 'Canada'), ('USA', 'USA'))
	SCHOOL_CHOICES = (('',''),('uOttawa', 'uOttawa'), ('Carleton', 'Carleton'), ('UQO', 'UQO'))
	STUDY_CHOICES = (('',''),('First Year Undergraduate', 'First Year Undergraduate'), ('Second Year Undergraduate', 'Second Year Undergraduate'), ('Third Year Undergraduate', 'Third Year Undergraduate'), ('Fourth Year Undergraduate', 'Fourth Year Undergraduate'), ('Masters Degree', 'Masters Degree'), ('PhD Candidate', 'PhD Candidate'))

	
	city = forms.CharField(max_length = 45,required=False, label="City", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
	province = forms.CharField(max_length=45, required=False, label="Province", widget=forms.Select(attrs={'class':'form-control'}, choices=PROVINCE_CHOICES))
	country = forms.CharField(max_length=45, required=False, label="Country", widget=forms.Select(attrs={'class':'form-control'}, choices=COUNTRY_CHOICES))
	school = forms.CharField(max_length=45, required=False, label="School", widget=forms.Select(attrs={'class':'form-control'}, choices=SCHOOL_CHOICES))
	faculty = forms.CharField(max_length = 45,required=False, label="Faculty", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Faculty'}))
	program = forms.CharField(max_length = 45,required=False, label="Program", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Program'}))
	yearofstudy = forms.CharField(max_length=45, required=False, label="Year Of Study", widget=forms.Select(attrs={'class':'form-control'}, choices=STUDY_CHOICES))
	birthday = forms.DateField(required=False, label="Birthday", widget=SelectDateWidget(years = range(2020, 1900, -1)))
	skills = forms.CharField(max_length = 500,required=False, label="Skills", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'List of skills'}))
	interests = forms.CharField(max_length = 500,required=False, label="Interests", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'List of interests'}))
	

	class Meta:
		model = UserProfile
		fields = ['birthday', 'city', 'province', 'country', 'school', 'faculty', 'program', 'yearofstudy', 'skills', 'interests']
		
class UserForm(forms.ModelForm):
	first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	class Meta:
		model = User
		fields = ['first_name', 'last_name']
		
class ProjectValidationForm(forms.ModelForm):
	questionaireURL = forms.CharField(label="", widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Questionaire URL', 'maxlength':500}))
	questionaireSummary = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Summary', 'rows': 5, 'maxlength':500}))
	
	class Meta:
		model = ProjectValidation
		fields = ['questionaireURL', 'questionaireSummary']
		
class ProjectFileValidationForm(forms.Form):
	file = forms.FileField(label='File')
	questionaireSummary = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Summary', 'rows': 5, 'maxlength':500}))
	
class ProjectForm(forms.ModelForm):
	title = forms.CharField(label="Project Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Project Title', 'maxlength':45}))
	
	def is_valid(self):
		valid = super(ProjectForm, self).is_valid()
		if not valid:
			return valid
			
		try:
			project = Project.objects.get(title=self.cleaned_data['title'])
		except Project.DoesNotExist:
			return True
				
		return False
	
	class Meta:
		model = Project
		fields = ['title']
		
class ProjectPitchForm(forms.ModelForm):
	description = forms.CharField(label="Problem Description", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description', 'rows': 5, 'maxlength':500}))
	solution = forms.CharField(label="Solution", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Solution', 'rows': 5, 'maxlength':500}))
	industry = forms.CharField(label="Industry", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Industry', 'maxlength':45}))
	video = forms.CharField(required=False, label="Video Presentation", widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Video Presentation', 'maxlength':500}))
	class Meta:
		model = Project_pitch
		fields = ['industry', 'video', 'description','solution']
		
class ProjectVideoForm(forms.ModelForm):
	video = forms.CharField(label="", widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Video Presentation', 'maxlength':500}))
	class Meta:
		model = Project_pitch
		fields = ['video']
		
class MilestoneForm(forms.ModelForm):
	content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Milestone', 'rows': 5, 'maxlength':500}))
	due_date = forms.DateField(label="Due Date", widget=SelectDateWidget())
	class Meta:
		model = Milestone
		fields = ['content','due_date']
		
class ModalMessageForm(forms.Form):
	recipient = forms.CharField(label="Recipient", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username or Project', 'id':'recipient'})) 
	content = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'(500 or less characters)', 'maxlength':500}))
	
	def is_valid(self):
		valid = super(ModalMessageForm, self).is_valid()
		if not valid:
			return valid
		try:
			user = User.objects.get(username=self.cleaned_data['recipient'])
		except User.DoesNotExist:
			try:
				project = Project.objects.get(title=self.cleaned_data['recipient'])
			except Project.DoesNotExist:
				return False
		return True
		
class MessageForm(forms.Form):
	recipient_type = forms.ChoiceField(widget=forms.RadioSelect, choices=MESSAGE_RECIPIENT_TYPE)
	recipient = forms.CharField(label="Recipient", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username or Project'})) 
	content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'(500 or less characters)', 'maxlength':500}))
	
	def is_valid(self):
		valid = super(MessageForm, self).is_valid()
		if not valid:
			return valid
			
		#Check recipient
		try:
			user = User.objects.get(username=self.cleaned_data['recipient'])
		except User.DoesNotExist:
			try:
				project = Project.objects.get(title=self.cleaned_data['recipient'])
			except Project.DoesNotExist:
				return False
				
		return True
	
class MessageConvoForm(forms.Form):
	recipient = forms.CharField(label="Recipient", widget=forms.HiddenInput()) 
	content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'(500 or less characters)'}))

class business_model_noteForm(forms.ModelForm):
	COLOR_CHOICES = (('', 'White'),('info', 'Blue'), ('success', 'Green'),('warning', 'Orange'),('danger', 'Red'))
	title = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description', 'rows': 4, 'maxlength':300}))
	#description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description', 'rows': 4}))
	color = forms.CharField(required=False, widget=forms.Select(attrs={'class':'form-control'}, choices=COLOR_CHOICES))
	table = forms.CharField(widget=forms.HiddenInput())
	order = forms.IntegerField(required=False, widget=forms.HiddenInput(), initial=1)
	
	class Meta:
		model = Business_model_notes
		#fields = ['title', 'description','color', 'table', 'order']
		fields = ['title','color', 'table', 'order']
		
class UploadFileForm(forms.Form):
	file = forms.FileField(label='File')
	
#Pretty cool technique
class BusinessModelSelectForm(forms.Form):
	def __init__(self, *args, **kwargs):
		businessModels = kwargs.pop('businessModels')
		super(BusinessModelSelectForm, self).__init__(*args, **kwargs)
		self.fields['businessModels'] = forms.ChoiceField(choices=businessModels, label="Canvas:")
		
	def businessModel(self):
		for name, value in self.cleaned_data.items():
			if name == 'businessModels':
				return (self.fields[name].label, value)
				
class BusinessModelCreateForm(forms.ModelForm):
	business_model_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title', 'maxlength':100}))
	class Meta:
		model = Business_model
		fields = ['business_model_name']
		
class LeaveProjectForm(forms.Form):
	project_to_leave = forms.CharField(widget=forms.HiddenInput())
	
class ValidationSummaryForm(forms.ModelForm):
	validation = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Validations done so far', 'rows': 4, 'maxlength':2000}))
	class Meta:
		model = Project
		fields = ['validation']
