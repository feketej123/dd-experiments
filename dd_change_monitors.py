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
api_endpoint = "https://api.datadoghq.com/api/v1/monitor"

headers = {
"Accept": "application/json",
"DD-API-KEY": DD_API_KEY,
"DD-APPLICATION-KEY": DD_APP_KEY
}

response = requests.get(api_endpoint, headers=headers).json()

for monitor in response:
#    print(str(monitor).encode("utf-8"))
  monitor_id = monitor["id"]

  if "datadog-moog2-acceptance" in monitor["message"]:
    monitor["message"] = monitor["message"].replace('@webhook-datadog-moog2-acceptance', '@webhook-incident-acceptance')

    monitor_endpoint = f"{api_endpoint}/{monitor_id}"

    response = requests.put(
    monitor_endpoint,
    headers=headers,
    json=monitor
    )
    print(monitor_id)
    print(response.json())