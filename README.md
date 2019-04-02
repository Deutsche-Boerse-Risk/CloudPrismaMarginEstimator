# cPME-API

Cloud Prisma Margin Estimator (cPME) calculates margin for an uploaded portfolio according to Eurex Prisma methodology. The application is available to both members and non-members of Eurex Exchange of Deutsche Boerse Group. It can be accessed via web user interface, see cPME GUI or directly through API, described here.

- **[cPME API definition at SwaggerHub](https://app.swaggerhub.com/apis-docs/dbgservice/cPME/1.0)**
- **[DBG Digital Business Platform - gateway for accessing the API](https://console.developer.deutsche-boerse.com/)**
- **[cPME GUI](https://eurexmargins.prod.dbgservice.com)**

# FAQ

## Submitting Calculation Request

### Can cPME calculate margin for all instruments?

No, cash market instruments (equities, bonds, subscription rights) are not in scope. cPME can evaluate derivatives, both exchange traded (ETD) and OTC interest rate instruments.

Other OTC instruments, such as inflation swaps and FX swaps, are not yet supported.

### Is it possible to calculate margin as of historical date?

Yes, see "Business date and time" section in [API definition](https://app.swaggerhub.com/apis-docs/dbgservice/cPME/1.0). The historical data are available from March 18 2019.

The request can take several minutes and it will be refused if the cluster is busy, in that case try again in 15 minutes.

## Interpreting Margin Result

### How precise is the margin?

For exchange traded derivatives, the margin is calculated by the same module as in Eurex Clearing Prisma. The result on liquidation group level should be exactly the same as on CC050 report, if calculated for the same date and time.

For OTC trades, the margin is approximated and can differ a few percent from the real EurexOTC margin.

### What liquidation groups are there and what is liquidation group split?

List of liquidation groups and assignment of exchange traded products to groups can be found at [Risk Parameters page](https://www.eurexclearing.com/clearing-en/risk-management/risk-parameters).

Liquidation group is further divided into splits, but currently only PFI01 liquidation group (Fixed Income, Money Market and OTC IRS) has two splits, others have only one split.

### How to validate cPME result against Eurex reports?

Compare the margin on liquidation group level against CC050 report. The margin on account level (CC060) cannot be obtained from cPME as the account may contain cash market instruments that are not in cPME scope.
