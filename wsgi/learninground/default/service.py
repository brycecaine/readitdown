def create_user(email, role):
    username = email.split('@')[0]
    print 'u: %s' % username

    # create user with username
    # set attributes based on other fields ('role', etc)

def create_guardian(user, guardian_email):
    username = guardian_email.split('@')[0]
    print 'g: %s' % username

    # create user for parent
    # create association for student-parent
