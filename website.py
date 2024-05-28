#!/usr/bin/env python3


from webapp import app

from webapp.views.views import *


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
