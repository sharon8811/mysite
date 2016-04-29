from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives

# Create your views here.


def index(request):
    if request.method == 'POST':
        context = {
            'sender': request.POST['sender'],
            'subject': request.POST['subject'],
            'message': request.POST['message'],
        }
        if context['sender'] == "" or context['subject'] == "" or context['message'] == "":
            template_name = 'formapp/index.html'
            form = ContactForm(initial={'subject': context['subject'], 'sender': context['sender'],
                                        'message': context['message']})
            context = {'user_form': form, 'err': 'Please fill all the fields!'}
            return render(request, template_name, context)
        else:
            try:
                htmlmsg = "<strong>From: " + request.POST['sender'] + "<br><br>" + request.POST['message']
                msg = EmailMultiAlternatives(request.POST['subject'], request.POST['message'],
                                             'contact@365testdomain.com', ['sharon8811@gmail.com'])
                msg.attach_alternative(htmlmsg, "text/html")
                msg.send()
                #send_mail(request.POST['subject'], msg, 'contact@365testdomain.com',
                #          ['sharon8811@gmail.com'], fail_silently=False)
            except BadHeaderError:
                form = ContactForm(request.POST)
                context = {'user_form': form, 'err': 'Error in sending message!'}
                return render(request, 'formapp/index.html', context)
            template_name = 'formapp/index2.html'
            context['msg'] = "The Contact mail was sent successfully"
            return render(request, template_name, context)
    else:
        template_name = 'formapp/index.html'
        form = ContactForm(initial={'subject': 'Contact us!'})
        context = {'user_form': form, 'err': ''}
        return render(request, template_name, context)

