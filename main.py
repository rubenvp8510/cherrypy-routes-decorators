import cherrypy
import inspect

dispatcher = cherrypy.dispatch.RoutesDispatcher()

def path(path):
    def path_decorator(func):
        func.path = path
        return func
    return path_decorator

def get(func):
    if not hasattr(func,'method'):
        func.method = []
    if 'GET' not in func.method:
        func.method.append('GET')
    return func

def post(func):
    if not hasattr(func,'method'):
        func.method = []
    if 'POST' not in func.method:
        func.method.append('POST')
    return func

def controller(path):
    def class_rebuilder(cls):
        if path is not None:
            cls.path = path
        else:
            cls.path = ''
        methods =  inspect.getmembers(cls, predicate=inspect.ismethod)
        for method in methods:
            name = method[0]
            fn = method[1]
            if not hasattr(fn,'path'):
                fn_path = name
            else:
                fn_path = fn.path
            final_path =  '/'.join([cls.path,fn_path])

            dispatcher.connect(cls.__name__,final_path,cls,action=name,
                                conditions={'method':fn.method})
        return cls
    return class_rebuilder



@controller('')
class HelloWorld(object):
    @get
    @path('')
    def index(self):
        return "Hello world!"

    @post
    def testing(self):
        return 'testing'


if __name__ == '__main__':
    config = {
        '/': {
            'request.dispatch' : dispatcher,
        }
    }
    cherrypy.quickstart(HelloWorld(),config=config)
