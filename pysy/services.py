from com.android.volley import Request
from com.android.volley import Response
from com.android.volley import toolbox
from com.android.volley.toolbox import Volley
from org.json import JSONObject
from java.util import HashMap
from .server import host, port

base_url = 'https://' + str(host) + '/api'

class OnResponse(implements=com.android.volley.Response[Listener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onResponse(self, response: java.lang.Object) -> void:
        self.callback(*self.args, **self.kwargs, res=response)

class OnError(implements=com.android.volley.Response[ErrorListener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onErrorResponse(self, error: com.android.volley.VolleyError) -> void:
        self.callback(*self.args, **self.kwargs, err=error)

class api():
    def __init__(self, activity):
        self.queue = Volley.newRequestQueue(activity)
        self.token = None
        self.url_login = base_url + '/api-token-auth/'
        self.url_doctors = base_url + '/doctors'
        self.url_patients = base_url + '/patients'
        self.url_appointments = base_url + '/appointments'

    def asHashMap(self, d):
        r = HashMap()
        for k, v in d.items():
            r.put(k, v)
        return r

    def login(self, username, password, listener=None, listenerError=None):
        username = str(username)
        password = str(password)

        credentials = JSONObject()
        credentials.put('username', username)
        credentials.put('password', password)

        loginRequest = toolbox.JsonObjectRequest(
            Request.Method.POST,
            self.url_login,
            credentials,
            OnResponse(listener),
            OnError(listenerError)
        )

        self.queue.add(loginRequest)

    def setToken(self, token):
        self.token = 'Token ' + token
        self.headers = {'Authorization': self.token}

    def getDoctors(self, listener=None, listenerError=None):
        doctorsRequest = toolbox.StringRequest(
            Request.Method.GET,
            self.url_doctors,
            OnResponse(listener),
            OnError(listenerError),
            self.asHashMap(self.headers)
        )
        self.queue.add(doctorsRequest)

