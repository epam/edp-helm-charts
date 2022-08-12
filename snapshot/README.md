# EPAM Delivery Platform - Helm Charts Repository

![https://raw.githubusercontent.com/epam/edp-install/master/docs/assets/logo.png](../images/logo.png)

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache.2-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/epmdedp)](https://artifacthub.io/packages/search?repo=epmdedp)

Welcome to the EPAM Delivery Platform charts repository.


>_**NOTE**: For more details on installing EDP, please refer to the [Install EDP](https://epam.github.io/edp-install/operator-guide/install-edp/) page._



## Add The Repository

```bash
helm repo add epamedp-snapshot https://epam.github.io/edp-helm-charts/snapshot
helm repo update
```

## Contribute

Do not hesitate to fork any repository and work on new features or bug fixes.

## Contact Us

Feel free to email us at SupportEPMD-EDP@epam.com for any issues.

## Description

This repository contains all EPAM Delivery Platform helm charts. Find here release versions and the charts for development and testing.

Source code of helm charts:

* [admin-console-operator](https://github.com/epam/edp-admin-console-operator/tree/master/deploy-templates)
* [cd-pipeline-operator](https://github.com/epam/edp-cd-pipeline-operator/tree/master/deploy-templates)
* [codebase-operator](https://github.com/epam/edp-codebase-operator/tree/master/deploy-templates)
* [edp-argocd-operator](https://github.com/epam/edp-argocd-operator/tree/master/deploy-templates)
* [edp-component-operator](https://github.com/epam/edp-component-operator/tree/master/deploy-templates)
* [edp-headlamp](https://github.com/epam/edp-headlamp/tree/master/deploy-templates)
* [edp-install](https://github.com/epam/edp-install/tree/master/deploy-templates)
* [gerrit-operator](https://github.com/epam/edp-gerrit-operator/tree/master/deploy-templates)
* [jenkins-operator](https://github.com/epam/edp-jenkins-operator/tree/master/deploy-templates)
* [keycloak-operator](https://github.com/epam/edp-keycloak-operator/tree/master/deploy-templates)
* [nexus-operator](https://github.com/epam/edp-nexus-operator/tree/master/deploy-templates)
* [perf-operator](https://github.com/epam/edp-perf-operator/tree/master/deploy-templates)
* [reconciler](https://github.com/epam/edp-reconciler/tree/master/deploy-templates)
* [sonar-operator](https://github.com/epam/edp-sonar-operator/tree/master/deploy-templates)

## Current Testing

Helm3 is currently used for testing.

## License

[Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

### Related Articles
* [EPAM Delivery Platform](https://epam.github.io/edp-install/)
* [Install EDP](https://epam.github.io/edp-install/operator-guide/install-edp/)
