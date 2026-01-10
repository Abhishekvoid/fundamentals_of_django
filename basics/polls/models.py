

"""

Models is use to define your database layout and additional metadata

-   Model is source of information about your data. it contain essential fields and behaviors of the   data we're storing 

- This includes the migrations, migrations are entirely derived from your models file, and are essentially a history that Django can roll through to update your database schema to match your current models.
"""

from django.db import models
import uuid

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class AppUser(models.Model):

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length = 100)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user


"""
- Each is represnted by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model

- Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

- The name of each Field instance (e.g. question_text or pub_date) is the field’s name, in machine-friendly format. You’ll use this value in your Python code, and your database will use it as the column name.

- You can use an optional first positional argument to a Field to designate a human-readable name. That’s used in a couple of introspective parts of Django, and it doubles as documentation. If this field isn’t provided, Django will use the machine-readable name. In this example, we’ve only defined a human-readable name for Question.pub_date. For all other fields in this model, the field’s machine-readable name will suffice as its human-readable name.

- Some Field classes have required arguments. CharField, for example, requires that you give it a max_length. That’s used not only in the database schema, but in validation, as we’ll soon see.

- A Field can also have various optional arguments; in this case, we’ve set the default value of votes to 0.

- Finally, note a relationship is defined, using ForeignKey. That tells Django each Choice is related to a single Question. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.

"""


"""
Activating models:
That small bit of model code gives Django a lot of information. With it, Django is able to:
- Create a database schema (CREATE TABLE statements) for this app.
- Create a Python database-access API for accessing Question and Choice objects.
But first we need to tell our project that the polls app is installed.

Philosophy:

- Django apps are “pluggable”: You can use an app in multiple projects, and you can distribute apps, because they don’t have to be tied to a given Django installation.

- To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. The PollsConfig class is in the polls/apps.py file, so its dotted path is 'polls.apps.PollsConfig'. Edit the mysite/settings.py file and add that dotted path to the INSTALLED_APPS setting. It’ll look like this: -> setting.py

"""