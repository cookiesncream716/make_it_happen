
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    def create_new(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not info["first_name"]:
            errors.append("First name cannot be blank")
        elif len(info["first_name"]) < 2:
            errors.append("First name must be at least 2 characters long")
        if not info["last_name"]:
            errors.append("Last name cannot be blank")
        elif len(info["last_name"]) < 2:
            errors.append("Last name must be at least 2 characters long")
        if not info["email"]:
            errors.append("Email cannot be blank")
        elif not EMAIL_REGEX.match(info["email"]):
            errors.append("Email format must be valid")
        if not info["password"]:
            errors.append("Password cannot be blank")
        elif len(info["password"]) < 8:
            errors.append("Password must be at least 8 characters long")
        elif info["password"] != info["pw_confirm"]:
            errors.append("Password and Password Confirmation must match")
        if not info["city"]:
            errors.append("City cannot be blank")
        if len(info["state"]) < 2:
            errors.append("State abbreviation must be 2 characters long")
        elif len(info["state"]) > 2:
            errors.append("State abbreviation can only be 2 letters")

        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info["password"] 
            hashed_pw = self.bcrypt.generate_password_hash(password)
            create_query = "INSERT INTO users (first_name, last_name, email, password, city, state, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, now(), now())"
            create_data = [info["first_name"], info["last_name"], info["email"], hashed_pw, info["city"], info["state"]]
            self.db.query_db(create_query, create_data)
            get_user  = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user)
            return {"status": True, "user": user[0]}
    def login(self, info):
        password = info["password"]
        login_query = "SELECT * FROM users WHERE email = %s LIMIT 1"
        login_data = [info["email"]]
        users = self.db.query_db(login_query, login_data)
        if users:
             if self.bcrypt.check_password_hash(users[0]["password"], password):
                return users[0]
        return False
    def get_all_activities(self, info):
        query = "SELECT * FROM activities WHERE activities.id NOT IN (SELECT activity_id FROM bucket_lists WHERE user_id = %s)"
        data = [info["user_id"]]
        return self.db.query_db(query, data)
    def add_my_list(self, info):
        query = "INSERT INTO bucket_lists (user_id, activity_id, created_at, completed) VALUES (%s, %s, now(), 0)"
        data = [info["user_id"], info["activity_id"]]
        self.db.query_db(query, data)
    def get_my_list(self, info):
        query = "SELECT users.id, bucket_lists.user_id, bucket_lists.activity_id, bucket_lists.completed, bucket_lists.updated_at, activities.activity FROM activities JOIN  bucket_lists ON activities.id=bucket_lists.activity_id JOIN users ON bucket_lists.user_id=users.id WHERE users.id=%s"
        data = [info["user_id"]]
        return self.db.query_db(query, data)
    def delete_item(self, info):
        query = "DELETE FROM bucket_lists WHERE user_id = %s and activity_id = %s"
        data = [info["user_id"], info["activity_id"]]
        self.db.query_db(query, data)
    def add_new_activity(self, info):
        errors = []
        if not info["activity"]:
            errors.append("Activity cannot be blank")
        if errors:
            return {"status": False, "errors": errors}        
        if info["category_id"] == "Travel":
            info["category_id"] = 1
        elif info["category_id"] == "Outdoor":
            info["category_id"] = 2
        else:
            info["category_id"] = 3
        query = "INSERT into activities (activity, category_id, created_at) VALUES (%s, %s, now())"
        data = [info["activity"], info["category_id"]]
        self.db.query_db(query, data)
        get_new_activity = "SELECT * FROM activities ORDER BY id DESC LIMIT 1"
        new_activity = self.db.query_db(get_new_activity)
        add_query = "INSERT INTO bucket_lists (user_id, activity_id, created_at, completed) VALUES (%s, %s, now(), 0)"
        add_data = [info["user_id"], new_activity[0]["id"]]
        self.db.query_db(add_query, add_data)
        return {"status": True}
        


