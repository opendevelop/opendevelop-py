# OpenDevelop Python wrapper

## Installation
Installation of the OpenDevelop Python wrapper can be done using pip.

	pip install opendevelop

## Usage

### Initiate client
Initiates the OpenDevelop client. It gets 3 optional parameters;

* `host = os.getenv('OPENDEVELOP_HOST')`
* `client_id = os.getenv('OPENDEVELOP_CLIENT_ID')`
* `client_secret = os.getenv('OPENDEVELOP_CLIENT_SECRET')`

	from opendevelop import OpenDevelop	
	client = OpenDevelop()
	
### Get available images
Returns a Python list with the available images for the current OpenDevelop installation

	images = client.images()
	
#### Example response
	[u'base']

### Create a sandbox
Creates a sandbox and executes the given commands inside it. It returns the slug of the sandbox is Python string format.

	sandbox_slug = client.create_sandbox(image='base', cmd='ls -l ')
	
#### Example response
	 u'19cc2425738661a6'
	
### Create a sandbox with some files inside
Creates a sandbox, uploads the files, that correspond to the given **absolute** file paths, to it 
and executes the given commands inside it. It returns the slug of the sandbox is Python string format.

	sandbox_slug = client.create_sandbox(image='base', cmd='python hello.py', files=['/home/user/Desktop/hello.py'])
	
#### Example response
	u'a4eb0e47e8e51724'
	
### Get status and logs of a sandbox
Returns information about the sandbox identified by the given slug. Returns the data in Python dict format.

	data = client.sandbox(sandbox_log)

#### Example response
	{u'cmd': u'["python hello.py"]',
	 u'image': u'base',
	 u'logs': u'Hello OpenDevelop!\n',
	 u'return_code': 0,
	 u'status': u'terminated'}
