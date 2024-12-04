'''Manages the home page of application'''
from flask import Blueprint, request, jsonify, render_template, session
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
        prev_sev = session.get("prev_sev", 0)
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
            if prev_sev == 4:
                user_message = "what are local emergency resources for the city of " + user_message
            ai_response, severity = get_response(user_message, chat_history)
            session["prev_sev"] = severity
            print("USER_MESSAGE", user_message)
            print("AI RESPONSE")
            print("Transformer severity", severity)
            print("LLM response: ", ai_response)
            print("PREVIOUS SEVERITY: ", severity)
            ai_message = Message(content=ai_response.content, 
                                 is_ai=True, 
                                 user_id=current_user.id,
                                 session_id=chat_history.session_id)
            db.session.add(ai_message)            
            db.session.commit()
            # case where one of the severitys is 4
            if severity == 4 or ("Severity 4" in ai_response.content) or ("severity 4" in ai_response.content) or ("Severity: 4" in ai_response.content) or ("severity: 4" in ai_response.content):
                prev_sev = 4
                ai_message.content += " This message is deemed as a crisis situation please insert your location to get local emergency resources"
                return jsonify({"response": ai_message.content})
            return jsonify({"response": ai_message.content})
    print("At the home page")
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.id,).all()
    print(messages)
    return render_template("home.html", messages=messages) 