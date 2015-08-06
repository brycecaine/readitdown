from main.models import Friendship

def create_friendship(user, friend, active, friend_type):
    friendship = None
    if friend:
        friendship, created = Friendship.objects.get_or_create(user=user,
            friend=friend, friend_type=friend_type, active=True)

    return friendship
