'''This file is used to run the flask application'''
from Backend import create_app
if __name__ == "__main__":
    app = create_app()
    # runs the app in debug mode
    app.run(debug=True)