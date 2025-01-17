from django.shortcuts import render, redirect
from postApp.models import Post

#Import para enviar correos
from postApp.forms import ContactEmailForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
#from postApp.forms import FormularioPost

def inicio(request):

    return render(request, 'postApp/inicio.html')


def todos_los_post(request):

    posts = Post.objects.all().order_by('-fecha_publicacion')

    return render(request, 'postApp/todos_los_post.html', {'posts': posts})

class ListaPosts(ListView):

    model = Post
    template_name= "postApp/lista_post.html"

class VerPost(DetailView):
    
    model = Post
    template_name= "postApp/ver_post.html"

class CrearPost(CreateView):
    
    #form_class= FormularioPost
    model = Post
    fields = ['titulo', 'subtitulo', 'categoria', 'autor', 'contenido', 'imagen']
    success_url = "/postApp/postLista"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto.update({
            'tipo_template': 'Publicar'
        })
        return contexto
class UpdatePost(UpdateView):

    #form_class= FormularioPost
    model = Post
    fields = ['titulo', 'subtitulo', 'categoria', 'autor', 'contenido', 'imagen']
    success_url = "/postApp/postLista"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto.update({
            'tipo_template': 'Editar' 
        })
        return contexto
class BorrarPost(DeleteView):

    model = Post
    success_url = "/postApp/postLista"

def aboutUs(request):
    return render(request,'postApp/about_us.html')

#Envio de correo desde Contacto
def contact(request):
    if request.method == 'POST':
        form = ContactEmailForm(request.POST)
        if form.is_valid():
            subject = "Tienes una nueva consulta desde el blog Tercer Tiempo" 
            body = {
            'first_name': form.cleaned_data['first_name'], 
            'last_name': form.cleaned_data['last_name'], 
            'email': form.cleaned_data['email_address'], 
            'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'blogtercertiempo2022@gmail.com', ['blogtercertiempo2022@gmail.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render ("index.html")
      
    form = ContactEmailForm()
    return render(request, "postApp/contacto.html", {'form':form})