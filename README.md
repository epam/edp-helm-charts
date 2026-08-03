# KubeRocketCI - Helm Charts Repository

<img src="https://raw.githubusercontent.com/KubeRocketCI/docs/main/static/img/kuberocketci.png" width=150 height=150>

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache.2-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/epmdedp)](https://artifacthub.io/packages/search?repo=epmdedp)

Welcome to the KubeRocketCI charts repository.


>_**NOTE**: For more details on installing KubeRocketCI, please refer to the [Install KubeRocketCI](https://docs.kuberocketci.io/docs/quick-start/platform-installation) page._



## Add The Repository

```bash
helm repo add epamedp https://epam.github.io/edp-helm-charts/stable
helm repo update
```

or

```bash
helm repo add epamedp-snapshot https://epam.github.io/edp-helm-charts/snapshot
helm repo update
```

## Contribute

Do not hesitate to fork any repository and work on new features or bug fixes.

## Contact Us

Feel free to email us at SupportEPMD-EDP@epam.com for any issues.

## Description

This repository contains all EPAM Delivery Platform helm charts. Find here the release versions and the charts for development and testing.

Source code of helm charts:

* [cd-pipeline-operator](https://github.com/epam/edp-cd-pipeline-operator/tree/master/deploy-templates)
* [codebase-operator](https://github.com/epam/edp-codebase-operator/tree/master/deploy-templates)
* [edp-headlamp](https://github.com/epam/edp-headlamp/tree/master/deploy-templates)
* [edp-install](https://github.com/epam/edp-install/tree/master/deploy-templates)
* [gerrit-operator](https://github.com/epam/edp-gerrit-operator/tree/master/deploy-templates)
* [keycloak-operator](https://github.com/epam/edp-keycloak-operator/tree/master/deploy-templates)
* [nexus-operator](https://github.com/epam/edp-nexus-operator/tree/master/deploy-templates)
* [sonar-operator](https://github.com/epam/edp-sonar-operator/tree/master/deploy-templates)

## Current Testing

Helm3 is currently used for testing.

## License

[Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

### Related Articles

* [KubeRocketCI](https://docs.kuberocketci.io/)
