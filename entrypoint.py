from flask import Flask, request, Response, jsonify
from flask_migrate import Migrate
from app import \
  user_controller, \
  conversation_controller, \
  matchup_controller
from app.models import db
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask("catalyzapp")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/user", methods=["POST"])
def create_user_endpoint():
  json_body = request.get_json(force=True)

  try:
    logger.info("POST /user %s" % json_body)
    user_controller.create_user(**json_body)
    return Response(status=200)
  except Exception as e:
    logger.error(e.message)
    return Response(status=400)


@app.route("/user/<int:facebook_id>", methods=["GET"])
def get_user_endpoint(facebook_id):
  logger.info("GET /user %s" % facebook_id)
  user = user_controller.get_user(facebook_id=facebook_id)

  if user is None:
    return Response(status=400)

  response = jsonify(user)
  response.status_code = 200
  return response


@app.route("/matchup", methods=["POST"])
def get_matchup_endpoint():
  json_body = request.get_json(force=True)
  logger.info("POST /matchup %s" % json_body)

  facebook_id = json_body.get("facebook_id")
  if facebook_id is None:
    return Response(status=400)

  try:
    response = jsonify(
      matchup_controller.matchup(facebook_id=facebook_id)
    )
    response.status_code = 200
    return response
  except Exception as e:
    logger.error("%s" % e.message)
    return Response(status=400)


@app.route("/conversation", methods=["POST"])
def get_conversation_endpoint():
  json_body = request.get_json(force=True)
  logger.info("GET /conversation %s" % json_body)

  mentor_facebook_id = json_body.get("mentor")
  mentee_facebook_id = json_body.get("mentee")
  if mentor_facebook_id is None or mentee_facebook_id is None:
    return Response(status=400)

  try:
    response = jsonify(conversation_controller.get_conversation(
      mentor=mentor_facebook_id,
      mentee=mentee_facebook_id
    ))
    response.status_code = 200
    return response
  except Exception:
    return Response(status=400)


@app.route("/history", methods=["POST"])
def get_history_endpoint():
  json_body = request.get_json(force=True)
  logger.info("POST /history %s" % json_body)

  facebook_id = json_body.get("facebook_id")
  if facebook_id is None:
    return Response(status=400)

  response = jsonify(conversation_controller.get_conversation_history(
    facebook_id=facebook_id
  ))
  response.status_code = 200
  return response


@app.route("/message", methods=["POST"])
def create_message_endpoint():
  json_body = request.get_json(force=True)
  logger.info("POST /message %s" % json_body)

  mentor = json_body.get("mentor")
  mentee = json_body.get("mentee")
  sent_by = json_body.get("sent_by")
  message = json_body.get("message")

  if mentor is None or \
          mentee is None or \
          sent_by is None or \
          message is None:
    return Response(status=400)

  try:
    conversation_controller.new_message(
      mentor=mentor,
      mentee=mentee,
      sent_by=sent_by,
      message=message
    )
    return Response(status=200)
  except Exception as e:
    logger.error(e.message)
    return Response(status=400)

if __name__ == "__main__":
  app.run()
