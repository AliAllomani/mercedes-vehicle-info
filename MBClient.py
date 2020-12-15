from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

class MBClient:
    def __init__(self, client_id, client_secret,redirect_uri):
        self.oauth_auth_url = r'https://id.mercedes-benz.com/as/authorization.oauth2'
        self.oauth_token_url = r'https://id.mercedes-benz.com/as/token.oauth2'

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        self.access_token = None
        self.state = None

        self.scope = ['mb:vehicle:mbdata:vehiclestatus','mb:vehicle:mbdata:vehiclelock']

        self.client = None


    def init_client(self):
        self.client = OAuth2Session(self.client_id, token=self.access_token)

    def get_resource(self, resource_path):

        if not self.client:
            self.init_client()

        r = self.client.get(resource_path)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 204:
            return {'error': 'No data available for the past 12 hours', 'err_code': r.status_code}
        else:
            return {'error': str(r.content), 'err_code': r.status_code}

    def get_oauth_token(self,request_url):
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri,scope=self.scope, state=self.state)
        return oauth.fetch_token(self.oauth_token_url,
        authorization_response=request_url,
        auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )

    def login(self):
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri,scope=self.scope)
        return oauth.authorization_url(self.oauth_auth_url)
