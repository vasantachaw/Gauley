from MainApp import models
from MainApp.models import OrderPlaced

def dashboard(request):
    if request.user.is_authenticated:
        order=OrderPlaced.objects.count()
        admin = models.Customer.objects.filter(user=request.user)
        context = {
            'users': admin,
            'order':order
            
        }
        return context
    context = {
        'users': None,
        'order':None
    }
    return context
