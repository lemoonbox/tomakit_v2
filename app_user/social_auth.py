__author__ = 'moon'
from datetime import datetime
import pytz
from models import UserProfile
from social.backends.facebook import FacebookOAuth2
from requests import request, HTTPError
from django.core.files.base import ContentFile


def user_account(strategy, details, response, user=None, *args, **kwargs):

    if user and kwargs['is_new']:
        attrs = {'djgouser': user}
        if type(kwargs['backend']) is FacebookOAuth2:
            _profile = UserProfile.objects.create(**attrs)
            _profile.save()
        else:
            pass

def save_propic(strategy,  response, details, user=None ,*args, **kwargs):

    if user:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        _profile = UserProfile.objects.get(djgouser=user)
        if kwargs['is_new']:
            try :
                response = request('GET', url, params={'type':'large'})
                response.raise_for_status()
            except HTTPError:
                pass
            else:
                _profile.propic.save('{0}_facebook.jpg'.format(user.username),
                                         ContentFile(response.content))

        FB_unitime= response[u'updated_time']
        FB_uptime=datetime.strptime(FB_unitime, "%Y-%m-%dT%H:%M:%S+%f")

        utc=pytz.UTC
        FB_uptime = utc.localize(FB_uptime)

        #repeat part need try modulation
        #profile pic sync
        if _profile and _profile.updated_at < FB_uptime:
            try :
                response = request('GET', url, params={'type':'large'})
                response.raise_for_status()
            except HTTPError:
                pass
            else:
                _profile.propic.save('{0}_facebook.jpg'.format(user.username),
                                         ContentFile(response.content))
