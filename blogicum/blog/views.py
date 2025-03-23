from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.views import generic
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin


from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserUpdateForm


User = get_user_model()



def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.all().filter(
        is_published=True
    ),
        slug=category_slug)

    post_list = category.post.filter(
        pub_date__lte=datetime.utcnow(),
        is_published=True)
    
    for post in post_list:
        comments_count = Comment.objects.filter(post_id=post.id).count()
        post.comments_count = comments_count

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category': category
    }

    return render(request, 'blog/category.html', context)


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = profile.post.all()
    
    for post in post_list:
        comments_count = Comment.objects.filter(post_id=post.id).count()
        post.comments_count = comments_count
    
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    
    
    
    context = {
        'page_obj': page_obj,
        'profile': profile,
    }
    
    return render(request, 'blog/profile.html', context)


class ProfileUpdateView(generic.UpdateView):
    model = Post
    form_class = UserUpdateForm
    template_name = 'blog/user.html'
    
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user
        return None
    
    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.object.username})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.object.author.username})
        
        
class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    
    redirect_field_name = None
    def get_login_url(self) -> str:
         object = self.get_object()
         return reverse_lazy('blog:post_detail', kwargs={'post_id': object.id})
    
    #def dispatch(self, request, *args, **kwargs):
    #    if not request.user.is_authenticated:
    #        return redirect('blog:post_detail', post_id=self.get_object().id)
    #    return super().dispatch(request, *args, **kwargs)
    

class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    
    def get_success_url(self, **kwargs):
        username = self.get_object().author.username
        return reverse_lazy('blog:profile', kwargs={'username': username})


#if self.get_object().author != self.request.user:

class PostList(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10
    
    def get_queryset(self):
        posts = Post.objects.select_related(
            'category'
        ).filter(
            pub_date__lte=datetime.utcnow(),
            is_published=True,
            category__is_published=True)
            
        queryset = list(posts)
        for post in queryset:
            comments_count = Comment.objects.filter(post_id=post.id).count()
            post.comments_count = comments_count
            
        return queryset


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            self.model.objects.prefetch_related(
                'category',
            ).filter(
                pub_date__lte=datetime.utcnow(),
                is_published=True,
                category__is_published=True),
            pk=self.kwargs['post_id']
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        comments = Comment.objects.all().filter(post_id=self.get_object().id)
        context['comments'] = comments
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context


class PostComment(
        LoginRequiredMixin,
        generic.detail.SingleObjectMixin,
        generic.FormView
):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('blog:post_detail', kwargs={'post_id': post.id})


class PostDetailView(generic.View):
    
    def get(self, request, *args, **kwargs):
        view = PostDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class CommentBase(LoginRequiredMixin):
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        comment = self.get_object()
        return reverse(
            'blog:post_detail', kwargs={'post_id': comment.post.id}
        ) + '#comments'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class CommentUpdate(CommentBase, generic.UpdateView):
    template_name = 'blog/comment.html'
    form_class = CommentForm


class CommentDelete(CommentBase, generic.DeleteView):
    template_name = 'blog/comment.html'


















