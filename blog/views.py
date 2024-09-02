from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post
from .forms import EmailPostForm


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list,2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year,month,day,post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug =post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )

def post_share(request,post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status= Post.Status.PUBLISHED
    )
    if request.method =='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',{
            'post': post,
            'form' : form
        }
    )