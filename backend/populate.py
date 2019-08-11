#!/usr/bin/env python3
import random
from datetime import date, timedelta, datetime

from app import app
from models.user import User
import requests


class RandomUser:
	def __init__(self):
		self.session = requests.Session()

	def get(self, **params):
		return self.session.get('https://randomuser.me/api/', params=params).json()

	def get_images(self, n: int):
		images = []
		while n > 0:
			r = self.session.get(f'https://dog.ceo/api/breeds/image/random/{min(n, 50)}')
			response_images = r.json().get('message', [])
			images += response_images
			n -= len(response_images)
		return images

	@staticmethod
	def get_random_tags():
		all_tags = ['42', 'eco', 'geek', 'veggie', 'music', 'travel']
		user_tags = []
		tags_amount = random.randint(0, len(all_tags))
		for i in range(tags_amount):
			user_tags.append(all_tags.pop(random.randint(0, len(all_tags) - 1)))
		return user_tags

	def create_users(self, **params):
		n = params.get('results', 1)
		images = self.get_images(n)
		users = []
		for fake in self.get(**params).get('results', []):
			user = User.from_dict({
				'first_name': fake.get('name', {}).get('first'),
				'last_name': fake.get('name', {}).get('last'),
				'username': fake.get('login', {}).get('username'),
				'email': fake.get('email', ''),
			})
			user.set_password(f"{fake.get('login', {}).get('username')}-PwD1!")
			print(f"Creating: {user.username}")
			user.create()
			user.tags = self.get_random_tags()
			if fake.get('dob', {}).get('date'):
				user.dob = datetime.strptime(fake['dob']['date'][:10], '%Y-%m-%d')
			user.gender = fake['gender'] if fake.get('gender') in ['female', 'male'] else None
			user.sex_pref = random.choice(['homo', 'hetero', 'bi'])
			user.profile_image = images.pop()
			user.activated = True
			user.last_connection = date.today() - timedelta(minutes=random.randint(1, 60 * 24 * 30 * 6))
			user.latitude = fake.get('location', {}).get('coordinates', {}).get('latitude')
			user.longitude = fake.get('location', {}).get('coordinates', {}).get('longitude')
			user.update()
			users.append(user)
		return users


def populate(n: int):
	print(f"Populating DB with {n} users")
	with app.app_context():
		params = {
			'results': n,
			'nat': 'fr',
		}
		RandomUser().create_users(**params)


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description="Populate DB with fake users")
	parser.add_argument('amount', type=int, help="how many users to add")
	args = parser.parse_args()
	populate(args.amount)
