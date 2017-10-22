from models import User
from textblob import TextBlob
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import numpy

geolocator = Nominatim()


def matchup(facebook_id):
  """
  Creates a list of recommendations
  :param facebook_id:
  :return: [{mentor, mentor_bio, mentee, mentee_bio, similarity_score}]
  """
  def get_language_score(language):
    if language == User.LanguageEnum.english:
      return 1
    else:
      return 0

  def get_gender_score(gender):
    if gender == "male":
      return 1
    else:
      return 0

  user_instance = User.query.filter_by(
    facebook_id=facebook_id
  ).one_or_none()

  if user_instance is None:
    raise RuntimeError("User does not exist")

  if user_instance.role == User.RoleEnum.mentor:
    user_partition = User.query.filter_by(
      role=User.RoleEnum.mentee
    ).all()
  elif user_instance.role == User.RoleEnum.mentee:
    user_partition = User.query.filter_by(
      role=User.RoleEnum.mentor
    ).all()

  max_distance = float("-inf")
  user_location_score = 0
  user_language_score = get_language_score(user_instance.language)
  user_gender_score = get_gender_score(user_instance.gender)
  user_bio_score = \
    TextBlob(user_instance.bio).sentiment.polarity

  results = []

  for another_user in user_partition:
    user_location = \
      geolocator.geocode(user_instance.country_of_origin)
    another_user_location = \
      geolocator.geocode(another_user.country_of_origin)

    another_user_location_score = vincenty((
      another_user_location.latitude,
      another_user_location.longitude
    ), (
      user_location.latitude,
      user_location.longitude
    )
    )
    another_user_language_score = get_language_score(
      another_user.language
    )
    another_user_gender_score = get_gender_score(
      another_user.gender
    )
    another_user_bio_score = TextBlob(
      another_user.bio
    ).sentiment.polarity

    user_vector = numpy.array((
      user_location_score,
      user_language_score,
      user_gender_score,
      user_bio_score
    ))
    another_user_vector = numpy.array((
      another_user_location_score,
      another_user_language_score,
      another_user_gender_score,
      another_user_bio_score
    ))
    distance = numpy.linalg.norm(user_vector - another_user_vector)

    if distance > max_distance:
      max_distance = distance

    if another_user.role == User.RoleEnum.mentor:
      results.append({
        "mentor": another_user.id,
        "mentor_bio": another_user.bio,
        "mentee": user_instance.id,
        "mentee_bio": user_instance.bio,
        "similarity_score": distance
      })

  return results
