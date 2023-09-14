FROM grafana/grafana:latest

ENV GF_INSTALL_PLUGINS=yesoreyeram-infinity-datasource,volkovlabs-echarts-panel,grafana-github-datasource

# COPY grafana.ini /etc/grafana/grafana.ini
COPY provisioning/datasources /etc/grafana/provisioning/datasources
COPY provisioning/dashboards /etc/grafana/provisioning/dashboards