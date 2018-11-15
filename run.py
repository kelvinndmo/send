import os
from app import create_app

app=create_app(os.getenv("CONFIG_STAGE") or "default")

if __name__ == '__main__':
    app.run(debug=True)