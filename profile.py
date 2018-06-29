import cProfile
from werkzeug.contrib.profiler import ProfilerMiddleware
from gazetteer.app import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[25])
app.run(debug = True)
#restriction sur 25 fonctions lourdes, même si je ne suis pas certaine du nombre dans notre appself.

#non fonctionnel, j'arrive à installer pstat mais par cProfile ou profileself.
