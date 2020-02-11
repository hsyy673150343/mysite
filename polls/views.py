from django.shortcuts import render, get_object_or_404

# Create your views here.

'''每个视图必须要做的只有两件事：返回一个包含被请求页面内容的 HttpResponse 对象，\
或者抛出一个异常，比如 Http404 。至于你还想干些什么，随便你\
你的视图可以从数据库里读取记录，可以使用一个模板引擎（比如 Django 自带的，或者其他第三方的），\
可以生成一个 PDF 文件，可以输出一个 XML，创建一个 ZIP 文件，你可以做任何你想做的事，使用任何你想用的 Python 库。\
Django 只要求返回的是一个 HttpResponse ，或者抛出一个异常。
'''

from django.http import HttpResponse, HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from django.views import generic



# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     '''这个上下文是一个字典，它将模板内的变量映射为 Python 对象。'''
#     context = {
#         'latest_question_list': latest_question_list
#     }
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#    # 如果指定问题 ID 所对应的问题不存在，这个视图就会抛出一个 Http404 异常。
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

'''通用视图'''
'''
我们在这里使用两个通用视图： ListView 和 DetailView 。
这两个视图分别抽象“显示一个对象列表”和“显示一个特定类型对象的详细信息页面”这两种概念。

每个通用视图需要知道它将作用于哪个模型。 这由 model 属性提供。
DetailView 期望从 URL 中捕获名为 "pk" 的主键值，所以我们为通用视图把 question_id 改成 pk 。
默认情况下，通用视图 DetailView 使用一个叫做 <app name>/<model name>_detail.html 的模板。
在我们的例子中，它将使用 "polls/question_detail.html" 模板。
template_name 属性是用来告诉 Django 使用一个指定的模板名字，而不是自动生成的默认名字。 
我们也为 results 列表视图指定了 template_name —— 这确保 results 视图和 detail 视图在渲染时具有不同的外观，
即使它们在后台都是同一个 DetailView 。

类似地，ListView 使用一个叫做 <app name>/<model name>_list.html 的默认模板；
我们使用 template_name 来告诉 ListView 使用我们创建的已经存在的 "polls/index.html" 模板。

在之前的教程中，提供模板文件时都带有一个包含 question 和 latest_question_list 变量的 context。
对于 DetailView ， question 变量会自动提供—— 因为我们使用 Django 的模型 (Question)， 
Django 能够为 context 变量决定一个合适的名字。然而对于 ListView， 自动生成的 context 变量是 question_list。
为了覆盖这个行为，我们提供 context_object_name 属性，表示我们想使用 latest_question_list。
作为一种替换方案，你可以改变你的模板来匹配新的 context 变量 —— 这是一种更便捷的方法，告诉 Django 使用你想使用的变量名。
'''
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        '''request.POST 是一个类字典对象，让你可以通过关键字的名字获取提交的数据。\
        这个例子中， request.POST['choice'] 以字符串形式返回选择的 Choice 的 ID。\
        request.POST 的值永远是字符串。如果在 request.POST['choice'] 数据中没有提供 choice ，\
        POST 将引发一个 KeyError 。'''
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
        #  HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL
        # 在 HttpResponseRedirect 的构造函数中使用 reverse() 函数。\
        # 这个函数避免了我们在视图函数中硬编码 URL。\
        # 它需要我们给出我们想要跳转的视图的名字和该视图所对应的 URL模式中需要给该视图提供的参数。\
        # 重定向的 URL 将调用 'results' 视图来显示最终的页面。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
