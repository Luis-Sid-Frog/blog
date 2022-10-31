from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def post_list(request):
        object_list = Post.published.all()
        paginator = Paginator(object_list, 3) # 3 for page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            #If page isnotinteger then return first page of results
            posts = paginator.page(1)
        except EmptyPage:
            #If page is > than last page number  then return last page of results
            posts = paginator.page(paginator.num_pages)
            posts = Post.published.all()
        return render(request,
                      'blog/post/list.html',
                      {'page': page,
                      'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,slug=post,
                                 status='published',
                                 publish_year=year,
                                 publish_month=month,
                                 publish_day=day,
                                 )
    return render(request,
                      'blog/post/detail.html',
                      {'post': post})


def post_share(request, post_id):
    #Downloading post by his ID
    post = get_object_or_404(Post, id=post_id, status = 'published')
    sent= False
    if request.method = 'POST':
        # Form was sent
        if form.is_valid():
            #Positive
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'],cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title, post_url, cd['name'],cd['comments'])
            send_mail = (subject, message, 'mateuszsadowski24@gmail.com', [cd['to']])
            send = True
            # so message can be sent
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,'form':form,'sent':sent})