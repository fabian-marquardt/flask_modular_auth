from .abstract import AbstractAuthProvider, AbstractUnauthenticatedEntity
from .utils import _context_processor
from flask import _request_ctx_stack


class AuthManager:
    def __init__(self, app=None, unauthorized_callback=None):
        self._auth_providers = []
        self.unauthenticated_entity_class = AbstractUnauthenticatedEntity
        self._unauthorized_callback = unauthorized_callback

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.auth_manager = self
        app.context_processor(_context_processor)

    def unauthorized(self):
        if self._unauthorized_callback:
            return self._unauthorized_callback()
        else:
            return 'Not authorized', 403

    def get_auth_providers(self):
        """
        Get a list of all registered authentication providers.

        :return:List of authentication providers
        """
        return self._auth_providers

    def register_auth_provider(self, auth_provider):
        """
        Register an authentication provider with the manager.
        :param auth_provider: A valid authentication provider (i.e. an instance of a subclass of AbstractAuthenticationProvider)
        """
        if type(auth_provider) == AbstractAuthProvider:
            raise RuntimeError('Tried to add AbstractAuthProvider. Please add an implementing subclass object instead.')
        elif not isinstance(auth_provider, AbstractAuthProvider):
            raise ValueError('Tried to add an object which is no valid AuthProvider. Object should be instantiated from a subclass of AbstractAuthProvider.')
        else:
            self._auth_providers.append(auth_provider)

    def _load_authenticated_entity(self):
        ctx = _request_ctx_stack.top
        if not self._auth_providers:
            raise RuntimeError('Please register at least one authentication provider to get authenticated entities.')
        for auth_provider in self._auth_providers:
            entity = auth_provider.get_authenticated_entity()
            if entity:
                ctx.authenticated_entity = entity
                return True
        ctx.authenticated_entity = self.unauthenticated_entity_class()
        return False
