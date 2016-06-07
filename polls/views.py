from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Choice, Question


# Create your views here.

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)
	
	'''template = loader.get_template('polls/index.html')
	context = {'latest_question_list': latest_question_list, }
	return HttpResponse(template.render(context, request))'''

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question':question})

	'''try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question Does not exist")
	return render(request, 'polls/detail.html', {'question': question})'''

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#redisplay the question voting form
		return render(request, 'polls/detail.html',
			{'question': question, 'error_message': "You didnt select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#Always return an HttpResponseRedirect after successfully dealing
		#with POST data. THis prevents data from being posted twice if a 
		#user hits the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))