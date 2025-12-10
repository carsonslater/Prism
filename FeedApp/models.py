from django.db import models
from django.contrib.auth.models import User


# The image shows a Django model definition for a User Profile
class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=300, blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    # Establishes a 1-to-1 link with Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Establishes a Many-to-Many link with the User model for friends
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    # Automatically set when the object is first created
    created = models.DateTimeField(auto_now=True)
    # Automatically set every time the object is saved
    updated = models.DateTimeField(auto_now_add=True)


STATUS_CHOICES = (("sent", "sent"), ("accepted", "accepted"))


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="receiver"
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="send")
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name="details", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    username = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
