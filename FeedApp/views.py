from django.shortcuts import render, redirect
from .forms import PostForm, ProfileForm, RelationshipForm
from .models import Post, Comment, Like, Profile, Relationship
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create views here.
# Views are Python functions that take a Web request and return a Web response.
# This response can be the HTML contents of a Web page, or a redirect, or a 404 error, etc.

# When a URL request matches the pattern we just defined,
# Django looks for a function called index() in the views.py file.


def index(request):
    """The home page for Learning Log."""
    # render() combines a template with a context dictionary and returns an HttpResponse object.
    return render(request, "FeedApp/index.html")


# @login_required decorator restricts access to this view to logged-in users only.
# If a user is not logged in, they will be redirected to the login page (configured in settings.py).
@login_required
def profile(request):
    # Retrieve the Profile object associated with the current user.
    profile = Profile.objects.filter(user=request.user)
    
    # If no profile exists for the user, create one.
    if not profile.exists():
        Profile.objects.create(user=request.user) # Profile is the model here
    
    # Get the single profile object.
    profile = Profile.objects.get(user=request.user)

    # Check if this is a POST request (form submission).
    if request.method != 'POST':
        # No data submitted; create a form pre-filled with the user's profile info.
        form = ProfileForm(instance=profile) # we need a specific instance to edit
    else:
        # POST data submitted; process data.
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid(): # Check if form data is valid.
            form.save() # Save the new data to the database.
            return redirect('FeedApp:profile') # Redirect back to the profile page.

    # Context dictionary transmits data to the template.
    context = {'form': form}
    return render(request, 'FeedApp/profile.html', context)


@login_required
def myfeed(request):
    comment_count_list = []
    like_count_list = []
    
    # Filter posts to show only those created by the current user.
    # .order_by('-date_posted') sorts them by date in descending order (newest first).
    posts = Post.objects.filter(username=request.user).order_by('-date_posted')
    
    for p in posts:
        # Count comments and likes for each post.
        c_count = Comment.objects.filter(post=p).count() # this enables us to count how many posts there are
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    
    # zip() combines multiple lists so we can iterate over them together in the template.
    zipped_list = zip(posts, comment_count_list, like_count_list)

    context = {'posts': posts, 'zipped_list': zipped_list}
    return render(request, 'FeedApp/myfeed.html', context)

@login_required
def new_post(request):
    if request.method != 'POST':
        # New empty form.
        form = PostForm()
    else:
        # Form submitted with data and files (for the image).
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False creates the object but doesn't save to DB yet.
            # We need to do this to assign the current user to the post first.
            new_post = form.save(commit=False) 
            new_post.username = request.user
            new_post.save() # Now save the complete object.
            return redirect('FeedApp:myfeed')

    context = {'form': form}
    return render(request, 'FeedApp/new_post.html', context)

@login_required
def comments(request, post_id):
    # Retrieve the specific post by its primary key (id).
    post = Post.objects.get(id=post_id) 

    # Handle comment submission within the same view.
    if request.method == 'POST' and request.POST.get('btn1'):
        comment = request.POST.get("comment") 
        # Create a new Comment linked to this post and user.
        Comment.objects.create(post_id=post_id, username=request.user, text=comment, date_added=date.today())
        return redirect('FeedApp:comments', post_id=post_id)  # Redirect to refresh the page.

    # Get all comments associated with this post.
    comments = Comment.objects.filter(post=post_id)

    context = {'post': post, 'comments': comments}
    return render(request, 'FeedApp/comments.html', context)


@login_required
def friendsfeed(request):
    comment_count_list = []
    like_count_list = []
    
    current_user_profile = Profile.objects.get(user=request.user)
    # Get all users who are friends with the current user.
    friends_users = current_user_profile.friends.all()
    
    # Filter posts to include only those where the username is in the list of friends.
    posts = Post.objects.filter(username__in=friends_users).order_by('-date_posted')
    
    for p in posts:
        c_count = Comment.objects.filter(post=p).count() 
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    
    zipped_list = zip(posts, comment_count_list, like_count_list)

    # Handle liking a post via POST request.
    if request.method == 'POST' and request.POST.get("like"):
        post_to_like = request.POST.get("like")
        # Check if the user already liked this post to prevent duplicate likes.
        like_already_exists = Like.objects.filter(post_id=post_to_like, username=request.user)
        if not like_already_exists.exists():
            Like.objects.create(post_id=post_to_like, username=request.user)
            return redirect('FeedApp:friendsfeed')

    context = {'posts': posts, 'zipped_list': zipped_list}
    return render(request, 'FeedApp/friendsfeed.html', context)


@login_required
def friends(request):
    # This view manages friend requests and the friends list.
    
    # get the admin profile and user profile to create their first relationship
    admin_profile = Profile.objects.get(user=1) # Assuming user ID 1 is admin.
    
    # get_or_create tries to get the object, or creates it if it doesn't exist.
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    # to get my friends
    user_friends = user_profile.friends.all()
    user_friends_profiles = Profile.objects.filter(user__in=user_friends)

    # to get Friend requests sent
    user_relationships = Relationship.objects.filter(sender=user_profile)
    request_sent_profiles = user_relationships.values('receiver')

    # to get eligible profiles - exclude the user themselves, their existing friends, and people they already sent requests to.
    all_profiles = Profile.objects.exclude(user=request.user).exclude(id__in=user_friends_profiles).exclude(id__in=request_sent_profiles)

    # get friend request recieved by the user
    request_recieved_profiles = Relationship.objects.filter(receiver=user_profile, status='sent')

    # if this is the first time to access the friend request page, create the first
    # relationship with the admin of the website
    if not user_relationships.exists():
        Relationship.objects.create(sender=user_profile, receiver=admin_profile, status='sent')

    # check to see WHICH submit button was pressed

    # process all send requests
    if request.method == 'POST' and request.POST.get("send_requests"):
        receivers = request.POST.getlist("send_requests")
        for receiver in receivers:
            receiver_profile = Profile.objects.get(id=receiver)
            # Create a Relationship object with status='sent'.
            Relationship.objects.create(sender=user_profile, receiver=receiver_profile, status='sent')

        return redirect('FeedApp:friends')

    # process all recieved requests
    if request.method == 'POST' and request.POST.get("recieve_requests"):
        senders = request.POST.getlist("recieve_requests")
        for sender in senders:
            # update relationship for the sender to status 'accepted'
            Relationship.objects.filter(id=sender).update(status='accepted')

            # create an object to access the sender's user id to add friends
            # to list of user
            relationship_obj = Relationship.objects.get(id=sender)
            user_profile.friends.add(relationship_obj.sender.user)

            # add the user to the friend's list of the sender profile
            relationship_obj.sender.friends.add(request.user)

    context = {'user_friends_profiles': user_friends_profiles, 'user_relationships':user_relationships,
               'all_profiles': all_profiles, 'request_recieved_profiles': request_recieved_profiles}

    return render(request, 'FeedApp/friends.html', context)
