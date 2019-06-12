# cPME-API

Cloud Prisma Margin Estimator (cPME) calculates margin for an uploaded portfolio according to Eurex Prisma methodology. The application is available to both members and non-members of Eurex Exchange of Deutsche Boerse Group. It can be accessed via web user interface, see cPME GUI or directly through API, described here.

- **[cPME API definition at SwaggerHub](https://app.swaggerhub.com/apis-docs/dbgservice/cPME/1.0)**
- **[DBG Digital Business Platform - gateway for accessing the API](https://console.developer.deutsche-boerse.com/)**
- **[cPME GUI](https://eurexmargins.prod.dbgservice.com)**, [GUI User Guide](docs/gui.md)

# Know Limitations

- does not support cash market (equities, bonds, ...)
- does not support FX swaps and inflation swaps
- does not support new flexible contracts, only the ones that already exist

# FAQ

## Comparison to Other Margin Calculation Tools

### Summary

feature / tool         | cPME API      | cPME GUI | OpenGamma PME | Online Margin Calculator
--- | --- | --- | --- | ---
Eurex products (ETD)   | yes           | yes           | yes           | yes
OTC interest rate trades | yes         | yes           | yes           | yes
OTC FX trades          | no            | no            | no            | yes
historical calculation | yes           | no            | yes           | yes
intraday calculation   | yes           | yes           | no            | yes
can run locally        | no            | no            | yes           | no
replicates production values | ETD     | ETD           | ETD           | ETD and OTC

### What is the differenece to cPME GUI?

The GUI is using the cPME API as well, but not every API feature is provided by the GUI.

### What is the advantage over OpenGamma PME?

No need to install, upgrade and maintain the software. You do not have to provide Transparency Enablers every day as an input.

### What is the advantage over Online Margin Calculator?

cPME provides API also for Eurex ETD, whereas Margin Calculator offers API only for OTC.

## Submitting Calculation Request

### Can cPME calculate margin for all instruments?

No, cash market instruments (equities, bonds, subscription rights) are not in scope. cPME can evaluate derivatives, both exchange traded (ETD) and OTC interest rate instruments.

Other OTC instruments, such as inflation swaps and FX swaps, are not yet supported.

### What to do when the request fails for a big portfolio?

Especially the XML formats of portfolio can be quite large which can cause connection problems. Try compressing the portfolio, see "Compressing request and response" in the [API definition](https://app.swaggerhub.com/apis-docs/dbgservice/cPME/1.0).

### What about flexible instruments?

Eurex clears also flexible contracts on futures and options (with non-standard expiry, strike or exercise style). If you have them in your real portfolio then cPME will calculate margin.
Hypothetical flexible contracts are not supported, cPME can price only existing contracts.

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

### How cross-margining works?

Fixed Income/Money Market positions and OTC IRS trades are both in PFI01 liquidation group. Without cross-margining, FI/MM positions are assigned to 2-day holding period split PFI01_HP2 and OTC trades are assigned to 5-day holding period split PFI01_HP5. Margin in each split is calculated independently. With cross-margining, some FI/MM positions are moved (or partially moved) to PFI01_HP5 split to offset the risk of OTC trades and lower the overall margin.

### How to validate cPME result against Eurex reports?

Compare the margin on liquidation group level against CC050 report. The margin on account level (CC060) cannot be obtained from cPME as the account may contain cash market instruments that are not in cPME scope.

### Is margin from simulation environment similar to production?

No, simulation (a.k.a. sandbox) uses different scenarios and has different prices than production, therefore it calculates different margin for the same portfolio.

## Security

### Where is cPME running?

cPME is deployed in Deutsche Boerse VPC (Virtual Private Cloud) within the Frankfurt region of Amazon Web Services.

### How is the communication designed, is it encrypted?

In essence cPME has a simple client-server architecture.
Client is either your browser or whatever you are making direct API calls from.
Server is the backend accepting API calls.
All communication between the backend and clients are running over HTTS.

### Are the requests or results archived?

On the backend side all calculations are done in memory only. No records are kept of the information processed.

### How do you ensure availability and disaster recovery?

cPME is stateless and highly elastic.
It runs in a highly-available Kubernetes cluster spread that is spread across three AWS Availability Zones.
