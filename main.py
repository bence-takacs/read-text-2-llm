from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from embedding import Embedding
import os


class MyApplication:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = './uploads'
        self.app.config['SECRET_KEY'] = 'your-secret-key'  # replace with a real secret key

        if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
            os.makedirs(self.app.config['UPLOAD_FOLDER'])

        filepath=os.path.join('.', 'state_of_the_union.txt')
        self.embedding= Embedding(filepath) # None
        self.setup_routes()


    def setup_routes(self):
        @self.app.route('/')
        def upload_file():
            return render_template('upload.html')

        @self.app.route('/', methods=['POST'])
        def save_file():
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath=os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            self.embedding = Embedding(filepath)
            return redirect(url_for('chat'))

        @self.app.route('/chat')
        def chat():
            return render_template('chat.html')

        @self.app.route('/chat', methods=['POST'])
        def respond_to_chat():
            user_message = request.form['message']
            # TODO: process the user's message and generate a response
            response = self.embedding.query(user_message) if self.embedding else "You should initialize knowledge base first"
            return render_template('chat.html', response=response)
        
    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    MyApplication().run()