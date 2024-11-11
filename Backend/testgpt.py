'''Handles Chatbot functionality, api calls, and evalutation'''
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# load_dotenv()
# OPENAI_KEY = os.getenv("OPENAI_KEY")
# llm = ChatOpenAI(api_key=OPENAI_KEY,
#              temperature=0.5,
#              model="gpt-4o-mini-2024-07-18")

def severity_determination(user_input: str) -> int:
    '''This method calls fine-tuned distilbert model to determine the severity of the user input'''
    model_path = os.path.join(os.getcwd(), "Backend/fine-tuned-model")
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    print("Model loaded")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print("Tokenizer loaded")
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=-1)
    print(predicted_class.item())
    return predicted_class.item()

def get_response(user_input: str, chat_history) -> str:
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    load_dotenv()
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    llm = ChatOpenAI(api_key=OPENAI_KEY,
                temperature=0.5,
                model="gpt-4o-mini-2024-07-18")
    severity = severity_determination(user_input)
    print("user input: ", user_input)
    if severity == 1 or severity == 0 or severity == 4 or severity == 3 or severity == 2:
        prompt = ChatPromptTemplate(
            input_variables=["Severity", "Content"],
            messages=[
                ("ai",
                """You are acting as a therapist for a user. After they have described their problem, you should respond with a message that is empathetic and understanding. The user's problem is: {Content}.
                The severity of the problem is: {Severity} This severity is on a scale from 0-4, with 0 being good and 4 being suicidal. Re-evaluate the severity of the problem state the severity at the end.
                If the severity is a 4 give the user local emergency resources, and be as empathetic and understanding as possible this is a crisis situation.
                But be sure to inform the user that you are not a professional therapist and that they should seek professional help if they are in crisis.
                Structure your response in JSON formate being "Severity": Number, "Response": "Your response here"."""),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{Content}")
            ]
        )
        chain = prompt | llm
        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: chat_history,
            input_messages_key="Content",
            history_messages_key="history"
        )
        response = chain_with_history.invoke({"Severity": severity, 
                                       "Content": user_input},
                                      config={"configurable": {"session_id": chat_history.session_id}})
        print(response)
        return response
    
    elif severity == 3:
        prompt = ChatPromptTemplate(
            input_variables=["Severity", "Content"],
            messages=[
                ("ai",
                """You are acting as a therapist for a user. After they have described their problem, you should respond with a message that is empathetic and understanding. The user's problem is: {Content}.
                The severity of the problem is: {Severity}, confirm the severity of the problem and re-evaluate if needed, the scale is 0-4 with 0 being good and 4 being suicidal.
                If the severity is a 3 be extremely empathetic, act as a therapist who is trying to help the user through a difficult time, while also being aware this is the early stages of a crisis.
                But be sure to inform the user that you are not a professional therapist and that they should seek professional help if they are in crisis.
                Structure your response in JSON formate being "Severity": Number, "Response": "Your response here"."""),
                ("human", "{Content}")
            ]
        )
        chain = prompt | llm
        response = chain.invoke({"Severity": severity, "Content": user_input})
        print(response)
        return response
    elif severity == 2:
        prompt = ChatPromptTemplate(
            input_variables=["Severity", "Content"],
            messages=[
                ("ai",
                """You are acting as a therapist for a user. After they have described their problem, you should respond with a message that is empathetic and understanding. The user's problem is: {Content}.
                The severity of the problem is: {Severity}, confirm the severity of the problem and re-evaluate if needed, the scale is 0-4 with 0 being good and 4 being suicidal.
                If the severity is a 2 be empathetic, act as a therapist who is helping a client who is going through a time of moderate difficulty.
                Approch the situation with empathy and understanding, while also providing solutions and advice in a professional manner but friendly manner.
                But be sure to inform the user that you are not a professional therapist and that they should seek professional help if they are in crisis.
                Structure your response in JSON formate being "Severity": Number, "Response": "Your response here"."""),
                ("human", "{Content}")
            ]
        )
        chain = prompt | llm
        response = chain.invoke({"Severity": severity, "Content": user_input})
        print(response)
        return response
    elif severity == 4:
        prompt = ChatPromptTemplate(
            input_variables=["Severity", "Content"],
            messages=[
                ("ai",
                """You are acting as a therapist for a user. After they have described their problem, you should respond with a message that is empathetic and understanding. The user's problem is: {Content}.
                The severity of the problem is: {Severity}, confirm the severity of the problem and re-evaluate if needed, the scale is 0-4 with 0 being good and 4 being suicidal.
                If the severity is a 1 act as a professional guide for the user, they may not currently be going through a difficult time but are looking for general life advice from a professional.
                Approch the situation with empathy and understanding, while also providing solutions and advice in a professional manner but friendly manner.
                But be sure to inform the user that you are not a professional therapist and that they should seek professional help if they are in crisis.
                Structure your response in JSON formate being "Severity": Number, "Response": "Your response here"."""),
                ("human", "{Content}")
            ]
        )
        chain = prompt | llm
        response = chain.invoke({"Severity": severity, "Content": user_input})
        print(response)
    else:
        prompt = ChatPromptTemplate(
            input_variables=["Severity", "Content"],
            messages=[
                ("ai",
                """You are acting as a therapist for a user. After they have described their problem, you should respond with a message that is empathetic and understanding. The user's problem is: {Content}.
                The severity of the problem is: {Severity}, confirm the severity of the problem and re-evaluate if needed, the scale is 0-4 with 0 being good and 4 being suicidal.
                If the severity is a 0 act as a professional guide for the user, they may not currently be going through a difficult time but are looking for general life advice from a professional.
                Approch the situation with empathy and understanding, while also providing solutions and advice in a professional manner but friendly manner.
                But be sure to inform the user that you are not a professional therapist and that they should seek professional help if they are in crisis.
                Structure your response in JSON formate being "Severity": Number, "Response": "Your response here"."""),
                ("human", "{Content}")
            ]
        )
        chain = prompt | llm
        response = chain.invoke({"Severity": severity, "Content": user_input})
        print(response)
    return response
