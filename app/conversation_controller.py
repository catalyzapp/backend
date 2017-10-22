from datetime import datetime
import pytz
from models import Conversation, Message, User, db


def get_conversation(mentor, mentee):
  """
  Get the conversation between a mentor and a mentee
  :param mentor:
  :param mentee:
  :return: {timestamp, messages:[sent_by, message, timestamp]}
  """
  user_mentor = User.query.filter_by(
    facebook_id=mentor
  ).one_or_none()
  user_mentee = User.query.filter_by(
    facebook_id=mentee
  ).one_or_none()
  if user_mentor is None or user_mentee is None:
    raise RuntimeError("Mentor and/or mentee doesn't exist")

  if user_mentor.role != User.RoleEnum.mentor:
    raise RuntimeError("Provided mentor isn't a mentor")
  elif user_mentee.role != User.RoleEnum.mentee:
    raise RuntimeError("Provided mentee isn't a mentee")

  current_datetime = datetime.now(pytz.timezone('US/Pacific'))
  conversation = Conversation.query.filter_by(
    mentor=mentor,
    mentee=mentee
  ).one_or_none()

  if conversation is None:
    conversation = Conversation(
      mentor=mentor,
      mentee=mentee,
      timestamp=current_datetime
    )

    db.session.add(conversation)
    db.session.commit()
    messages_list = []
  else:
    messages_list = [
      {
        "sent_by": message.sent_by,
        "message": message.message,
        "timestamp": message.timestamp
      }
      for message in Message.query.filter_by(
        conversation_id=conversation.id
      ).order_by(Message.timestamp.asc()).all()]

  return {
    "timestamp": conversation.timestamp.isoformat(),
    "mentor": conversation.mentor,
    "mentee": conversation.mentee,
    "messages": messages_list
  }


def new_message(
    mentor,
    mentee,
    sent_by,
    message,
    timestamp=datetime.now(pytz.timezone('US/Pacific'))
):
  """
  Creates a new message
  :param conversation_id: int
  :param sent_by: string
  :param message: text
  :param timestamp: datetime
  :return:
  """
  conversation = Conversation.query.filter_by(
    mentor=mentor,
    mentee=mentee
  ).one_or_none()
  if conversation is None:
    raise RuntimeError("Conversation doesn't exist")

  message_object = Message(
    conversation_id=conversation.id,
    sent_by=sent_by,
    message=message,
    timestamp=timestamp
  )
  db.session.add(message_object)
  db.session.commit()


def get_conversation_history(facebook_id):
  """
  Get conversation history of a user with multiple users
  :param facebook_id: string
  :return: [{mentor, mentor_bio, mentee, mentee_bio, timestamp}]
  """
  user = User.query.filter_by(
    facebook_id=facebook_id
  ).one_or_none()

  conversation_list = []
  if user is None:
    return conversation_list

  if user.role is user.RoleEnum.mentee:
    conversation_list = Conversation.query.filter_by(
      mentee=user.facebook_id
    ).all()
  elif user.role is user.RoleEnum.mentor:
    conversation_list = Conversation.query.filter_by(
      mentor=user.facebook_id
    ).all()

  return [
    {
      "mentor": conversation.mentor,
      "mentor_bio": User.query.filter_by(
        facebook_id=conversation.mentor
      ).one_or_none().bio,
      "mentee": conversation.mentee,
      "mentee_bio": User.query.filter_by(
        facebook_id=conversation.mentee
      ).one_or_none().bio,
      "timestamp": conversation.timestamp.isoformat()
    } for conversation in conversation_list]
