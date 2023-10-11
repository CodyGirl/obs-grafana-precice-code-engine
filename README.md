# MasterThesis-Precice

This project aims at providing a solution to better manage the code repositories for modular project structures.

## Project Structure and Instructions

### Backend

- Language: Python
- REST APIs are created using Flask framework
- Starting point is the 'dependencyAPI.py' file
- To start the backend individually run ```python3 dependencyAPI.py```
- To build a docker image run ```docker build -t precice-obs-backend-python .```

### Frontend

- Tool: Grafana
- Plugins used: yesoreyeram-infinity-datasource,volkovlabs-echarts-panel,grafana-github-datasource
- Authentication done via GitHub OAuth application
- To build a docker image run ```docker build -t precice-obs-grafana .```

### Environment

Create a .env file in the root directory with the following fields:

- GF_SECURITY_ADMIN_USER=
- GF_SECURITY_ADMIN_PASSWORD=
- GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH=```/etc/grafana/provisioning/dashboards/{name_of_the_dashboardconfig_file}```
- GF_SERVER_ROOT_URL=[http://localhost:3000](http://localhost:3000)
- GTOKEN={github_personal_access_token}
- GHE_CLIENT_SECRET={github_oauth_application_client_secret}
- GHE_CLIENT_ID={github_oauth_application_client_id}
- CE_APP={cloud_env_app_name}
- CE_SUBDOMAIN={cloud_env_sub_domain}
- CE_DOMAIN={cloud_env_domain}

All these parameters are configurable, do not forget to change them as the environment changes.

### Instructions to run the application

Once both the images are ready, the application can be started using the docker-compose file.

- Go to the base directory
- Make sure to have proper environment variables in a .env file.
- Run ```docker-compose up```
