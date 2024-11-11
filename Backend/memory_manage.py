'''Handles memory management for chat history'''
'''Note that this file was done with the help of GitHub copilot'''
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List
from datetime import datetime
from flask_login import current_user
from flask import flash
from .models import Message
from . import db

class CustomMessageHistory(SQLChatMessageHistory):
    '''This class is used to store message history in the database'''
    def __init__(self, session_id: str):
        super().__init__(
            session_id=session_id,
            connection_string="sqlite:///instance/test.db",
        )
        self._messages: List[BaseMessage] = []
        self.session_id = session_id
        self._load_messages()
    
    def _load_messages(self) -> None:
        '''Load messages from database'''
        self._messages.clear()
        msgs = Message.query.filter_by(
            user_id=current_user.id,
            session_id=self.session_id
        ).distinct(Message.timestamp).all()
        
        self._messages = [
            AIMessage(content=msg.content) if msg.is_ai 
            else HumanMessage(content=msg.content)
            for msg in msgs
        ]
    
    @property
    def messages(self) -> List[BaseMessage]:
        '''Returns copy of messages for RunnableHistory function'''
        return self._messages.copy()
    
    def add_message(self, message: BaseMessage) -> None:
        '''Add a message to the store'''
        msg = Message(
            content=message.content,
            is_ai=isinstance(message, AIMessage),
            user_id=current_user.id,
            session_id=self.session_id
        )
        db.session.add(msg)
        db.session.commit()
        self._messages.append(message)
    
    def clear(self) -> None:
        '''Clears the chat history'''
        Message.query.filter_by(
            user_id=current_user.id,
            session_id=self.session_id
        ).delete()
        db.session.commit()
        self._messages.clear()

def get_chat_history():
    '''Returns chat history for the current user'''
    if not current_user:
        flash("Authentication Error")
        return None
    
    session_id = f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d')}"
    return CustomMessageHistory(session_id=session_id)