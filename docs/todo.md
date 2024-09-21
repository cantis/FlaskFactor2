# Flask Factor 2

## Todo
- [ ] Create DB Tables
- [x] Add Bootstrap base template
- [x] Add Navbar
- [x] Add Footer
- [x] Players route add/edit/delete
- [ ] User login
- [ ] items route add/edit/delete
- [ ] admin route settings

### DB Tables
- [x] players
- [ ] sessions
- [ ] items
- [ ] item_categories
- [ ] item_tags
- [ ] characters
- [ ] character_items
- [ ] campaigns
- [ ] player_characters
- [ ] player_campaigns
- [ ] character_campaigns


Summary: Plan for flask-login integration... from github copilot
- [x] Install and Initialize flask-login.
- [x] Update the Player Model to include UserMixin.
- [x] Define a User Loader Callback.
- [x] Create Login Form using FlaskForm.
- [x] Add Login and Logout Routes.
- [ ] Protect Routes with @login_required.
- [ ] Create Templates for login and other views.
By following these steps, you can integrate flask-login into your Flask application to handle user authentication, including login, logout, and protecting routes.