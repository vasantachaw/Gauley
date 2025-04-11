from MainApp import models
from MainApp.models import OrderPlaced
from Authentication.models import User

def dashboard(request):
    if request.user.is_authenticated:
        order = OrderPlaced.objects.count()
        admin = models.Customer.objects.filter(user=request.user)
        customers_count = User.objects.filter(is_customer=True).count()
        context = {
            'users': admin,
            'order': order,
            'active_users': customers_count,

        }
        return context
    context = {
        'users': None,
        'order': None
    }
    return context
