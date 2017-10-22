from models import User, db


def create_user(**kwargs):
  """
  Represents a user resource
  :param kwargs:
  :return: New user's Facebook id
  """
  new_user = User(**kwargs)
  db.session.add(new_user)
  db.session.commit()

  return new_user.facebook_id


def get_user(facebook_id):
  """
  Gets user information
  :param facebook_id:
  :return: User information
  """
  user = User.query.filter_by(
    facebook_id=facebook_id
  ).one_or_none()

  if user is None:
    return None

  return {
    "facebook_id": user.facebook_id,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "email": user.email,
    "image_link": user.image_link,
    "language": user.language.name,
    "country_of_origin": user.country_of_origin,
    "gender": user.gender,
    "bio": user.bio,
    "interest": user.interest,
    "role": user.role.name
  }
