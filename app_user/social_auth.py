__author__ = 'moon'
from datetime import datetime
import pytz
from models import UserProfile
from social.backends.facebook import FacebookOAuth2
from requests import request, HTTPError
from django.core.files.base import ContentFile
import logging
logger = logging.getLogger(__name__)

def user_account(strategy, details, response, user=None, *args, **kwargs):

    if user:
        logger.debug(user)
        attrs = {'djgouser': user}
        if type(kwargs['backend']) is FacebookOAuth2:
            _profile, is_new = UserProfile.objects.get_or_create(**attrs)
            _profile.save()
        else:
            pass

def save_propic(strategy,  response, details, user=None ,*args, **kwargs):

    if user:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        _profile = UserProfile.objects.get(djgouser=user)
        if kwargs['is_new'] or kwargs['new_association']:
            try :
                responsepic = request('GET', url, params={'type':'large'})
                responsepic.raise_for_status()
            except HTTPError:
                pass
            else:
                _profile.propic.save('{0}_facebook.jpg'.format(user.username),
                                         ContentFile(responsepic.content))

        FB_unitime= response.get(u'updated_time')
        FB_uptime=datetime.strptime(FB_unitime, "%Y-%m-%dT%H:%M:%S+%f")

        utc=pytz.UTC
        FB_uptime = utc.localize(FB_uptime)

        #repeat part need try modulation
        #profile pic sync
        if _profile and _profile.updated_at < FB_uptime:
            try :
                responsepic = request('GET', url, params={'type':'large'})
                responsepic.raise_for_status()
            except HTTPError:
                pass
            else:
                _profile.propic.save('{0}_facebook.jpg'.format(user.username),
                                         ContentFile(responsepic.content))
