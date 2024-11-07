**14 Sept 24**
*Start*
Back at it. Today I'm adding a user login form, I think internally I'll use 'user' as copilot and everything else defaults to that. Flask-login will be how I'll handle login and permissions but I'll need to add a user registration form first.

**21 Sept 24**
Working through the login process, added the flask-login extension and updated the player model to include UserMixin. I've also added a user loader callback and created a login form using FlaskForm. I'm now working on the login and logout routes.

The flask-login procedure is still muddy for me, need to work through more.

**6 Nov 24**
Been working on this on and off. I have been having issues with the 3 layer architechture I've been using, So I have an Application, a Route and a Service. With the idea of seperating the database logic from the route logic. It seems reasonable to seperate the two. I've also moved to having seperate templates for read, add, edit and list (players in this case but stil). The issue appears when I try ad add a new user and then get the user 'back' to display the new user. I loose the session on the passing the fix is to inject the session and then it comes back properly. I've also switched back to sqlalchemy. I was trying to use SQLModel but it was causing me issues. I think I'll stick with sqlalchemy for now.