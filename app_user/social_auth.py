__author__ = 'moon'

from models import UserAccount
from social.backends.facebook import FacebookOAuth2
from requests import request, HTTPError
from django.core.files.base import ContentFile


def user_account(strategy, details, response, user=None, *args, **kwargs):

    if user:
        if kwargs['is_new']:
            attrs = {'djgouser': user}
            if type(kwargs['backend']) is FacebookOAuth2:
                if response:
                    fb_data = {
                        'firstname':response[u'first_name'],
                        'lastname':response[u'last_name'],
                        'email':response[u'email'],
                    }
                    attrs = dict(attrs.items()+fb_data.items())
                UserAccount.objects.create(**attrs)
            else:
                pass

def save_profile(strategy,  response, details, user=None ,*args, **kwargs):
#add is new??
    if user:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try :
            response = request('GET', url, params={'type':'large'})
            response.raise_for_status()
        except HTTPError:
            pass

        else:
            _useraccount = UserAccount.objects.get(email=user.username)
            _useraccount.propic.save('{0}_facebook.jpg'.format(user.username),
                                     ContentFile(response.content))