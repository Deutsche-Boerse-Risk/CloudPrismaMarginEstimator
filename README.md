# cPME-API

Cloud Prisma Margin Estimator (cPME) calculates margin for an uploaded portfolio according to Eurex Prisma methodology. The application is available to both members and non-members of Eurex Clearing. It can be accessed via web user interface, see cPME GUI or directly through API, described here.

- **[cPME API definition at SwaggerHub](https://app.swaggerhub.com/apis-docs/dbgservice/cPME/1.0)**
- **[DBG Digital Business Platform - gateway for accessing the API](https://console.developer.deutsche-boerse.com/)**
- **[cPME GUI](https://eurexmargins.prod.dbgservice.com)**

# FAQ

### How precise is the margin?

For exchange traded derivatives, the margin is calculated by the same module as in Eurex Clearing Prisma. The result on liquidation group level should be exactly the same as on CC050 report, if calculated for the same date and time.

For OTC trades, the margin is approximated and can differ a few percent from the real EurexOTC margin.

### What liquidation groups are there and what is liquidation group split?

List of liquidation groups and assignment of exchange traded products to groups can be found at [Risk Parameters page](https://www.eurexclearing.com/clearing-en/risk-management/risk-parameters).

Liquidation group is further divided into splits, but currently only PFI01 liquidation group (Fixed Income, Money Market and OTC IRS) has two splits, others have only one split.

