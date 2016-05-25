
from system.core.controller import *
from instagram.client import InstagramAPI
import tweepy

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        
    def index(self):
        return self.load_view('/users/index.html')
    def new(self):
        session["first_name"] = request.form["first_name"]
        user_info = {
            "first_name": session["first_name"],
            "last_name": request.form["last_name"], 
            "email": request.form["new_email"], 
            "password": request.form["new_password"], 
            "pw_confirm": request.form["confirm_pw"],
            "city": request.form["city"],
            "state": request.form["state"]}
        create_status = self.models["User"].create_new(user_info)

        if create_status["status"] == True:
            session["user_id"] = create_status["user"]["id"]
            return redirect("/users/add_activity")  
        else:
            for message in create_status["errors"]:
                flash(message)
            return redirect("/")
    def login(self):
        user_info = {"email": request.form["email"], "password": request.form["password"]}
        login_status = self.models["User"].login(user_info)
        if login_status:
            session["first_name"] = login_status["first_name"]
            session["user_id"] = login_status["id"]
            return redirect("/users/profile_page")
            
        else:
            flash("Error logging in")
            return redirect("/")
    def add_activity_page(self):
        access_token = "[INSERT ACCESS TOKEN]"
        client_secret = "[INSERT CLIENT SECRET]"
        api = InstagramAPI(access_token=access_token, client_secret=client_secret)
        recent_media, url = api.user_recent_media()
        photos_travel=[]
        tag_search, next_tag = api.tag_search(q="travel")
        tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
        for tag_media in tag_recent_media:
            photos_travel.append("%s" % tag_media.get_standard_resolution_url())
        photos_outdoor=[]
        tag_search, next_tag = api.tag_search(q="outdoor")
        tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
        for tag_media in tag_recent_media:
            photos_outdoor.append("%s" % tag_media.get_standard_resolution_url())
        photos_indoor=[]
        tag_search, next_tag = api.tag_search(q="indoor")
        tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
        for tag_media in tag_recent_media:
            photos_indoor.append("%s" % tag_media.get_standard_resolution_url())

        info = { "user_id": session["user_id"]}
        activities = self.models["User"].get_all_activities(info)
        return self.load_view("/users/add_activity.html", activities=activities, recent_media=recent_media, url = url, photos_travel = photos_travel, photos_indoor=photos_indoor, photos_outdoor=photos_outdoor)
    def profile_page(self):
        info = {"user_id": session["user_id"]}
        my_activities = self.models["User"].get_my_list(info)
        return self.load_view("/users/profile.html", name=session["first_name"], my_activities=my_activities)
    def add(self, id):
        info = {
            "activity_id": id,
            "user_id": session["user_id"]
        }
        self.models["User"].add_my_list(info)
        return redirect("/users/get_activities")
    def get_activities(self):
        info = {"user_id": session["user_id"]}
        activities = self.models["User"].get_all_activities(info)
        return self.load_view("/users/activity_partial.html", activities=activities)
    def delete(self, id):
        info = {
            "activity_id": id,
            "user_id": session["user_id"]
        }
        self.models["User"].delete_item(info)
        return redirect("/users/get_all")
    def get_all(self):
        info_all = {"user_id": session["user_id"]}
        my_activities = self.models["User"].get_my_list(info_all)
        return self.load_view("/users/partial_profile.html", name=session["first_name"], my_activities=my_activities)
    def new_activity(self):
        info = {
            "activity": request.form["new_activity"],
            "category_id": request.form["category"],
            "user_id": session["user_id"]
        }
        add_status = self.models["User"].add_new_activity(info)
        if add_status["status"] == True:
            return redirect("/users/get_activities")
        else:
            for errors in add_status["errors"]:
                flash(errors)
            return redirect("/users/get_activities")   
    def logout(self):
        session.clear()
        return redirect("/")

