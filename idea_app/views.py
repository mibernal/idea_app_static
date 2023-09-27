from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordResetForm  # Importa PasswordResetForm correctamente
from .models import Idea
from .forms import IdeaForm
from django.http import HttpResponse

def idea_list(request):
    ideas = Idea.objects.all()
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'ideas/idea_detail.html', {'idea': idea})

@login_required
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_form.html', {'form': form})

@login_required
def idea_edit(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    # Verificar si el usuario actual es el propietario de la idea
    if request.user != idea.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'ideas/idea_form.html', {'form': form})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    # Check if the current user has permission to delete this idea
    if request.user != idea.user:
        raise PermissionDenied

    if request.method == 'POST':
        idea.delete()
        return redirect('idea_list')
    return render(request, 'ideas/idea_confirm_delete.html', {'idea': idea})

def home(request):
    ideas = Idea.objects.all()
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})

def about_view(request):
    return render(request, 'about.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('idea_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('idea_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Password Reset Views

def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                # Generate and send the password reset email
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                mail_subject = _('Password reset for your account')
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'protocol': 'https' if request.is_secure() else 'http',
                })
                email = EmailMessage(mail_subject, message, to=[email])
                email.send()
                return HttpResponse(_('Password reset email sent. Check your email for further instructions.'))
    else:
        form = PasswordResetForm()  # Debes definir "form" aquí si el método no es POST
    return render(request, 'registration/password_reset_form.html', {'form': form})


def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Handle password reset form submission here
            # Example:
            # form = YourCustomPasswordResetForm(request.POST)
            # if form.is_valid():
            #     new_password = form.cleaned_data.get('new_password')
            #     user.set_password(new_password)
            #     user.save()
            return HttpResponse(_('Password reset successful. You can now log in with your new password.'))
        else:
            # Render your custom password reset form here
            # Example:
            # form = YourCustomPasswordResetForm()
            return render(request, 'registration/password_reset_confirm.html', {'form': forms})
    else:
        return HttpResponse(_('Password reset link is invalid or has expired.'))

def user_profile(request):
    # Aquí puedes agregar la lógica para mostrar la página de inicio del usuario
    # Puedes obtener datos del usuario actual usando 'request.user'
    
    # Ejemplo de obtención de datos del usuario actual
    user = request.user
    user_info = {
        'username': user.username,
        'email': user.email,
        # Agrega otros campos del usuario que desees mostrar en el perfil
    }
    
    # Renderiza la plantilla 'user_profile.html' y pasa los datos del usuario
    return render(request, 'user_profile.html', {'user_info': user_info})