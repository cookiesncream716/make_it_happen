
from system.core.router import routes

routes['default_controller'] = 'Users'
routes["POST"]["/users/new"] = "Users#new"
routes["POST"]["/users/login"] = "Users#login"
routes["GET"]["/users/profile_page"] = "Users#profile_page"
routes["GET"]["/users/add_activity"] = "Users#add_activity_page"
routes["GET"]["/users/logout"] = "Users#logout"
routes["POST"]["/users/delete/<id>"] = "Users#delete"
routes["POST"]["/users/add/<id>"] = "Users#add"
routes["POST"]["/users/new_activity"] = "Users#new_activity"
routes['/users/inspire_me/<id>'] = 'Twitters#index'
routes["GET"]["/users/get_activities"] = "Users#get_activities"
