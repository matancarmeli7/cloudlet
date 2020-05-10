Save your app under a folder with the name of your app, inside it make 2 folders:
1. build folder (code, docker file)
2. Yaml folder (all your configurations needed to deploy the app)

beside those files if you know you need any requierments/dependencies make sure to list them in a seperate file

	|-- apps
		└-- example-app
			|-- requierments.txt
			|-- build
			|	└-- code
			|		└-- ...py
			|	└-- Dockerfile
			└-- config
				└-- ...yml
					
	|-- dashboards
		└-- example-name.xml
