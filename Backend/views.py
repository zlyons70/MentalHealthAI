'''Manages the home page of application'''
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from .models import User, Message
from . import db
from .testgpt import get_response
from .memory_manage import get_chat_history
views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    '''Simple home page for the application'''
    if request.method == "POST":
        # when there is a post method we add the message to the database
        print("post request in views home")
        user_message = request.form.get("user_message")
        if user_message:
            chat_history = get_chat_history()
            print("chat history")
            print(chat_history)
            print("user message")
            print(user_message)
            message = Message(content=user_message, 
                              user_id=current_user.id,
                              session_id=chat_history.session_id)
            db.session.add(message)
            # get the response from the model, add to db ands send to frontend
            ai_response = get_response(user_message, chat_history)
            print(ai_response)
            ai_message = Message(content=ai_response.content, 
                                 is_ai=True, 
                                 user_id=current_user.id,
                                 session_id=chat_history.session_id)
            db.session.add(ai_message)            
            db.session.commit()
    print("At the home page")
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.id,).all()
    print(messages)
    return render_template("home.html", messages=messages) 