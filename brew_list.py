
import os, sys
import subprocess, os
from plumbum import local
import json
import jmespath

def update_environ(envvar: str):
	VAR = (
		subprocess.check_output(["bash", "--login", "-c", f"echo ${envvar}"]).decode().strip()
	)
	os.environ[envvar] = VAR
	return VAR

PATH = update_environ('PATH')
local.env.update({"PATH": PATH})
local.env._update_path()

def formula(local) -> list:
  """Return brew list with summaries
  
  :param: plumbum.machines.base.BaseMachine local
  """
  loc = local['brew']['info', '--installed', '--json']
  code, out, err = loc.run()
  if code != 0 or not out:
    raise Exception('Couldn't do brew!'')
  if out:
    stdout = json.loads(out)
  
  assert isinstance(stdout, list)
  table = jmespath.search('[].[name, desc]', j)
  if table:
    return table

# graphs = ['scipy', 'couchdb', 'redis', 'mongodb-community', 'apache-spark', 'sqlite3']




  
  
  
  
  