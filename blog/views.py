from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from .forms import EmailPostForms


class PostListView(ListView):
    '''Альтернативное представление списка постов'''
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):  # все сообщения
    # Постраничная разбивка
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


# обработчик формы
def post_share(request, post_id):
    # извлечь посты по идентификатору
    post = get_object_or_404(Post,
                             id=post_id,
                             staus=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForms(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # отправить электронное письмо
    else:
        form = EmailPostForms()
    return render(request,
                  'blog/post/share.html',
                  {'post': post,
                   'form': form})
