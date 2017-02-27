import requests
import time
import datetime
import json

configBase = {
    'url': 'https://quantumexperience.ng.bluemix.net/api'
}

class _Credentials():
    def __init__(self, token, config=None):
        self.tokenUnique = token
        if (config and config.get('url', None)):
            self.config = config
        else:
            self.config = configBase

        self.obtainToken()

    def obtainToken(self):
        self.dataCredentials = requests.post(self.config.get('url') + "/users/loginWithToken",
                                             data={'apiToken': self.tokenUnique}).json()

        if(not self.getToken()):
            print('ERROR: Not token valid')

    def getToken(self):
        return self.dataCredentials.get('id', None)

    def getUserId(self):
        return self.dataCredentials.get('userId', None)

    def getConfig(self):
        return self.config


class _Request():
    def __init__(self, token, config=None):
        self.credential = _Credentials(token, config)

    def checkToken(self, respond):
        if (respond.status_code == 401):
            self.credential.obtainToken()
            return False
        return True

    def post(self, path, params='', data={}):
        headers = {'Content-Type': 'application/json'}
        respond = requests.post(self.credential.config['url'] + path + '?access_token=' + self.credential.getToken() + params, data=data, headers=headers)
        if (not self.checkToken(respond)):
            respond = requests.post(self.credential.config['url'] + path + '?access_token=' + self.credential.getToken() + params, data=data, headers=headers)
        return respond.json()

    def get(self, path, params=''):
        respond = requests.get(self.credential.config['url'] + path + '?access_token=' + self.credential.getToken() + params)
        if (not self.checkToken(respond)):
            respond = requests.get(self.credential.config['url'] + path + '?access_token=' + self.credential.getToken() + params)
        return respond.json()


class IBMQuantumExperience():
    def __init__(self, token, config=None):
        self.req = _Request(token, config)

    def _checkCredentials(self):
        if (not self.req.credential.getToken()):
            return False
        return True

    def getExecution(self, id):
        if (not self._checkCredentials()):
            return None
        execution = self.req.get('/Executions/' + id, '')
        if (execution["codeId"]):
            url = self.req.get('/Codes/' + execution["codeId"] + '/export/png/url', '')
            execution['code'] = self.getCode(execution["codeId"])
        return execution

    def getResultFromExecution(self, id):
        if (not self._checkCredentials()):
            return None
        execution = self.req.get('/Executions/' + id, '')
        result = {}
        if ('result' in execution):
            if (execution["result"]["data"].get('p', None)):
                result["measure"] = execution["result"]["data"]["p"]
            if (execution["result"]["data"].get('valsxyz', None)):
                result["bloch"] = execution["result"]["data"]["valsxyz"]

        return result

    def getCode(self, id):
        if (not self._checkCredentials()):
            return None
        code = self.req.get('/Codes/' + id, '')
        executions = self.req.get('/Codes/' + id + '/executions', 'filter={"limit":3}')
        if (isinstance(executions, list)):
            code["executions"] = executions
        return code

    def getImageCode(self, id):
        if (not self._checkCredentials()):
            return None
        return self.req.get('/Codes/' + id + '/export/png/url', '')

    def getLastCodes(self):
        if (not self._checkCredentials()):
            return None
        return self.req.get('/users/' + self.req.credential.getUserId() + '/codes/lastest', '&includeExecutions=true')['codes']


    def runExperiment(self, qasm, device, shots, name=None, timeout=60):
        if (not self._checkCredentials()):
            return None
        data = {}
        qasm = qasm.replace('IBMQASM 2.0;', '')
        data['qasm'] = qasm
        data['codeType'] = 'QASM2'
        if name is None:
            name = 'Experiment #' + datetime.date.today().strftime("%Y%m%d%H%M%S")
        data['name'] = name
        deviceType = 'sim_trivial_2'
        if (device == 'real'):
            deviceType = 'real'
        execution = self.req.post('/codes/execute','&shots=' + str(shots) + '&deviceRunType=' + deviceType, json.dumps(data))
        respond = {}
        try:
            status = execution["status"]["id"]
            idExecution = execution["id"]
            result = {}
            respond["status"] = status
            respond["idExecution"] = idExecution
            respond["idCode"] = execution["codeId"]
            if (status == "DONE"):
                if (execution["result"]):
                    if (execution["result"]["data"].get('p', None)):
                        result["measure"] = execution["result"]["data"]["p"]
                    if (execution["result"]["data"].get('valsxyz', None)):
                        result["bloch"] = execution["result"]["data"]["valsxyz"]
                    respond["result"] = result
                    return respond
            elif (status == "ERROR"):
                return respond
            else:
                if (timeout):
                    if (timeout > 300):
                        timeout = 300
                    for i in range (1, timeout):
                        print("Waiting for results...")
                        result = self.getResultFromExecution(idExecution)
                        if (len(result) > 0):
                            respond["status"] = 'DONE'
                            respond["result"] = result
                            return respond
                        else:
                            time.sleep(2)
                    return respond
                else:
                    return respond
        except Exception:
            respond["error"] = execution
            return respond

    def runJob(self, qasms, device='simulator', shots=1, maxCredits=3):
        if (not self._checkCredentials()):
            return None
        data = {}
        for qasm in qasms:
            qasm['qasm'] = qasm['qasm'].replace('IBMQASM 2.0;', '')
        data['qasms'] = qasms
        data['shots'] = shots
        data['maxCredits'] = maxCredits
        data['backend'] = {}
        data['backend']['name'] = 'simulator'
        if (device == 'real'):
            data['backend']['name'] = 'real'

        job = self.req.post('/Jobs', data=json.dumps(data))
        return job

    def getJob(self, idJob):
        if (not self._checkCredentials() or not idJob):
            return None
        job = self.req.get('/Jobs/'+idJob)
        return job
