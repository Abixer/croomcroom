from django.conf.urls import patterns, url

from demo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^about$', views.about, name='about'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^register$', views.register, name='register'),
    #url(r'^login$', views.login_view, name='login'),
	#url(r'^logout/$', views.logout_view, name='logout'),

	
	
	
	url(r'^messaging$', views.messaging, name='messaging'),
	url(r'^startups$', views.startups, name='startups'),
	
	url(r'^project_list/(?P<filter>.+)/$', views.project_list, name='project_list'),
	
	url(r'^project_filter$', views.project_filter, name='project_filter'),
	
	url(r'^new_profile$', views.new_profile, name='new_profile'),
	url(r'^profile$', views.profile, name='profile'),
	url(r'^profile_edit$', views.profile_edit, name='profile_edit'),
	url(r'^new_project$', views.new_project, name='new_project'),

	#Project team pages
	url(r'^project/(?P<project_name>.+)/team_profile$', views.team_profile, name='team_profile'),
	url(r'^project/(?P<project_name>.+)/recruit_team$', views.recruit_team, name='recruit_team'),
	
	#Project pages
	#url(r'^project/(?P<project_name>.+)/new_user_message/(?P<target>.+)$', views.project_messaging, name='project_messaging'),

	
	
	url(r'^project/(?P<project_name>.+)/messaging$', views.project_messaging, name='project_messaging'),
	url(r'^project/(?P<project_name>.+)/businessPlan$', views.businessPlan, name='businessPlan'),
	url(r'^project/(?P<project_name>.+)/ecosystem$', views.ecosystem, name='ecosystem'),
	
	url(r'^project/(?P<project_name>.+)/project_validation$', views.project_validation, name='project_validation'),	
	url(r'^project/(?P<project_name>.+)/mvp$', views.mvp, name='mvp'),
	url(r'^project/(?P<project_name>.+)/investors$', views.investors, name='investors'),
	url(r'^project/(?P<project_name>.+)/services$', views.services, name='services'),
	url(r'^project/(?P<project_name>.+)/resource_center$', views.resource_center, name='resource_center'),
	url(r'^project/(?P<project_name>.+)/ecosystem_projects$', views.ecosystem_projects, name='ecosystem_projects'),
	url(r'^project/(?P<project_name>.+)/ecosystem_experts$', views.ecosystem_experts, name='ecosystem_experts'),
	
	url(r'^project/(?P<project_name>.+)/pitchCard/(?P<canvas_id>.+)$', views.pitchCard, name='pitchCard'),
	url(r'^project/(?P<project_name>.+)/businessModel/(?P<canvas_id>.+)$', views.businessModel, name='businessModel'),
	
	url(r'^project/(?P<project_name>.+)/project_pitch$', views.project_pitch, name='project_pitch'),
	url(r'^project/(?P<project_name>.+)/', views.project, name='project'),

)

