""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Twitter(Model):
    def __init__(self):
        super(Twitter, self).__init__()

    def get_activites_name(self, id ):
        query= "SELECT activity FROM activities WHERE id=%s"
        data = [id]
        activity_info = self.db.query_db(query, data)
        activity = activity_info[0]["activity"]
        return activity
            
   