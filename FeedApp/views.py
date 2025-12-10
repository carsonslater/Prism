from django.shortcuts import render, redirect
from .forms import PostForm, ProfileForm, RelationshipForm
from .models import Post, Comment, Like, Profile, Relationship
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

# When a URL request matches the pattern we just defined,
# Django looks for a function called index() in the views.py file.


def index(request):
    """The home page for Learning Log."""
    return render(request, "FeedApp/index.html")


@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user)
    if not profile.exists():
        Profile.objects.create(user=request.user) # Profile is the model here
    profile = Profile.objects.get(user=request.user)

    if request.method != 'POST':
        form = ProfileForm(instance=profile) # we need a specific instance
    else:
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('FeedApp:profile')

    context = {'form': form}
    return render(request, 'FeedApp/profile.html', context)


@login_required
def myfeed(request):
    comment_count_list = []
    like_count_list = []
    posts = Post.objects.filter(username=request.user).order_by('-date_posted')
    for p in posts:
        c_count = Comment.objects.filter(post=p).count() # this enables us to count how many posts there are
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    zipped_list = zip(posts, comment_count_list, like_count_list)

    context = {'posts': posts, 'zipped_list': zipped_list}
    return render(request, 'FeedApp/myfeed.html', context)

@login_required
def new_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            new_post=form.save(commit=False) # not saving or writing it to the database because it doesnt have all information yet
            new_post.username = request.user
            new_post.save()
            return redirect('FeedApp:myfeed')

    context = {'form': form}
    return render(request, 'FeedApp/new_post.html', context)

@login_required
def comments(request, post_id):
    post = Post.objects.get(id=post_id)  # Changed from filter to get

    if request.method == 'POST' and request.POST.get('btn1'):
        comment = request.POST.get("comment")  # Fixed: uppercase POST
        Comment.objects.create(post_id=post_id, username=request.user, text=comment, date_added=date.today())
        return redirect('FeedApp:comments', post_id=post_id)  # Redirect after POST

    comments = Comment.objects.filter(post=post_id)

    context = {'post': post, 'comments': comments}
    return render(request, 'FeedApp/comments.html', context)


@login_required
def friendsfeed(request):
    comment_count_list = []
    like_count_list = []
    friends = Profile.objects.filter(username=friends).values('friends')
    posts = Post.objects.filter(username__in=friends).order_by('-date_posted')
    for p in posts:
        c_count = Comment.objects.filter(post=p).count() # this enables us to count how many posts there are
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    zipped_list = zip(posts, comment_count_list, like_count_list)

    if request.method == 'POST' and request.POST.get("like"):
        post_to_like = request.POST.get("like")
        like_already_exists = like.objects.filter(post_id=post_to_like, username=request.user)
        if not like_already_exists:
            Like.objects.create(post_id=post_to_like, username=request.user)
            return redirect('FeedApp:friendsfeed')

    context = {'posts': posts, 'zipped_list': zipped_list}
    return render(request, 'FeedApp/friendsfeed.html', context)


@login_required
def friends(request):
    # get the admin profile and user profile to create their first relationship
    admin_profile = Profile.objects.get(user=1)
    user_profile = Profile.objects.get(user=request.user)

    # to get my friends
    user_friends = user_profile.friends.all()
    user_friends_profiles = Profile.objects.filter(user__in=user_friends)

    # to get Friend requests sent
    user_relationships = Relationship.objects.filter(sender=user_profile)
    request_sent_profiles = user_relationship.values('receiver')

    # to get elligible profiles - exclude the user, their existing friends, and friend requests sent already
    all_profiles = Profile.objects.exclude(user=request.user).exclude(id_in=user_friends_profiles).exclude(id__in=request_sent_profiles)

    # get friend request recieved by the user
    request_recieved_profiles = Relationship.objects.filter(receiver=user_profile, status='sent')

    # if this is the first time to access the friend request page, create the first
    # relationship with the admin of the website
    if not user_relationships.exists():
        Relationship.objects.create(sender=user_profile, reciever=admin_profile, status='sent')

    # check to see WHICH submit button was pressed

    # process all send requests
    if request.method == 'POST' and request.POST.get("send_requests"):
        receivers = request.POST.getlist("send_request")
