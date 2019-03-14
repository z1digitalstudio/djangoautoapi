# AUTO Api

Automatic API REST creation  

# Installation

Install using `pip`...

    pip install djangoautoapi

Please, note that you also need to have djangorestframework on your project.

Add `'autoapi'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'autoapi',
    )

Add a route to your auto-generated API.

    urlpatterns = [
        ...
        path('api/', include('autoapi.urls')),
    ]
