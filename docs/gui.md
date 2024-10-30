# GUI User Guide

[CPME GUI](https://cpme.eurex.com) offers margin calculation for:

- Eurex listed derivatives (ETD)
    - [upload in a simplified CSV format](#prepare-etd-portfolio)
    - or [enter directly in the GUI](#enter-etd-portfolio)
    - or [upload](#upload-the-prepared-etd-file) Eurex Clearing ETD position report CP005
    - or [upload](#upload-the-prepared-etd-file) portfolio export from C7 GUI
- OTC IRS trades accepted by Eurex OTC except FX swaps uploaded
    - [in CSV format known from Margin Calculator](#upload-otc-portfolio)
    - in the format of Eurex Clearing member full inventory reports (CB202/CB207)
    - as [DV01 sensitivity table or as CC233 Sensitivity report](#upload-otc-sensitivities)
    - or [entered as OTC shorthand](#enter-otc-shorthand)
- Repo single-ISIN trades except floating rate and open-ended repos
    - [uploaded in F7 portfolio export CSV format](#upload-repo-portfolio)
    - or [entered directly in the GUI](#enter-repo-portfolio)

It is assumed that the uploaded portfolio belongs to one account and the positions can offset each other.
If an OTC member report contains more members and accounts, the GUI picks the P account of the clearing member.

The following sections describe ETD and OTC portfolios separately,
but it is possible to margin a combined portfolio at the same time.
In that case you can select whether cross-margining between ETD and OTC
should be applied using the "Cross margin" checkbox.

Repo portfolio can be submitted only separately, because the margin
is calculated by a different methodology: Risk Based Margining (RBM)
for Repo vs Portfolio Margining for ETD and OTC.

Besides the Production environment https://cpme.eurex.com,
also Member Simulation environment is available at https://cpme.risk.simu.gcp.dbgservice.com/
with results comparable to Prisma Member Simulation reports (note that the margin figures can be very different from Production).

# ETD

## Upload ETD Portfolio

### Launch CPME GUI

1. Navigate to [https://cpme.eurex.com].
1. If you have not visited the site before, Terms of Use are shown. These must be accepted before the tool can be used.

### Prepare ETD Portfolio

If you have CP005 position report or C7 portfolio export, you can directly [upload it](#upload-the-prepared-etd-file).
Otherwise, prepare ETD portfolio file in CSV format as follows:

1. Download an example from the CPME main page by first clicking "Eurex portfolio example" followed by "Download as a CSV file".
1. Edit the CSV file to replace the example with the positions you wish.

The columns in the CSV file are as follows:

column | mandatory for Options / Futures? | example
--- | --- | ---: 
Product ID | mandatory | OEXD
Contract Date | mandatory | 20311219
Call Put Flag | O: mandatory, F: ignored | C
Exercise Price | O: mandatory, F: ignored | 100.00
Version Number | optional, defaults to 0 | 0
Net LS Balance | mandatory | -100

Example CSV file with one future and one option:

```csv
Product ID,Contract Date,Call Put Flag,Exercise Price,Version Number,Net LS Balance
FEXD,20311219,,,0,100
OEXD,20311219,C,100.00,0,-100
```

All the additional columns can be left empty, they are used only for special cases:

- positions which expired today and were not closed before the expiry, then the net position size is entered under Net EA Balance
- positions on flexible contracts, then Instrument Type ("Flex Future" or "Flex Option") and Exercise Style Flag (for options, "EUROPEAN" or "AMERICAN") is filled

### Upload the Prepared ETD File

1. Click "Upload Eurex Portfolio".
1. Select your prepared portfolio.
    - for CP005 upload, CPME displays dialog to select an account from those available in your report

### Read the Results

Top box displays:

- "Total Margin", a sum of initial margin and premium margin for all [liquidation groups]
- "Initial Margin" and "Premium Margin", both total figures and figures for each liquidation group
- Drilldown icon (split arrow) next to liquidation group row opens further breakdown of initial margin into
  - liquidation groups splits (only for PFI01, i.e. Fixed Income and IRS)
  - margin components (market risk and the add-ons)

ETD Position table shows (if ETD portfolio was uploaded):

- "Initial margin", an approximation of contribution of given position by "component VaR" method
    - note that this is only an indication, given the nature of portfolio margining there is no such thing as the exact contribution of a single position to the margin
- "Premium margin" for options (except future-style options)
- Drilldown icon to display distribution between liquidation group splits (interesting only for Fixed Income derivatives)

OTC Trade table shows (if OTC portfolio was uploaded):

- "PV" as present value
- "DV01" as the DV01 sensitivity
- "CompVaR", an approximation of contribution of given trade to Initial Margin by "component VaR" method (only an indication, see disclaimer above)

## Enter ETD Portfolio

Positions can also be entered manually in the GUI:

1. [launch CPME GUI](#launch-cpme-gui)
2. Click "Start an empty portfolio"
3. Enter the positions you wish:

column             | description
---                | ---
Product ID         | dropdown with eligible products, e.g. "OEXD"
Contract Frequency | filters expiries that are displayed in Contract Date column, most products have only MONTHLY frequency
Contract Date      | dropdown with contract year/month of standard series
C/P                | Call/Put flag, for options dropdown with "C" or "P", empty and disabled for futures
Strike             | Strike, for options dropdown filled with exercise price of standard series of selected maturity, empty and disabled for flex
Version            | dropdown with distinct version numbers for given maturity and strike, non-editable if only one version exists
Net Position       | free text field to enter the position size, negative for short position

4. Click "+" or press Enter after each position
5. Click "Recalculate margin"
6. [Read the results](#read-the-results)

# OTC

## Upload OTC Portfolio

Upload of OTC portfolio is similar to ETD portfolio upload:

1. [launch CPME GUI](#launch-cpme-gui)
2. Get your "Eurex Clearing member full inventory reports (CB202/CB207)", or prepare your [OTC trades in CSV format](#otc-portfolio-csv-format)
    - you can use [Excel template] to generate the CSV:
        - save the template and open it in Excel
        - use "Insert trade" to enter the trades using the Excel form, see [OTC template description]
        - use "Export portfolio" which saves the portfolio in CSV format in the same folder as the template
3. Click "Upload OTC portfolio" and select the prepared CSV file
4. [Read the results](#read-the-results)

## Upload OTC Sensitivities

1. [launch CPME GUI](#launch-cpme-gui)
2. Prepare DV01 sensitivity table as CSV file using [OTC sensitivities template], or get your "CC233 Sensitivity Report for IRS"
    - for CC233 upload, CPME displays dialog to select an account from those available in your report
4. Click "Upload OTC Sensitivities" and select the prepared CSV or the report file
5. [Read the results](#read-the-results)

## OTC Portfolio CSV Format

One line contains all information for one trade, including both its legs.
All columns must be present, although some can be empty.
Mandatory columns are marked by asterisk \*.
For certain trade types, even some optional columns must be filled, see the description.
If you are unsure about possible combinations of attribute values please refer to the [EurexOTC Clear IRS Product List] or the [OTC template description] (also available as link in the CPME GUI).

### Basic OTC trade attributes

- internalTradeID*: id of the trade to distinguish it in drilldown, must be unique
- tradeType*: IRS, Basis swap, OIS, FRA, VNS, ZCIS
- currency*: ISO code of currency, e.g. EUR, CHF, USD, GBP
- effectiveDate*: effective date as DD/MM/YYYY, e.g. 20/12/2018
- terminationDate*: termination date as DD/MM/YYYY, e.g. 20/12/2028

### Pay leg attributes

- payLegType*: fixedLeg or floatingLeg
- payLegSpread: rate for fixedLeg in %, or spread (optional) for floatingLeg in bp
- payLegIndex: index for floatingLeg, if empty, default index for the currency is selected
- payInterestFixedAmount: allowed for fixedLeg only, lump sum paid at maturity of zero coupon swap
- payNotional*: notional
- payPaymentPeriod*: 1M, 3M, 6M, 12M, 1T (for zero-coupon)
- payPeriodStartVNS: fill only for VNS
- payCompounding: fill only for compounding swap, Flat or Straight
- payCompoundingIndexPeriod: period for compounding swap, 1M, 3M, 6M, 12M
- payStub: fill only if the leg has a stub, LongFinal, LongInitial, ShortInitial, ShortFinal
- payFirstRate: first pre-defined rate
- payFirstInterpolationTenor: stub interpolation tenor for floatingLeg, 1W, 1M, 3M, 6M
- paySecondInterpolationTenor: stub interpolation tenor for floatingLeg, 1W, 1M, 3M, 6M
- payDayCountMethod*: 30/360, 30E/360, 30E/360.ISDA, ACT/360, ACT/365.FIXED, ACT/ACT.ISDA, ACT/365.ISDA, ACT/ACT.ICMA, ACT/ACT.ISMA, 1/1
- payBusinessDayConvention: MODFOLLOWING, FOLLOWING, PRECEDING
- payPaymentCalendar: EUTA, CHZU, GBLO, USNY, DEFR, ITMI, FRPA, ESMA, BEBR, JPTO, DKCO, NOOS, SEST, PLWA
- payAdjustment: ADJUSTED, UNADJUSTED, MAT_UNADJUSTED
- payRollMethod: Standard, IMM

### Receive leg attributes

The receive leg has the same attributes as pay leg above, except prefix "pay" is replaced by "rcv".

### Example

```csv
internalTradeID,tradeType,currency,effectiveDate,terminationDate,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod
1,FRA,EUR,20/12/2018,20/08/2019,fixedLeg,0.15,,,100000000,3M,,,,,,,,ACT/360,,,,,floatingLeg,,,,100000000,3M,,,,,,,,ACT/360,,,,
```

## Enter OTC shorthand

Instead of uploading the OTC trades or sensitivities, it is possible to enter interest rate swaps
in a simplified way called "OTC shorthand". Only the key attributes are required:
currency, notional, maturity and pay/rec, optionally fixed rate - e.g. `EUR 100m 25y pay 1%`.
If the rate is left out, the swap with NPV=0 will be created.
CPME uses default values for the remaining attributes, it is not possible to enter them.

To specify trade by OTC shorthand:

1. [launch CPME GUI](#launch-cpme-gui)
2. Click "Start an empty portfolio"
3. Switch to "OTC portfolio" tab
4. Click "Enter OTC trades"
5. Write one trade per line into the trade window, using "currency notional maturity pay/rec rate(optional)" format, e.g.:

```
USD 1b 3y rec 1.5%
EUR 500m 10y pay 1%
CHF 100m 20y pay
```

6. Click "Submit" (this will replace your previous OTC portfolio, there is currently no option to add trades to the existing portfolio)
7. [Read the results](#read-the-results)


# Repo

## Upload Repo portfolio

Upload of Repo portfolio is similar to ETD portfolio upload:

1. [launch CPME GUI](#launch-cpme-gui)
2. Prepare your [Repo trades in CSV format](#repo-portfolio-csv-format)
  - either by exporting the portfolio from F7
  - or download an example from the CPME main page by first clicking "Repo portfolio example" followed by "Download as a CSV file" and replace example trades by your trades
3. Click "Upload REPO portfolio" and select the prepared CSV file
4. [Read RBM results](#read-rbm-results) or download them using "Download" / "Repo margin" / "As XLSX file" buttons.


### Repo portfolio CSV format

CSV column                                         | Data type | Mandatory | Example | Comments
---                                                | ---    | ---  | ---          | ---
_ISIN_                                             | string | yes  | EU000A1A1DJ5 |
_Trade date_                                       | string | yes  | 2021-03-15   | YYYY-MM-DD or YYYYMMDD
_Settlement Date FrontLeg_<br> or _Front Leg Date_ | string | yes  | 2021-03-16   | YYYY-MM-DD or YYYYMMDD
_Settlement Date TermLeg_<br> or _Term Leg Date_   | string | yes* | 2021-04-13   | YYYY-MM-DD or YYYYMMDD
_Buy Sell Indicator_<br> or _Buy/Sell Indicator_   | string | yes  | BUY          | SELL: Sell securities, Cash taker;<br/> BUY: Buy securities, Cash Provider
_Currency_                                         | string | no   | EUR          |
_Nominal_                                          | double | yes* | 500000000.00 |
_Fixed Repo Rate_<br> or _Repo Rate_               | double | yes* | -1.200       | in percent
_Trade ID_                                         | string | no   | 2323435      |
_Clean Price increase / decrease_                  | double | no   | -1.00        | e.g. price 101.71 shifted by -1.00 is 100.71

\* _Settlement Date TermLeg_, _Nominal_ and _Fixed Repo Rate_ are necessary in order to process the repo in CPME. However the F7 portfolio can contain "open repos" without term leg settlement date (the date is empty), "GC basket trades" (nominal is empty) and "floating repos" without fixed rate (the rate is not a number). CPME skips such repos with a warning, processing the rest.


### Read RBM 

Additional Margin and Current Liquidating Margin (account level) is summed from Margin Class level per currency and displayed in a box "Cash Market RBM Margin".
See example for a portfolio that contains EUR and CHF margin class currencies:

```
Cash Market RBM Margin
                    AM    AM before grouping             CLM    Total Margin
EUR          10,000.00             12,000.00        1,000.00        11,000.0
CHF          20,000.00             20,000.00        3,000.00        23,000.0
```

Value "AM before grouping" is for your information only, to see the effect of margin offsets in case several trades fall into the same margin group.

Results on Margin Class and trade (or even trade leg) level can be found by clicking "Show details" icon at the end of the Repo trade row, e.g.:

```
Margin Class                         S0055 (Margin Group ABCD)
Additional Margin                     12,345,678.00 CHF
Additional Margin before grouping     12,789,678.50 CHF
Current Liquidating Margin             1,123,456.35 CHF
Margin Parameter                               3.56 %

--------------------------------------------------------------

ISIN                                 CH0224397171

Settlement Date                      2021-03-16 (Front Leg)
Net Cash Position                    513,566,585.00 CHF
Net Security Position               -513,525,147.00 CHF
Current Liquidating Margin                41,439.00 CHF

Settlement Date                      2021-04-13 (Term Leg)
Net Cash Position                   -513,342,253.00 CHF
Net Security Position                513,535,108.00 CHF
Current Liquidating Margin               237,385.00 CHF
```

## Enter Repo portfolio

Repo trades can be also entered directly in the GUI:

1. [launch CPME GUI](#launch-cpme-gui)
2. Click "Start an empty portfolio"
3. Switch to "Repo portfolio" tab
4. Enter the positions you wish, using the same attributes as described in [Repo portfolio CSV format](#repo-portfolio-csv-format)
5. [Read RBM results](#read-rbm-results) or download them using "Download" / "Repo margin" / "As XLSX file" buttons.


## Historical calculation

By default, the margin is calculated as of the latest snapshot, i.e. using the most recent market data.
To calculate margin as of a historical snapshot, e.g. to compare against end-of-day reports,
select the historical calculation in GUI:

1. check "Historical calculation"
2. use "Select an available date" to pick the desired date
3. in case an intraday margin (and not end-of-day margin) is required, check "Live"
4. if "Live" is checked, use "Select timestamp" to pick the desired time


[https://cpme.eurex.com]:https://cpme.eurex.com
[liquidation groups]:https://deutsche-boerse-risk.github.io/CloudPrismaMarginEstimator/#what-liquidation-groups-are-there-and-what-is-liquidation-group-split
[Excel template]:https://github.com/Deutsche-Boerse-Risk/CloudPrismaMarginEstimator/blob/master/templates/otc/OTC_trade_template.xlsm?raw=true
[OTC template description]:https://github.com/Deutsche-Boerse-Risk/CloudPrismaMarginEstimator/blob/master/templates/otc/OTC_template_description.xlsm?raw=true
[EurexOTC Clear IRS Product List]:https://www.eurexclearing.com/resource/blob/227404/ff4638f2a3bfedbf511868ef54c6a153/data/ec15075e_Attach.pdf
[OTC sensitivities template]:https://github.com/Deutsche-Boerse-Risk/CloudPrismaMarginEstimator/raw/master/templates/otc/OTC_sensitivities_template.m
