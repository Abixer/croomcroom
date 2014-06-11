from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from datetime import datetime
import demo.gist
import IMS.settings
import botocore.session

class S3FileManager():
	def push_file_to_s3(file):
		#print("Putting a file in s3 - initial parameters")

		bucket = IMS.settings.BUCKET_NAME # change this to your bucket name
		key = 'croomer_production' # a subfolder under the bucket
		filelocation = IMS.settings.MEDIA_ROOT + '/' + file.name # the file we will put into S3
		filename = file.name
		region = 'us-west-2' # change this to your region
		acl = 'public-read' # we are going to set the ACL to public-read so we can access the file via a url

		#print( ' region: ' + region)
		#print( ' bucket: ' + bucket)
		#print( 'key (subfolder): ' + key)
		#print( ' filename: ' + './' + filename)
		#print( ' acl: ' + acl)

		session = botocore.session.get_session()
		s3 = session.get_service('s3')
		operation = s3.get_operation('PutObject')
		endpoint = s3.get_endpoint(region)

		#print("uploading the file to s3")

		fp = open('./' + filelocation, 'rb')
		http_response, response_data = operation.call(endpoint,
												  bucket=bucket,
												  key=key + '/' + filename,
												  body=fp)
		#print (http_response)
		#print (response_data)
		#print("getting s3 object properties of file we just uploaded")
		operation = s3.get_operation('GetObjectAcl')
		http_response, response_data = operation.call(endpoint,
													  bucket=bucket,
													  key=key + '/' + filename)
		#print( http_response)
		#print( response_data)
		#print("setting the acl to public-read")
		operation = s3.get_operation('PutObjectAcl')
		http_response, response_data = operation.call(endpoint,
													  bucket=bucket,
													  key=key + '/' + filename,
													  acl=acl)
		#print( http_response)
		#print( response_data)
		#print("The url of the object is:")
		#print ('http://'+bucket+'.s3.amazonaws.com/'+ key + '/' + filename)
		return 'http://'+bucket+'.s3.amazonaws.com/'+ key + '/' + filename

		

class UploadedFile(models.Model):
	uploaded = models.FileField(upload_to='user_uploads/')	
	fileURL = models.CharField(max_length=500, blank=True, null=True)
	
	
	def save(self, *args, **kwargs):
		super(UploadedFile, self).save(*args, **kwargs)
		#So we save it locally then upload for maximum efficiency.
		url = S3FileManager.push_file_to_s3(self.uploaded)
		self.fileURL = url
		super(UploadedFile, self).save(*args, **kwargs)
	
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	
	city = models.CharField(max_length=45)
	province = models.CharField(max_length=45)
	country = models.CharField(max_length=45)
	school = models.CharField(max_length=45)
	faculty = models.CharField(max_length=45)
	program = models.CharField(max_length=45)
	yearofstudy = models.CharField(max_length=45)
	skills = models.CharField(max_length=500)
	interests = models.CharField(max_length=500, blank=True, null=True)
	birthday = models.DateTimeField(blank=True, null=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class ProjectValidation(models.Model):
	project_validation_id = models.AutoField(primary_key=True)
	questionaireURL = models.CharField(max_length=500)
	questionaireSummary = models.CharField(max_length=500)
	project_id = models.ForeignKey('Project')
	
	def getValidations(project):
		return ProjectValidation.objects.filter(project_id=project)

class ProjectFileValidation(models.Model):
	project_file_validation_id = models.AutoField(primary_key=True)
	file_id = models.ForeignKey('UploadedFile', blank=True, null=True)
	questionaireSummary = models.CharField(max_length=500)
	project_id = models.ForeignKey('Project')
	
	def getValidations(project):
		return ProjectFileValidation.objects.filter(project_id=project)
		
class Business_model(models.Model):
	business_model_id = models.AutoField(primary_key=True)
	project_id = models.ForeignKey('Project')
	
	business_model_name = models.CharField(max_length=100, blank=True, null=True)
	
	def newBusiness_model(project):
		business_model = Business_model.objects.create(project_id=project)
		return True
		
	def newBusiness_model(project, name):
		business_model = Business_model.objects.create(project_id=project, business_model_name=name)
		return True
		
	def getBusiness_model(project):
		return Business_model.objects.filter(project_id=project)

class Business_model_notes(models.Model):
	business_model_notes_id = models.AutoField(primary_key=True)
	business_model_id = models.ForeignKey('Business_model')
	table = models.CharField(max_length=45)
	title = models.CharField(max_length=300)
	description = models.CharField(max_length=300, blank=True, null=True)
	color = models.CharField(max_length=45)
	order = models.IntegerField(blank=True, null=True)
	
	def newBusiness_model_note(business_model, table, title, description, color, order):
		business_model_notes = Business_model_notes.objects.create(business_model_id=business_model, table=table, title=title, description=description, color=color, order=order)
		return True
	
	def getBusiness_model_notes(business_model, table):
		results = []
		business_model_notes = Business_model_notes.objects.filter(business_model_id=business_model, table=table)

		for business_model_note in business_model_notes:
			results.append(business_model_note)
		
		return results
		
	def getAllBusiness_model_notes(business_model):
		results = []
		business_model_notes = Business_model_notes.objects.filter(business_model_id=business_model)

		return business_model_notes
		
class Project_pitch(models.Model):
	pitch_id = models.AutoField(primary_key=True)
	description = models.CharField(max_length=500)
	solution = models.CharField(max_length=500)
	industry = models.CharField(max_length=45)
	video = models.CharField(max_length=500, blank=True, null=True)

class Uploaded_projections(models.Model):
	project_id = models.ForeignKey('Project')
	file_id = models.ForeignKey('UploadedFile', blank=True, null=True)
	
class Project(models.Model):
	project_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=45)
	pitch_id = models.ForeignKey('Project_pitch')
	start_date = models.DateTimeField()
	validation = models.CharField(max_length=2000, blank=True, null=True)
	
	def getProjections(self):
		return Uploaded_projections.objects.filter(project_id=self)
	
	def addProjection(self, projection):
		Uploaded_projections.objects.create(project_id=self, file_id=projection)
	
	
	def __str__(self):
		return str(self.project_id) + ": " +  str(self.title)
		
	def __repr__(self):
		return str(self)
	
	def newProject(description, solution, industry, video, title, user):		
		pitchEntry = Project_pitch.objects.create(description=description, solution=solution, industry=industry, video=video)
		start_date = datetime.utcnow().replace(tzinfo=utc)
		projectEntry = Project.objects.create(title=title.replace(" ","_"), start_date=start_date, pitch_id=pitchEntry)
		projectMember = Project_members.objects.create(user_id=user, project_id=projectEntry)
		business_model = Business_model.objects.create(project_id=projectEntry, business_model_name="initial")
		return True

	def addMember(title, email):
		member = User.objects.get(email=email)
		project = Project.objects.get(title=title)
		projectMember = Project_members.objects.create(user_id=member, project_id=project)
			
	def getTeamMembers(project):
		return Project_members.getTeamMembers(project)
		
	def getValidations(self):
		return ProjectValidation.getValidations(self)
		
	def getFileValidations(self):
		return ProjectFileValidation.getValidations(self)
		
	def addCanvas(self, name):
		business_model = Business_model.objects.create(project_id=self, business_model_name=name)
		return business_model
		
	def remove(self, user):
		results = Project_members.objects.filter(user_id=user, project_id=self).delete()
		
	def getLeader(self):
		leader = "None"
		if Project_members.getTeamMembers(self):
			leader = Project_members.getTeamMembers(self)[0]
		return leader
		
	def newPost(self, content):
		project_post = ProjectPosts.objects.create(project_id=self, content=content, timestamp=datetime.utcnow().replace(tzinfo=utc))
		
	def addFileValidation(self, file, summary):
		ProjectFileValidation.objects.create(file_id=file, questionaireSummary=summary, project_id=self)
		
	
class Project_members(models.Model):
	project_id = models.ForeignKey('Project')
	user_id = models.ForeignKey(User)
	
	def getTeamMembers(project):
		results = []
		project = Project_members.objects.filter(project_id=project)

		for member in project:
			results.append(member.user_id)
		
		return results	
		
class Messages_from_user_to_user(models.Model):
	message_id = models.AutoField(primary_key=True)
	user_id_from = models.ForeignKey(User, related_name='messages_from_user_to_user_user_id_from')
	user_id_to = models.ForeignKey(User, related_name='messages_from_user_to_user_user_id_to')
	content = models.CharField(max_length=500)
	unread = models.BooleanField()
	timestamp = models.DateTimeField()
	
	def __str__(self):
		return str(self.message_id) + ": " +  str(self.timestamp)
		
	def __repr__(self):
		return str(self)
	
	def newMessage(user_id_from, user_id_to, content):
		timenow = datetime.utcnow().replace(tzinfo=utc)
		message = Messages_from_user_to_user.objects.create(user_id_from=user_id_from, user_id_to=user_id_to, content=content, unread=True, timestamp=timenow)
		return message
	
	def getUnreadMessages(user_id):
		return Messages_from_user_to_user.objects.filter(unread=True).filter(user_id_to=user_id)
	
	def messagesRead(user_id):
		messages = Messages_from_user_to_user.getUnreadMessages(user_id)
		for message in messages:
			message.unread = False
			message.save()
	
	def getMessagesFromUser(user_id):
		messages = Messages_from_user_to_user.objects.filter(user_id_from=user_id).order_by('-timestamp') #minus means sort descending
		return messages
	
	def getMessagesToUser(user_id):
		messages = Messages_from_user_to_user.objects.filter(user_id_to=user_id).order_by('-timestamp') #minus means sort descending
		return messages

	
class Messages_from_user_to_project(models.Model):
	message_id = models.AutoField(primary_key=True)
	user_id_from = models.ForeignKey(User, related_name='messages_from_user_to_project_user_id_from')
	project_id_to = models.ForeignKey('Project', related_name='messages_from_user_to_project_project_id_to')
	content = models.CharField(max_length=500)
	unread = models.BooleanField()
	timestamp = models.DateTimeField() #need DateTime and not Date for more than daily precision
	
	def __str__(self):
		return str(self.message_id) + ": " +  str(self.timestamp.ctime())
		
	def __repr__(self):
		return str(self)
	
	def newMessage(user_id_from, project_id_to, content):
		timenow = datetime.utcnow().replace(tzinfo=utc)
		message = Messages_from_user_to_project.objects.create(user_id_from=user_id_from, project_id_to=project_id_to, content=content, unread=True, timestamp=timenow)
		return message
		
	def getUnreadMessages(project_id):
		return Messages_from_user_to_project.objects.filter(unread=True).filter(project_id_to=project_id)
		
	def messagesRead(project_id):
		messages = Messages_from_user_to_project.getUnreadMessages(project_id)
		for message in messages:
			message.unread = False
			message.save()
	
	def getMessagesFromUser(user_id):
		messages = Messages_from_user_to_project.objects.filter(user_id_from=user_id).order_by('-timestamp') #minus means sort descending
		return messages
	
	def getMessagesToProject(project_id):
		messages = Messages_from_user_to_project.objects.filter(project_id_to=project_id).order_by('-timestamp') #minus means sort descending
		return messages
	
class Messages_from_project_to_user(models.Model):
	message_id = models.AutoField(primary_key=True)
	project_id_from = models.ForeignKey('Project', related_name='messages_from_project_to_user_project_id_from')
	user_id_to = models.ForeignKey(User, related_name='messages_from_project_to_user_user_id_to')
	content = models.CharField(max_length=500)
	unread = models.BooleanField()
	timestamp = models.DateTimeField()
	
	def __str__(self):
		return str(self.message_id) + ": " +  str(self.timestamp)
		
	def __repr__(self):
		return str(self)
	
	def newMessage(project_id_from, user_id_to, content):
		timenow = datetime.utcnow().replace(tzinfo=utc)
		message = Messages_from_project_to_user.objects.create(project_id_from=project_id_from, user_id_to=user_id_to, content=content, unread=True, timestamp=timenow)
		return message
		
	def getUnreadMessages(user_id):
		return Messages_from_project_to_user.objects.filter(unread=True).filter(user_id_to=user_id)
		
	def messagesRead(user_id):
		messages = Messages_from_project_to_user.getUnreadMessages(user_id)
		for message in messages:
			message.unread = False
			message.save()
	
	def getMessagesFromProject(project_id):
		messages = Messages_from_project_to_user.objects.filter(project_id_from=project_id).order_by('-timestamp') #minus means sort descending
		return messages
	
	def getMessagesToUser(user_id):
		messages = Messages_from_project_to_user.objects.filter(user_id_to=user_id).order_by('-timestamp') #minus means sort descending
		return messages
	
class Messages_from_project_to_project(models.Model):
	message_id = models.AutoField(primary_key=True)
	project_id_from = models.ForeignKey('Project', related_name='messages_from_project_to_project_project_id_from')
	project_id_to = models.ForeignKey('Project', related_name='messages_from_project_to_project_project_id_to')
	content = models.CharField(max_length=500)
	unread = models.BooleanField()
	timestamp = models.DateTimeField()
	
	def __str__(self):
		return str(self.message_id) + ": " +  str(self.timestamp)
		
	def __repr__(self):
		return str(self)
	
	def newMessage(project_id_from, project_id_to, content):
		timenow = datetime.utcnow().replace(tzinfo=utc)
		message = Messages_from_project_to_project.objects.create(project_id_from=project_id_from, project_id_to=project_id_to, content=content, unread=True, timestamp=timenow)
		return message
		
	def getUnreadMessages(project_id):
		return Messages_from_project_to_project.objects.filter(unread=True).filter(project_id_to=project_id)
		
	def messagesRead(project_id):
		messages = Messages_from_project_to_project.getUnreadMessages(project_id)
		for message in messages:
			message.unread = False
			message.save()
	
	def getMessagesFromProject(project_id):
		messages = Messages_from_project_to_project.objects.filter(project_id_from=project_id).order_by('-timestamp') #minus means sort descending
		return messages
	
	def getMessagesToProject(project_id):
		messages = Messages_from_project_to_project.objects.filter(project_id_to=project_id).order_by('-timestamp') #minus means sort descending
		return messages

class Milestone(models.Model):
	milestone_id = models.AutoField(primary_key=True)
	project_id = models.ForeignKey('Project')
	content = models.CharField(max_length=500)
	due_date = models.DateTimeField()
	
	def newMilestone(content, due_date, project):
		milestone_entry = Milestone.objects.create(content=content, project_id=project, due_date=due_date, projections=projections)
		return True
		
	def getProjectMilestones(project):
		milestones = Milestone.objects.filter(project_id=project).order_by('due_date') #ascending order	
		return milestones
	
class FeedPosts(models.Model):
	post_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User)
	content = models.CharField(max_length=500)
	timestamp = models.DateTimeField()
	
	def postUser(user, content):
		feed_post = FeedPosts.objects.create(user_id=user, content=content, timestamp=datetime.utcnow().replace(tzinfo=utc))
		
	def postTeam(project, content):
		teammates = Project_members.getTeamMembers(project)
		for teammate in teammates:
			FeedPosts.postUser(teammate, content)

	def postToEveryone(content):
		users = User.objects.all()
		for user in users:
			FeedPosts.postUser(user, content)

class ProjectPosts(models.Model):
	post_id = models.AutoField(primary_key=True)
	project_id = models.ForeignKey(Project)
	content = models.CharField(max_length=500)
	timestamp = models.DateTimeField()

	

class Notifications(models.Model):
	notification_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User)
	content = models.CharField(max_length=500)
	urlToRemove = models.CharField(max_length=500)
	hasSeen = models.BooleanField()
	
	timestamp = models.DateTimeField()
	
	def notify(user, content, url):
		notification_entry = Notifications.objects.create(user_id=user, content=content, timestamp=datetime.utcnow().replace(tzinfo=utc), urlToRemove=url, hasSeen=False)
		
	def notifyTeam(project, content, url):
		teammates = Project_members.getTeamMembers(project)
		for teammate in teammates:
			Notifications.notify(teammate, content, url)
		
class ProjectInvite(models.Model):
	invite_id = models.AutoField(primary_key=True)
	project_id = models.ForeignKey(Project)
	user_id = models.ForeignKey(User)
	
	def invite(project, email):
		invite_entry = ProjectInvite.objects.create(project_id=project, user_id=email)
		
	def getInvite(project, user):
		return ProjectInvite.objects.filter(user_id=user, project_id=project)
		
	def deleteInvite(project, user):
		return ProjectInvite.objects.filter(user_id=user, project_id=project).delete()
		
	
class Spectators(models.Model):
	user_id = models.ForeignKey(User)