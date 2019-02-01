from django import template
from django.contrib.auth.models import Group,User

register = template.Library()

@register.filter(name='get_users')
def get_users(group_name, random): 
    users=list(User.objects.filter(groups__name=group_name))
    usernames=""
    for user in users:
    	usernames+=" "+user.username
    return usernames

@register.filter(name='get_groups')
def get_groups(user_name, random): 
    groups=list(User.objects.get(username=user_name).groups.all())
    groupnames=""
    for group in groups:
        groupnames+=" "+group.name
    return groupnames