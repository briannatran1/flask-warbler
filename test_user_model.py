"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follow

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_is_following(self):
        """Tests is_following method."""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)

        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    def test_is_followed_by(self):
        """Tests is_followed_by method."""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)
        #TODO: commit every time append/do changes to db

        self.assertFalse(u1.is_followed_by(u2))
        self.assertTrue(u2.is_followed_by(u1))

    def test_user_signup_success(self):
        """Tests User.signup success."""

        u3 = User.signup("u3", "u3@email.com", "password", None)

        self.assertIsInstance(u3, User)
        #TODO: u3 has properties we expect

    def test_user_signup_fail(self):
        """Tests User.signup fail."""

        u4 = User.signup("u1", "u1@email.com", "password", None)

        # non-unique username/email raises IntegrityError upon trying to commit
        self.assertRaises(IntegrityError, db.session.commit)

        #TODO: separate test
        # missing password raises TypeError when trying to call User.signup
        self.assertRaises(TypeError, User.signup, "u666", "u666@email.com")

    def test_user_authenticate(self):
        """Tests User.authenticate."""

        self.assertIsInstance(User.authenticate("u1", "password"), User) #TODO: check correct user not just a user

        #TODO: separate test
        self.assertFalse(User.authenticate("u1", "123456"))
        self.assertFalse(User.authenticate("u3", "password"))
