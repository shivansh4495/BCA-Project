from django.shortcuts import render
from packetTrackingSystem.models import Live_Updates

# Create your views here.
def home(request):
    return render(request, 'homePage.html')


def OrderTracking(request):
    if request.method == 'POST':
        
        awbno = request.POST.get('awbno')
        
        updates = Live_Updates.objects.filter(AWBNO=awbno).order_by('-last_update_time')
        
        return render(request, 'OrderTracking.html', {'updates': updates, 'awbno': awbno})
    else:
        
        return render(request, 'HomePage.html')
