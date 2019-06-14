# cPME-API

Cloud Prisma Margin Estimator (cPME) calculates margin for an uploaded
portfolio according to [Eurex Prisma
methodology][prisma-methodology]. The application is available to both
members and non-members of Eurex Exchange of Deutsche Boerse Group. It
can be used via a [browser based GUI][cpme-gui], or via an API.

This repo contains documentation, exmaples and frequently asked
questions.

Key links:

- [cPME API definition at SwaggerHub][api-definition]
- [DBG Digital Business Platform][api-digital-business-platform] - gateway for accessing the
  API
- [cPME GUI][cpme-gui]
- [GUI User Guide](docs/gui.md)

# Know Limitations

- does not support cash market (equities, bonds, ...)
- does not support FX swaps and inflation swaps
- does not support new flexible contracts, only ones that already
  exist

# Frequently Asked Questions

## Comparison to other Eurex Clearing margin calculation tools

### Summary Table

| feature / tool               | cPME API | cPME GUI | OpenGamma PME | Online Margin Calculator |
|------------------------------|----------|----------|---------------|--------------------------|
| Eurex products (ETD)         | yes      | yes      | yes           | yes                      |
| OTC interest rate trades     | yes      | yes      | yes           | yes                      |
| OTC FX trades                | no       | no       | no            | yes                      |
| equities, bonds              | no       | no       | no            | no                       |
| historical calculation       | yes      | no       | yes           | yes                      |
| intraday calculation         | yes      | yes      | no            | yes                      |
| can run locally              | no       | no       | yes           | no                       |
| replicates production values | ETD      | ETD      | ETD           | ETD and OTC              |

### What is the difference between the cPME GUI and API?

The GUI is a browser front-end to the API, but not every API feature
is provided by the GUI.

### What is the advantage of cPME over OpenGamma PME?

cPME is a service provided by Deutsche Boerse/Eurex Clearing, no
need to install and maintain the software in-house. No need to provide
Transparency Enablers every day as an input.

### What is the advantage of cPME over Online Margin Calculator?

cPME provides an API also for Eurex Exchange Traded Derivatives,
whereas the Online Margin Calculator offers API only for OTC.

## Submitting a calculation request

### Can cPME calculate margin for all instruments?

No.

Cash market instruments (equities, bonds, subscription rights) are not
in scope.

cPME can evaluate derivatives, both exchange traded
(ETD) and OTC interest rate instruments.

Other OTC instruments, such as inflation swaps and FX swaps, are not
yet supported.

### What to do when a request fails for a big portfolio?

Especially XML formats of a portfolio can be quite large which can
cause connection problems. Try compressing the portfolio, see
"Compressing request and response" in the [API
definition][api-definition]

### What about flexible instruments?

Eurex Clearing clears flexible contracts on futures and options
(with non-standard expiry, strike or exercise style).

cPME can calculate margins on flexible contracts provided they exist
on the Eurex market. Hypothetical flexible contracts (eg: of
customers' own making) are not able to be processed by cPME.

### Is it possible to calculate margin as of historical date?

Yes, see "Business date and time" section in [API
definition][api-definition]. Historical data is available from March
18 2019.

Historical requests can take several minutes and might be refused if
cPME calculation cluster is busy as there is an upper limit on the
number of concurrent global historical calculations. In case your
request historical request is rejected try again in 15 minutes.

## Interpreting a margin result

### How precise is the margin?

For exchange traded derivatives, the margin is calculated by the same
module as in Eurex Clearing Prisma. The result on liquidation group
level should be exactly the same as on `CC050` report, if calculated for
the same date and time.

For OTC trades, the margin is approximated and can differ a few
percent from the real EurexOTC margin.

### What liquidation groups are there and what is liquidation group split?

List of liquidation groups and assignment of exchange traded products
to groups can be found at Eurex Clearing's [Risk Parameters
page][risk-parameters].

A liquidation group is further divided into splits, but currently only
`PFI01` liquidation group (Fixed Income, Money Market and OTC IRS) has
two splits, others have only one split.

### How does cross-margining work?

Fixed Income/Money Market positions and OTC IRS trades are both in
`PFI01` liquidation group. 

Without cross-margining, FI/MM positions are assigned to 2-day holding
period split `PFI01_HP2` and OTC trades are assigned to 5-day holding
period split `PFI01_HP5`. Margins in each split are calculated
independently. With cross-margining, some FI/MM positions are moved
(or partially moved) to `PFI01_HP5` split to offset the risk of OTC
trades and lower the overall margin.

### How to validate cPME result against Eurex reports?

Compare the margin on liquidation group level against `CC050`
report. The margin on account level (`CC060`) cannot be obtained from
cPME as the account may contain cash market instruments that are
currently supported by cPME.

### Is margin from simulation environment similar to production?

No.

Simulation (a.k.a. [sandbox on the Digital Business
Platform][api-digital-business-platform]) uses different scenarios
and has different prices than production, therefore it calculates a
different margin for the same portfolio.

## Security

### Where is cPME running?

cPME is deployed in Deutsche Boerse VPC (Virtual Private Cloud) within
the Frankfurt region of Amazon Web Services.

### How is the communication designed, is it encrypted?

In essence cPME has a client-server architecture.

Client is either your browser or whatever you are making direct API
calls from.  Server is the backend accepting API calls.  All
communication between the backend and clients are running over HTTPS.

### Are the requests or results archived?

On the backend side all calculations are done in memory only. No
records are kept of the information processed.

### How do you ensure availability and disaster recovery?

cPME is stateless, has a highly elastic architecture and fault
tolerant setup.

It runs in a highly-available Kubernetes cluster spread that is spread
across three AWS Availability Zones.


[api-definition]:https://app.swaggerhub.com/apis-docs/dbgservice/cPME/1.0
[api-digital-business-platform]:https://console.developer.deutsche-boerse.com/
[cpme-gui]:https://eurexmargins.prod.dbgservice.com
[prisma-methodology]:https://www.eurexclearing.com/resource/blob/32818/7bcf119060b658ad4e487f588744140d/data/brochure_eurex_clearing_prisma.pdf
[risk-parameters]:https://www.eurexclearing.com/clearing-en/risk-management/risk-parameters.
