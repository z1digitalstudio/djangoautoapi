from django.apps import apps

from rest_framework.schemas.generators import (
    EndpointEnumerator as DRFEndpointEnumerator,
    SchemaGenerator as DRFSchemaGenerator,
    LinkNode, insert_into)

from autoapi.utils import is_managed


class EndpointEnumerator(DRFEndpointEnumerator):

    def get_api_endpoints(self, patterns=None, prefix=''):
        endpoints = super(EndpointEnumerator, self).get_api_endpoints(
            patterns, prefix)

        result = []
        for path, method, callback in endpoints:
            if isinstance(path, tuple):
                result.append((path, method, callback))
                continue
            if ('{app_name}' in path and
                    '{model_name}' in path):
                for app, models in apps.all_models.items():
                    for model_name in models.keys():
                        if not is_managed(app, model_name):
                            continue
                        kwargs = {
                            'model_name': model_name,
                            'app_name': app,
                        }
                        new_path = path.replace(
                            '{model_name}', model_name).replace(
                                '{app_name}', app)
                        result.append(
                            ((new_path, kwargs), method, callback))
            else:
                result.append(
                    ((path, {}), method, callback))
        return result


class SchemaGenerator(DRFSchemaGenerator):

    endpoint_inspector_cls = EndpointEnumerator

    def get_links(self, request=None):
        """
        Return a dictionary containing all the links that should be
        included in the API schema.
        """
        links = LinkNode()

        # Generate (path, method, view) given (path, method, callback).
        paths = []
        view_endpoints = []
        for path_with_kwargs, method, callback in self.endpoints:
            path, kwargs = path_with_kwargs
            view = self.create_view(callback, method, request)
            view.kwargs = kwargs
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            link = view.schema.get_link(path, method, base_url=self.url)
            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)
            insert_into(links, keys, link)

        return links
