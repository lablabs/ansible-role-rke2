from argparse import ArgumentParser
from requests import get
from subprocess import Popen, PIPE
from time import sleep
from psutil import net_connections
from random import randrange

arguments = ArgumentParser()
arguments.add_argument('--longhorn-service-name', dest='longhorn_service_name', type=str, help='Longhorn Kubernetes service name', default='services/longhorn-frontend')
arguments.add_argument('--namespace', dest='namespace', type=str, help='Longhorn namespace', default='longhorn-system')
arguments.add_argument('--kubectl_path', dest='kubectl_path', type=str, help='kubectl binary path', default='kubectl')
arguments.add_argument('--kubeconfig', dest='kubeconfig', type=str, help='kubeconfig file path', required=True)
arguments = arguments.parse_args()

def check_longhorn_volumes_state(longhorn_url :str) -> list | None :
  volumes = get(f"{longhorn_url}/v1/volumes")
  volumes.raise_for_status()
  volumes = volumes.json()

  unhealthy_volumes = []
  for single_volume in volumes['data']:
    if single_volume['robustness'] != 'healthy':
      unhealthy_volumes.append((single_volume['name'], single_volume['robustness']))

  if unhealthy_volumes:
    return unhealthy_volumes
  else:
    return None

used_listening_ports = []

for conn in net_connections(kind='inet'):
  if conn.status == 'LISTEN':
    used_listening_ports.append(conn.laddr.port) # type: ignore

random_pf_port = randrange(32770,65500)

while random_pf_port in used_listening_ports:
  random_pf_port = randrange(32770,65500)


command = [f"{arguments.kubectl_path}", "port-forward", f"{arguments.longhorn_service_name}", f"{random_pf_port}:http", "--namespace", f"{arguments.namespace}", "--kubeconfig", f"{arguments.kubeconfig}"]
process = Popen(command, stdout=PIPE, stderr=PIPE)

sleep(5)

try:
  unhealthy_volumes = check_longhorn_volumes_state(f"http://localhost:{random_pf_port}")

finally:
  process.terminate()
  process.wait()

if unhealthy_volumes:
  print("There are volumes that are not healthy:")
  for unhealthy in unhealthy_volumes:
    print(f"Volume [{unhealthy[0]}] is in state [{unhealthy[1]}]")
  exit(1)
else:
  exit(0)
