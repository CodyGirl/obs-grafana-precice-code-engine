FROM grafana/grafana:latest

ENV GF_INSTALL_PLUGINS=yesoreyeram-infinity-datasource,volkovlabs-echarts-panel,grafana-github-datasource
ENV GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH=/etc/grafana/provisioning/dashboards/DependencyDashboard.json

COPY grafana.ini /etc/grafana/grafana.ini
COPY provisioning /etc/grafana/provisioning.template

RUN chmod +x entrypoint.sh
COPY entrypoint.sh /entrypoint
ENTRYPOINT /entrypoint