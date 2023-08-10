# Project 3 - FitMeIn
## Description
<p>At week nine of the Software Engineering Immersive course at General Assembly, we were challenged to work in a team for this project. We were requested to architect, design and collaboratively build a full-stack web app using Python and Django.</p>

## Working Team
Meet the team: [Myself](https://github.com/gellisun) [Hannah Curran](https://github.com/hannahcurran) [James Carter](https://github.com/JamesC215) [Lucas Neno](https://github.com/casneno)<br>
<p>There was a great synergy from the beginning, we went through the planning all together and decided that we wanted to build a social network for couch potatoes who need some motivation to exercise.
</p>
<p>During the planning we also decided that we would be working with a mix of pair/mob programming and solo programming depending on the needs and functionalities.</p>

## Technology Used
### Code & Collaboration
<div align="left">
	<code><img width="30" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/html-5.svg" alt="HTML" title="HTML"/></code>
	<code><img width="30" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/css-3.svg" alt="CSS" title="CSS"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/bootstrap.svg" alt="Bootstrap" title="Bootstrap"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/javascript.svg" alt="JavaScript" title="JavaScript"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/python.svg" alt="Python" title="Python"/></code>
  <code><img width="30" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/django.svg" alt="Django" title="Django"/></code>
</div><br>
<div align="left">
	<code><img width="80" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/git.svg" alt="Git" title="Git"/></code>
	<code><img width="40" src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/github-icon.svg" alt="GitHub" title="GitHub"/></code>
</div>

## Brief
- Connect to and perform data operations on a PostgreSQL database (the default SQLLite3 database is not acceptable).
- If consuming an API, have at least one data entity (Model) in addition to the built-in User model.
- If not consuming an API, have at least two data entities (Models) in addition to the built-in User model.
- Have full-CRUD data operations across any combination of the app's models (excluding the User model).
- Authenticate users using Django's built-in authentication.
- Implement authorization by restricting access to the Creation, Updating & Deletion of data resources.

## Planning
### Brainstorming
![Initial brainstorming on the project](/main_app/static/images/README/Brainstorming.png "Initial brainstorming on the project")
### Wireframe
![Mobile](/main_app/static/images/README/mobile-wireframe.png "Wireframe for mobile")<br>

![Web](/main_app/static/images/README/web-wireframe.png "Wireframe for web")
### ERD
![ERD](/main_app/static/images/READMEerd.png "ERD")

## Code Process
<p>The biggest challenge regarding the various functionalities was surely understanding how to make a 1:1 relationship work.</p>

```JavaScript
@login_required
def profile(request):
  try:
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile}
    if profile:
        profile_form = ProfileForm(instance=profile)
        comments = Comment.objects.filter(user=request.user)
        context['profile_form']=profile_form
        context['comments']=comments
    return render(request, 'user/profile.html', context)
  except Profile.DoesNotExist:
    return redirect('create_profile')


# ---------------- Sign-Up ------------------------


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('create_profile')
    else:
      error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


#-------------Create Profile----------------


class ProfileCreate(CreateView):
  model = Profile
  template_name = 'user/create_profile.html'
  fields = ['age', 'gender', 'location', 'is_couch_potato', 'favorites', 'latitude', 'longitude', 'is_active']
  success_url = reverse_lazy('profile')  # Replace 'profile-detail' with your actual URL pattern

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      print(form)
      return super().form_valid(form)
```

## Challenges
<p>The most time consuming challenge we faced was pulling down from the main remote repo after major changes and functionalities were made. Also, as the functionalities we wanted to implement were different from we did during class and labs, that meant that we all had to go through a lot of documentation in order to implement them.</p>

## Wins

## Key Learnings

## Future Improvements
- We would like the app show all the connections made.
- We would like it to also be a place where, based on the user's location, fitness events in the area can be suggested.
- We would like to add the possiblity to also find recipes and eating habits and suggestions to improve the user's health.


