import copy

import pytz
from datetime import datetime, timezone
from fsrs import FSRS, Card, Rating
# from sqlalchemy.orm import Session
# from . import crud, schemas


# first_review_date = datetime(2022, 11, 29, 12, 30, 0, 0, tzinfo=timezone.utc)

class FSRSScheduler ():
    def __init__(self, flashcard_id, first_review_date):
        self.fsrs = FSRS()
        self.card = Card()
        self.flashcard_id = flashcard_id
        self.first_review_date:datetime = first_review_date
        self.review_history = []
        # self.ratings = []
        # self.ratings_date = []

    def get_next_review(self):
        now = copy.deepcopy(self.first_review_date)
        card_due = now
        logs = []
        print("FSRS LOGS", logs)
        for review in self.review_history:
            print(review)
            print(review["date"])
            print(review["date"].replace(tzinfo=timezone.utc))
            print(type(review["date"]))
            scheduling_cards = self.fsrs.repeat(self.card, review["date"].replace(tzinfo=timezone.utc))
            card = scheduling_cards[review["rating"]].card
            log = scheduling_cards[review["rating"]].review_log
            logs.append(vars(log))
            card_due = card.due
        return card_due

    def add_review(self, score, date):
        rating = self._convert_score_to_ratings(score)
        self.review_history.append({
            "rating": rating,
            "date": date
        })


    # def get_next_review(self):
    #     now = copy.deepcopy(self.first_review_date)
    #     logs = []
    #     print("FSRS LOGS", logs)
    #     for rating in self.ratings:
    #         print(now)
    #         print(type(now))
    #         scheduling_cards = self.fsrs.repeat(self.card, now)
    #         card = scheduling_cards[rating].card
    #         log = scheduling_cards[rating].review_log
    #         logs.append(vars(log))
    #         now = card.due
    #     return now

    # def add_review(self, score):
    #     rating = self._convert_score_to_ratings(score)
    #     self.ratings.append(rating)

    def _convert_score_to_ratings(self, score):
        if score == 3:
            return Rating.Easy
        elif score == 2:
            return Rating.Good
        elif score == 1:
            return Rating.Hard
        else:
            return Rating.Again
        

        
    