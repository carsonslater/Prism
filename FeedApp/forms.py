from django import forms
from .models import (
    Post,
    Profile,
    Relationship,
)  # Assuming models are imported from local file


# Form 1: for creating or editing a Post object
# ModelForm creates a form automatically from a model class.
class PostForm(forms.ModelForm):
    # The Meta class is where we tell Django which model to use and which fields to include in the form.
    class Meta:
        model = Post
        fields = ["description", "image"]
        # labels allow us to customize the text displayed next to the input field.
        labels = {"description": "What would you like to say?"}


# Form 2: for editing a User's Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email", "dob", "bio"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "dob": "Date of Birth",
            "bio": "Bio",
        }


# Form 3: for managing friend requests/relationships
class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        # fields = "__all__" includes all fields from the model in the form.
        fields = "__all__"
        labels = {
            "sender": "Accept friend request from:",
            "receiver": "Send friend request to:",
            "status": "Current status:",
        }
