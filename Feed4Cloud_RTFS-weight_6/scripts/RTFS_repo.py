import json

class Service:
    service_ids = {}

    def __init__(self, service_id):
        Service.service_ids = Service.load_data()
        self.service_id = service_id

        if self.service_id not in Service.service_ids:
            Service.service_ids[self.service_id] = {}
            Service.service_ids[self.service_id]['reputation'] = 5


    @classmethod
    def load_data(cls):
        try:
            with open("service_data.json", "r") as f:
                cls.service_ids = json.load(f)

        except FileNotFoundError:
            cls.service_ids = {}
            cls.save_data()
        return cls.service_ids

    @classmethod
    def save_data(cls):
        with open("service_data.json", "w") as f:
            json.dump(Service.service_ids, f)

    def set_reputation(self, reputation):
        Service.service_ids[self.service_id]['reputation'] = reputation

    def get_reputation(self):
        return Service.service_ids[self.service_id]['reputation']


class User:

    user_ids = {}

    def __init__(self, user_id):
        User.user_ids = User.load_data()
        self.user_id = user_id

        if self.user_id not in User.user_ids:
            User.user_ids[self.user_id] = {}
            User.user_ids[self.user_id]['user_credibility'] = 5
            User.user_ids[self.user_id]['fakes'] = 0

    @classmethod
    def load_data(cls):
        try:
            with open("user_data.json", "r") as f:
                cls.user_ids = json.load(f)

        except FileNotFoundError:
            cls.user_ids = {}
            cls.save_data()
        return cls.user_ids

    @classmethod
    def save_data(cls):
        with open("user_data.json", "w") as f:
            json.dump(User.user_ids, f)

    def set_credibility(self, credibility):
        User.user_ids[self.user_id]['user_credibility'] = credibility

    def get_credibility(self):
        return User.user_ids[self.user_id]['user_credibility']

    def set_fakes(self, fakes):
        User.user_ids[self.user_id]['fakes'] = fakes

    def get_fakes(self):
        return User.user_ids[self.user_id]['fakes']


class Feedback:
    feedback = []

    @classmethod
    def load_data(cls):
        try:
            with open("verified_ratings.json", "r") as f:
                cls.feedback = json.load(f)
        except FileNotFoundError:
            cls.feedback = []
            cls.save_data()
        return cls.feedback

    @classmethod
    def save_data(cls):
        with open("verified_ratings.json", "w") as f:
            json.dump(Feedback.feedback, f)

    def __init__(self, service_id, user_id, rating, timestamp):
        Feedback.feedback = Feedback.load_data()

        new_rating = {"service_id": service_id, "user_id": user_id, "rating": rating, "timestamp": str(timestamp)}
        for feedback in Feedback.feedback:
            if feedback["service_id"] == service_id and feedback["user_id"] == user_id and feedback["rating"] == rating and feedback["timestamp"] == str(timestamp):
                return
        Feedback.feedback.append(new_rating)
