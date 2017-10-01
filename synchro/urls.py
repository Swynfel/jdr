from django.conf.urls import url
from . import views, autocomplete

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^auth/signup/$', views.signup, name='signup'),
    url(r'^auth/signup/done/$', views.signupDone, name='signup-done'),
    url(r'^waiting/$', views.waiting, name='waiting'),

    url(r'^activity/$', views.activities, name='activity-all'),
    url(r'^activity/me/$', views.myActivities, name='activity-me'),
    url(r'^activity/me/organiser/$', views.myActivities, {'what':'organiser'}, name='activity-me-organiser'),
    url(r'^activity/me/player/$', views.myActivities, {'what':'player'}, name='activity-me-player'),

    url(r'^activity/new/$', views.editActivity, name='activity-new'),
    url(r'^activity/(?P<key>[0-9]+)/$', views.getActivity, name='activity-get'),
    url(r'^activity/(?P<key>[0-9]+)/edit/$', views.editActivity, name='activity-edit'),
    url(r'^activity/(?P<key>[0-9]+)/join/$', views.askActivity, {'what':'join'}, name='activity-join'),
    url(r'^activity/(?P<key>[0-9]+)/leave/$', views.askActivity, {'what':'leave'}, name='activity-leave'),

    url(r'^me/$', views.default, name='me'),

    # Autocomplete
    url(r'^autocomplete/tags/$',autocomplete.TagsAutocomplete.as_view(),name='autocomplete-tags'),
]
