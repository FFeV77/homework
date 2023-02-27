from flask import Flask
import advert
import users


app = Flask(__name__)
app.secret_key = 'dev'
app.register_blueprint(advert.bp)
app.register_blueprint(users.bp)

app.run(debug=True)