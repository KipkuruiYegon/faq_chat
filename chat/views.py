from django.shortcuts import render

# Create your views here.
def home(request):
    if request.method == 'POST':
        user = request.user
        form_data = request.POST

        # Extract form data
        shipping_name = form_data['name']
    return render(request, 'index.html')