from .models import Mentorship

def validate_token(token):
    return Mentorship.objects.filter(token=token).first()
  