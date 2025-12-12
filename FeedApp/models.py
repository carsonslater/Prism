from django.db import models
from django.contrib.auth.models import User

# This file is used to define the database structure (schema) for the app.
# Each class represents a table in the database.
# Django handles creating the tables and managing the relationships.

class Profile(models.Model):
    # Field definitions:
    # Each attribute represents a column in the database table and the type of data it holds.
    
    # CharField is for short text strings. 'max_length' is required.
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    # EmailField checks that the value is a valid email address.
    email = models.EmailField(max_length=300, blank=True)
    # DateField is for storing dates.
    dob = models.DateField(null=True, blank=True)
    # TextField is for large amounts of text.
    bio = models.TextField(blank=True)
    
    # Relationship fields:
    # OneToOneField: Each User has exactly one Profile, and each Profile belongs to exactly one User.
    # on_delete=models.CASCADE means if the User creates is deleted, this Profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # ManyToManyField: A user can have many friends (other Users), and those friends can have many friends.
    # related_name allows us to access this relationship from the User model (e.g., user.friends.all()).
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    
    # DateTimeField with auto_now_add=True is set only when the object is first created.
    created = models.DateTimeField(auto_now_add=True)
    # DateTimeField with auto_now=True is updated every time the object is saved.
    updated = models.DateTimeField(auto_now=True)

    # __str__ defines the string representation of the object, used in the Admin site and debugging.
    def __str__(self):
        return f"{self.user.username}'s Profile"


# Choices for the 'status' field in the Relationship model.
# The first element is the value stored in DB, the second is the human-readable name.
STATUS_CHOICES = (("sent", "sent"), ("accepted", "accepted"))


class Relationship(models.Model):
    # ForeignKey links to another model. It represents a many-to-one relationship.
    # Here, a Relationship links a sender (Profile) and a receiver (Profile).
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="receiver"
    )
    # choices argument limits the field to the options in STATUS_CHOICES.
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="sent")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    # ForeignKey to User: one user can have many posts.
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    # ImageField stores an image. 'upload_to' specifies the subdirectory in MEDIA_ROOT.
    image = models.ImageField(upload_to="images", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Comment(models.Model):
    # ForeignKey to Post: one post can have many comments.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name="details", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    # ForeignKey to User and Post to track who liked what.
    username = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
