from django.apps import AppConfig

class BlogConfig(AppConfig):
    name = 'blog'

    # for signal
    def ready(self):
        import blog.signals