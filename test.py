from pykeepass import PyKeePass
import getpass
import requests

password = getpass.getpass(prompt='Password: ', stream=None) 
kp = PyKeePass('Database.kdbx', password)
group = kp.find_groups(name='Datadog', first=True)

entry = kp.find_entries(title='Sandbox API key', first=True)
DD_API_KEY = entry.password
entry = kp.find_entries(title='Sandbox Application key', first=True)
DD_APP_KEY = entry.password

#api_endpoint = "https://api.datadoghq.com/api/v1/monitor"
api_endpoint = "https://api.datadoghq.com/api/v1/org"

headers = {
"Accept": "application/json",
"DD-API-KEY": DD_API_KEY,
"DD-APPLICATION-KEY": DD_APP_KEY
}

response = requests.get(api_endpoint, headers=headers).json()
print(response)
