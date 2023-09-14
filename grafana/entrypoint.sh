set -ex

if [[ -n "${DEX_URL}" ]]; then
    mkdir -p /etc/grafana/provisioning/
    cp -r /etc/grafana/provisioning.template/* /etc/grafana/provisioning/

    find /etc/grafana/provisioning/ -type f -exec sed -i -e "s!{{DEX_URL}}!${DEX_URL}!g" {} \;
    find /etc/grafana/provisioning/ -type f
    grep -R DEX_URL /etc/grafana/provisioning/ || true
fi

set +x
/run.sh "$@"