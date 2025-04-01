from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="hello world")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user' : request.user
            }
            return render(request,'chat\partials\chat_message_p.html',context)
    
    return render(request, 'chat.html', {'chat_messages': chat_messages, 'form':form})

def home(request):
    return render(request, 'chat.html')
