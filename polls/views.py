from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from .forms import QuestionAjaxForm
from django.core.context_processors import csrf
from django.utils import timezone

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')  # [:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        votesum = 0
        for cho in question.choice_set.all():
            votesum += cho.votes
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def addpoll(request, object_id=False):
    # pollformset = modelformset_factory(Question, fields=('question_text', 'pub_date', 'choice_text', 'votes'))
    # pollformset = inlineformset_factory(Question, Choice, fields=('choice_text', 'votes'))
    # if object_id:
    #    poll = Question.objects.get(pk=object_id)
    # else:
    #    poll = Question()

    if request.method == "POST":
        if request.POST['question_text'] != "":
            nq = Question(question_text= request.POST['question_text'], pub_date=timezone.now())
            nq.save()
            for key, value in request.POST.items():
                if key != 'question_text' and key != 'csrfmiddlewaretoken':
                    nc = Choice(question=nq, choice_text=value, votes=0)
                    nc.save()
            return HttpResponseRedirect("/polls/", {'msg': "The new poll was added successfully"})
        else:
            args = {}
            args.update(csrf(request))
            args['error'] = "Please fill poll question field"
            return render_to_response('polls/addpoll2.html', args)
    else:
        # f = QuestionAjaxForm(instance=poll, initial={'pub_date': timezone.now()})
        # fs = pollformset(instance=poll)
        args = {}
        args.update(csrf(request))
        return render_to_response('polls/addpoll2.html', args)

    args = {}
    args.update(csrf(request))
    # args['fs'] = fs
    # args['f'] = f

    # args['poll'] = poll
    #return render_to_response('polls/addpoll2.html', args)
    # return render(request, 'polls/addpoll.html', {'formset': formset})
