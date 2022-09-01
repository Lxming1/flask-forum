from flask import Flask
from controllers.ct_home import xmHomeApi
from controllers.ct_profile import xmProfileApi
from controllers.ct_user import xmUserApi
from controllers.ct_avatar import xmAvatarApi
from utils.config import HOST, PORT, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(xmUserApi)
app.register_blueprint(xmHomeApi)
app.register_blueprint(xmAvatarApi)
app.register_blueprint(xmProfileApi)

if __name__ == '__main__':
  app.run(debug=True, host=HOST, port=PORT)
