temple.js
=========

A micro-library for partial template loading with AJAX.

Depends on jQuery, and some simple backend sorcery.

serving needs
-------------

There are many ways to accomplish this, I chose to check for a 'stub' flag in request data sent to relevant views, prior to rendering the template. This manifest as a custom decorator I added on to Flask routes.
    
    def stubbable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ctx = f(*args, **kwargs)
        if ctx is None:
            ctx = {}
        elif isinstance(ctx, dict):
            ctx['stub'] = request.args.get('stub', False)
        return ctx
    return decorated_function

Use looks like this:

    @app.route('/blog')
    @templated('blog.html') # a decorator that accepts a context and returns a rendered template
    @stubbable
    def blog_view():
        ...
        return { ... }      # note that the custom decorator must intercept the context 
                            # before the template is rendered
                            
Finally, within your base template, wrap everything that isn't an empty block to be extended (i.e. not needed for the stub) in conditional tags:

    {% if not stub %}
    <html>
    <head>...</head>
    <body>
    {% endif %}
    {% block body %}
    {% endblock %}
    {% if not stub %}
    </body>
    </html>
    {% endif %}
    
Any templates that extend the base can now be rendered without the repetitive elements (essentially a conditional extension.)
        
