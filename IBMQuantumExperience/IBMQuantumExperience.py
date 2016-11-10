import requests

baseURL = 'https://qcwi-develop.mybluemix.net/api'

class _Credentials():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.obtainToken()

    def obtainToken(self):
        self.dataCredentials = requests.post(baseURL + "/users/login",
                                             data={'email': self.email, 'password': self.password}).json()

    def getToken(self):
        return self.dataCredentials.get('id', None)

    def getUserId(self):
        return self.dataCredentials.get('userId', None)


class _Request():
    def __init__(self, email, password):
        self.credential = _Credentials(email, password)

    def checkToken(self, respond):
        if (respond.status_code == 401):
            self.credential.obtainToken()
            return False
        return True

    def post(self, path, params, data):
        respond = requests.post(baseURL + path + '?access_token=' + self.credential.getToken() + params, data=data)
        if (not self.checkToken(respond)):
            respond = requests.post(baseURL + path + '?access_token=' + self.credential.getToken() + params, data=data)
        return respond.json()

    def get(self, path, params):
        respond = requests.get(baseURL + path + '?access_token=' + self.credential.getToken() + params)
        if (not self.checkToken(respond)):
            respond = requests.get(baseURL + path + '?access_token=' + self.credential.getToken() + params)
        return respond.json()


class IBMQuantumExperience():
    def __init__(self, email, password):
        self.req = _Request(email, password)

    def getExecution(self, id):
        execution = self.req.get('/Executions/' + id, '')
        if (execution["codeId"]):
            url = self.req.get('/Codes/' + execution["codeId"] + '/export/png/url', '')
            execution['code'] = self.getCode(execution["codeId"])
        return execution

    def getResultFromExecution(self, id):
        execution = self.req.get('/Executions/' + id, '')
        result = {}
        if (execution["result"]):
            if (execution["result"]["data"].get('p', None)):
                result["measure"] = execution["result"]["data"]["p"]
            if (execution["result"]["data"].get('valsxyz', None)):
                result["bloch"] = execution["result"]["data"]["valsxyz"]

        return result

    def getCode(self, id):
        code = self.req.get('/Codes/' + id, '')
        executions = self.req.get('/Codes/' + id + '/executions', 'filter={"limit":3}')
        if (isinstance(executions, list)):
            code["executions"] = executions
        return code

    def getImageCode(self, id):
        return self.req.get('/Codes/' + id + '/export/png/url', '')


    def getLastCodes(self):
        return self.req.get('/users/' + self.req.credential.getUserId() + '/codes/lastest', '&includeExecutions=true')['codes']