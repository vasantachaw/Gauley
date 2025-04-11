from Authentication.models import User

def active_users_no(request):
    customers_count = User.objects.filter(is_customer=True).count()
    context={'active_users':customers_count}
    return context