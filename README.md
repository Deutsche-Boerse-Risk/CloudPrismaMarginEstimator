# Cloud Prisma Margin Estimator (CPME)

Cloud Prisma Margin Estimator (cPME) calculates portfolio margin according to the [Eurex Prisma
methodology][prisma-methodology]. The application is available to both
members and non-members of Eurex Clearing, a part of the Deutsche Boerse Group. It
can be used via a [browser based GUI][CPME-gui] or an API.

This repo contains documentation, examples and frequently asked
questions.

Key links:

- [CPME GUI][CPME-gui]
- [GUI User Guide](docs/gui.md)
- [CPME API definition at SwaggerHub][api-definition]
- [DBG Digital Business Platform][api-digital-business-platform] - gateway for accessing the
  API

# Known Limitations

- Does not support cash market (equities, bonds, ...)
- Does not support FX swaps
- Does not support new flexible contracts, only existing ones

# Frequently Asked Questions

## Comparing Eurex Clearing Margin Simulation Tools

### Summary Table

| feature / tool                  | CPME API        | CPME GUI        |  Online Margin Calculator |
|---------------------------------|-----------------|-----------------|---------------------------|
| Availability                    | Everyone        | Everyone        | Disclosed clients         |
| Asset classes covered:          |                 |                 |                           |
| - ETD                           | yes             | yes             | yes                       |
| - OTC IRS                       | yes             | yes             | yes                       |
| - OTC FX                        | no              | no              | yes                       |
| - OTC inflation                 | yes             | yes             | yes                       |
| - Cross-margining (ETD/OTC IRS) | yes             | yes             | yes                       |
| - Equities, bonds               | no              | no              | no                        |
| Input formats covered:          |                 |                 |                           |
| - Member reports                | yes             | yes             | yes                       |
| - CSV files                     | yes             | yes             | yes                       |
| - OTC sensitivities (CSV)       | yes             | no              | yes                       |
| - OTC FpML                      | yes             | yes             | no                        |
| Historical calculation          | yes             | yes             | yes                       |
| Intraday calculation            | yes             | yes             | yes                       |
| Local installation possible     | no              | no              | no                        |
| Margin accuracy - ETD           | production-like | production-like | production-like           |
| Margin accuracy - OTC IRS       | high            | high            | production-like           |

### What is the difference between the CPME GUI and the API?

The GUI is a browser front-end to the API, but not every API feature
is provided by the GUI.

## Submitting a calculation request to API

### How can I perform a what-if analysis?

The user may load portfolios in the API in several formats concurrently. The user can for example

- Query the API with the member report CB202 to establish the baseline initial margin 
- Call the API with the member report CB202 and additional trades in a CSV file to get the what-if initial margin

Alternatively the user can prepare baseline and what-if portfolios in a single format and submit these individually.

### What to do when a request fails for a big portfolio?

Especially portfolios in XML formats can be quite large which may
cause connection problems. Try compressing the portfolio before submitting, see
"Compressing request and response" in the [API
definition][api-definition]

### Can I margin flexible instruments?

Eurex Clearing clears so-called flexible futures and options contracts
with non-standard expiry, strike or exercise style.

CPME can calculate margins on flexible contracts provided they already exist
on the Eurex market. Hypothetical flexible contracts (eg: of
client's own making) cannot be processed by CPME.

### Is it possible to calculate margin as-of an historical date?

Yes:

- in the API, see "Business date and time" section in [API definition][api-definition]
  - dates from 18 March 2019 available, or from 11 December 2018 for ETD-only requests
- on GUI, use "Historical calculation" checkbox
  - one year history available

Historical requests can take several minutes to perform. A request might be refused if the
CPME calculation cluster is busy as there is an upper limit on the
number of concurrent global historical calculations. In case your
request historical request is rejected try again in 15 minutes.

An upper limit has been imposed on the number of concurrent historical calculations
across all users, so a request might be refused if the CPME calculation cluster is busy.
In this case you are advised to try again in 15 minutes.

### What is the difference between API versions 1.0 and 2.0?

Version 2.0 has slightly more complex [estimator request](https://app.swaggerhub.com/apis-docs/dbgservice/cPME/2.0#/default/post_estimator)
allowing the user to submit multiple portfolio components of the same type,
e.g. two parts of OTC portfolio both in CSV format.

There are no plans to decommission 1.0, but some future functionality might
be implemented only in 2.0. You do not have to commit to one version - an application may use resources from
both 1.0 and 2.0.

### How to submit CSV or XML files?

The portfolio in CSV and XML formats is submitted as one string attribute
containing all the trades or positions. Please be careful about special
characters:

- line endings in CSV are written as `\n`
- strings inside XML are enclosed by single quotes `'`, because double quotes enclose the whole XML as one JSON attribute

As an example see how XML can be submitted using the `curl` command
(replace "your key" by your API key).
Note that the single quotes inside XML are escaped because we need
to enclose the JSON in single quotes on the command line. This is not
required inside application or script.

```
curl https://api.developer.deutsche-boerse.com/prod/prisma-margin-estimator/1.0.0/estimator \
 -H X-DBP-APIKEY:your-key -H "Content-Type: application/json" \
 -d '{"otc_cb202": {"account": "P", "xml": "<?xml version='"'"'1.0'"'"' encoding='"'"'UTF-8'"'"'?><Report xmlns:fpml='"'"'http://www.fpml.org/FpML-5/confirmation'"'"' xmlns='"'"'http://www.eurexchange.com/EurexIRSFullInventoryReport'"'"' name='"'"'CB202 Full Inventory Report'"'"'><rptHdr><exchNam>ECAG</exchNam><rptCod>RPTCB202</rptCod><rptNam>Full Inventory Report</rptNam><membLglNam>Some Member AG</membLglNam><membId>XYZFR</membId><rptPrntEffDat>2018-03-28T23:59:00</rptPrntEffDat><rptPrntRunDat>2018-03-27</rptPrntRunDat></rptHdr> <reportNameGrp> <CM> <rptSubHdr> <membLglNam>XYZFR &amp; Bank &quot; Inter &lt; n &gt; Germany &apos;</membLglNam> <membId>XYZFR</membId> <globalLEId>XYZFRXYZFRXYZFRXYZ85</globalLEId> </rptSubHdr> <acctTypGrp name='"'"'P'"'"'> <ProductType name='"'"'Swap'"'"'> <currTypCod value='"'"'CHF'"'"'> <rateIndex name='"'"'LIBOR'"'"'> <rateIndexTenor name='"'"'6M'"'"'> <idxSource>LIBOR02</idxSource> <CCPTradeId id='"'"'1234567'"'"'> <fpml:dataDocument fpmlVersion='"'"'5-0'"'"'> <fpml:trade> <fpml:tradeHeader> <fpml:partyTradeIdentifier> <fpml:partyReference href='"'"'CPTY_1234567'"'"'/> <fpml:tradeId tradeIdScheme='"'"''"'"'/> </fpml:partyTradeIdentifier> <fpml:partyTradeIdentifier> <fpml:partyReference href='"'"'PO_1234567'"'"'/> <fpml:accountReference href='"'"'ACC_1234567'"'"'/> <fpml:tradeId tradeIdScheme='"'"''"'"'>12345678-2</fpml:tradeId> <fpml:versionedTradeId> <fpml:tradeId tradeIdScheme='"'"''"'"'>1234567</fpml:tradeId> <fpml:version>2</fpml:version> </fpml:versionedTradeId> </fpml:partyTradeIdentifier> <fpml:tradeDate>2017-10-17</fpml:tradeDate> <fpml:clearedDate>2017-10-17</fpml:clearedDate> </fpml:tradeHeader> <fpml:fra> <fpml:buyerPartyReference href='"'"'PO_1234567'"'"'/> <fpml:sellerPartyReference href='"'"'CPTY_1234567'"'"'/> <fpml:adjustedEffectiveDate id='"'"'resetDate_1234567'"'"'>2018-10-19</fpml:adjustedEffectiveDate> <fpml:adjustedTerminationDate>2047-04-20</fpml:adjustedTerminationDate> <fpml:paymentDate> <fpml:unadjustedDate>2018-10-19</fpml:unadjustedDate> <fpml:dateAdjustments> <fpml:businessDayConvention>MODFOLLOWING</fpml:businessDayConvention> <fpml:businessCenters> <fpml:businessCenter>CHZU</fpml:businessCenter> </fpml:businessCenters> </fpml:dateAdjustments> </fpml:paymentDate> <fpml:fixingDateOffset> <fpml:periodMultiplier>-2</fpml:periodMultiplier> <fpml:period>D</fpml:period> <fpml:dayType>Business</fpml:dayType> <fpml:businessDayConvention>NONE</fpml:businessDayConvention> <fpml:businessCenters> <fpml:businessCenter>GBLO</fpml:businessCenter> </fpml:businessCenters> <fpml:dateRelativeTo href='"'"'resetDate_1234567'"'"'/> </fpml:fixingDateOffset> <fpml:dayCountFraction>ACT/360</fpml:dayCountFraction> <fpml:calculationPeriodNumberOfDays>32</fpml:calculationPeriodNumberOfDays> <fpml:notional> <fpml:currency>CHF</fpml:currency> <fpml:amount>12000000.00</fpml:amount> </fpml:notional> <fpml:fixedRate>0.03000000</fpml:fixedRate> <fpml:floatingRateIndex>CHF-LIBOR-BBA</fpml:floatingRateIndex> <fpml:indexTenor> <fpml:periodMultiplier>6</fpml:periodMultiplier> <fpml:period>M</fpml:period> </fpml:indexTenor> <fpml:fraDiscounting>ISDA</fpml:fraDiscounting> </fpml:fra> <fpml:documentation> <fpml:masterAgreement> <fpml:masterAgreementType masterAgreementTypeScheme='"'"''"'"'>ISDA</fpml:masterAgreementType> </fpml:masterAgreement> <fpml:contractualDefinitions>ISDA2006</fpml:contractualDefinitions> </fpml:documentation> </fpml:trade> <fpml:party id='"'"'CPTY_1234567'"'"'> <fpml:partyId>EUREX</fpml:partyId> <fpml:partyName>EUREX</fpml:partyName> </fpml:party> <fpml:party id='"'"'PO_1234567'"'"'> <fpml:partyId>XYZFR</fpml:partyId> <fpml:partyName>XYZFR &amp; Bank &quot; Inter &lt; n &gt; Germany &apos;</fpml:partyName> </fpml:party> <fpml:account id='"'"'ACC_1234567'"'"'> <fpml:accountId>XYZFR_P</fpml:accountId> <fpml:accountBeneficiary href='"'"'PO_1234567'"'"'/> </fpml:account> </fpml:dataDocument> <novDateTime>2017-10-17 16:44:55.646</novDateTime> <CCPTrdVersion>2</CCPTrdVersion> <CCPStatus>VERIFIED</CCPStatus> <preSrcSysTradeId>12345678</preSrcSysTradeId> <srcSysTradeId>12345678</srcSysTradeId> <srcSysGroupId>12345678</srcSysGroupId> <srcSysLEId>EEU_FUND1</srcSysLEId> <tradeRefID>12345678-2</tradeRefID> <oldtradeRefID>12345678-2</oldtradeRefID> <srcSysId>MarkitWire</srcSysId> <UTI>O00000000000001234567C</UTI> <UTIIssuer>E01XXXXECAG</UTIIssuer> <priorUTI>MARKITWIRE0000000000000012345678</priorUTI> <priorUTIIssuer>1234567890</priorUTIIssuer> <USI>O00000000000001234567C</USI> <USIIssuer>1050000007</USIIssuer> <priorUSI>MARKITWIRE0000000000000012345678</priorUSI> <priorUSIIssuer>1012345689</priorUSIIssuer> </CCPTradeId> </rateIndexTenor> </rateIndex> </currTypCod> </ProductType> </acctTypGrp> </CM> </reportNameGrp></Report>"}}'
```

You can also submit queries to the API with a programming language, e.g. Python. The
[API documentation][api-definition] contains an example in Python to get you started.

## Interpreting a margin result

### What is the precision of the margin calculation?

For exchange traded derivatives, the margin is calculated by code identical to the 
one used in the production environment at Eurex Clearing. The result on liquidation group
level should therefore be exactly the same as in the `CC050` report, if calculated for
the same date and time.

For OTC trades, the margin is calculated in an independent implementation of the 
margin methodology and may differ a few percent from official EurexOTC margin requirements.

### What are liquidation groups and liquidation group splits?

Products are placed in liquidation groups depending on their characteristics, for
instance in the listed equity liquidation group or the fixed income liquidation group. 
A list of liquidation group and the products that are assigned to them can be found 
at Eurex Clearing's [Risk Parameters page][risk-parameters].

A liquidation group can be further divided into liquidation group splits. This is currently only
the case for the fixed income liquidation group PFI01, which is divided into separate liquidation group
splits for OTC derivatives and listed fixed income/money market products, respectively.

For a given portfolio, initial margin is calculated independently at liquidation group level and is then
added to give total initial margin. Liquidation group splits are also treated independently.

### How does cross-margining work?

Listed fixed income/money market positions and OTC IRS derivatives belong to the
PFI01 liquidation group. 

Listed FI/MM products are placed in the liquidation group split PFI01_HP2, meaning they
are margined under the assumption of a two-day holding period. Similarly, OTC derivatives are
assumed a five-day holding period and are assigned to the liquidation group split PFI01_HP5.

Initial margin for PFI01 portfolios is calculated independently for the liquidation group splits and
are added to get total initial margin. When cross-margining is turned on, an algorithm checks will check 
if any of the listed FI/MM positions are economically sensible hedges to the OTC portfolio and will move
these to the five-day split if doing so lowers the total margin.

### How to validate CPME result against Eurex reports?

Compare the margin on liquidation group level against the `CC050`
report. The margin on account level (`CC060`) cannot be obtained from
CPME as the account may contain cash market instruments that are
currently supported by CPME.

### Is the margin from the simulation environment similar to production?

No.

The simulation environment (a.k.a. [sandbox on the Digital Business
Platform][api-digital-business-platform]) has different scenarios
and prices compared to production, and therefore produces a
different margin for the same portfolio.

Occasionally, the sandbox can be setup with production market data
but with different risk model parametrization, as a testing ground
before the new setup becomes productive. This will be announced by
the usual channels.

## Security

### Where is CPME running?

CPME is deployed in Deutsche Boerse VPC (Virtual Private Cloud) within
the Frankfurt region of Amazon Web Services.

### How is the communication designed, is it encrypted?

In essence CPME has a client-server architecture.

Client is either your browser or whatever you are making direct API
calls from.  Server is the backend accepting API calls.  All
communication between the backend and clients are running over HTTPS.

### Are the requests or results archived?

On the backend side all calculations are done in memory only. No
records are kept of the information processed.

### How do you ensure availability and disaster recovery?

CPME is stateless, has a highly elastic architecture and fault
tolerant setup.

It runs in a highly-available Kubernetes cluster spread that is spread
across three AWS Availability Zones in Frankfurt region.

### Which countries does client data pass?

Since CPME runs entirely within the Frankfurt region of AWS,
all processing takes part within Germany.

[CPME-gui]:https://eurexmargins.prod.dbgservice.com
[api-definition]:https://app.swaggerhub.com/apis-docs/dbgservice/cPME/2.0
[api-digital-business-platform]:https://console.developer.deutsche-boerse.com/
[prisma-methodology]:https://www.eurexclearing.com/resource/blob/32818/7bcf119060b658ad4e487f588744140d/data/brochure_eurex_clearing_prisma.pdf
[risk-parameters]:https://www.eurexclearing.com/clearing-en/risk-management/risk-parameters
