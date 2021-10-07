# GUI User Guide

[CPME GUI](https://eurexmargins.prod.dbgservice.com/estimator) offers margin calculation for:

- Eurex listed derivatives (ETD)
    - [uploaded in a simplified CSV format](#upload-etd-portfolio)
    - or [entered directly in the GUI](#enter-etd-portfolio)
    - or upload Eurex Clearing ETD position report CP005
    - or upload portfolio export from C7 GUI
- OTC IRS trades accepted by Eurex OTC except FX swaps uploaded
    - [in CSV format known from Margin Calculator](#upload-otc-portfolio)
    - in the format of Eurex Clearing member full inventory reports (CB202/CB207)

It is assumed that the uploaded portfolio belongs to one account and the positions can offset each other.
If an OTC member report contains more members and accounts, the GUI picks the P account of the clearing member.

The following sections describe ETD and OTC portfolios separately,
but it is possible to margin a combined portfolio at the same time.
In that case you can select whether cross-margining between ETD and OTC
should be applied using the "Cross margin" checkbox.

## Upload ETD Portfolio

### Launch CPME GUI

1. Navigate to [https://eurexmargins.prod.dbgservice.com].
1. If you have not visited the site before, Terms of Use are shown. These must be accepted before the tool can be used.

### Prepare ETD Portfolio

1. Download an example from the CPME main page by first clicking "Eurex portfolio example" followed by "Download as a CSV file".
1. Edit the CSV file to replace the example with the positions you wish.

The columns in the CSV file are as follows:

column | mandatory for Options / Futures? | example
--- | --- | ---: 
Product ID | mandatory | ODAX
Maturity | mandatory | 201912
Call Put Flag | O: mandatory, F: ignored | C
Exercise Price | O: mandatory, F: ignored | 11000
Version Number | optional, defaults to 0 | 0
Net LS Balance | mandatory | -100

Example CSV file with one future and one option:

```csv
Product ID,Maturity,Call Put Flag,Exercise Price,Version Number,Net LS Balance
H3OL,202012,,,0,100
NVU,202006,P,36.000000,0,-200
```

### Upload the Prepared ETD File

1. Click "Upload Eurex Portfolio".
1. Select your prepared portfolio.

### Read the Results

Top box displays:

- "Total Margin", a sum of initial margin and premium margin for all [liquidation groups]
- "Initial Margin" and "Premium Margin", both total figures and figures for each liquidation group
- Drilldown icon (split arrow) next to liquidation group row opens further breakdown of initial margin into
  - liquidation groups splits (only for PFI01, i.e. Fixed Income and IRS)
  - margin components (market risk and the add-ons)

Position table shows:

- "Initial margin", an approximation of contribution of given position by "component VaR" method
  - note that this is only an indication, given the nature of portfolio margining there is no such thing as the exact contribution of a single position to the margin
- "Premium margin" for options (except future-style options)
- Drilldown icon to display distribution between liquidation group splits (interesting only for Fixed Income derivatives)

## Enter ETD Portfolio

Positions can also be entered manually in the GUI:

1. [launch CPME GUI](#launch-cpme-gui)
2. Click "Start an empty portfolio"
3. Enter the positions you wish:

column | description
--- | ---
Product ID   | dropdown with eligible products
Maturity     | dropdown with contract year/month of standard series, e.g. "201712"
C/P          | Call/Put flag, for options dropdown with "C" or "P", empty and disabled for futures
Strike       | Strike, for options dropdown filled with exercise price of standard series of selected maturity, empty and disabled for flex
Version      | dropdown with distinct version numbers for given maturity and strike, non-editable if only one version exists
Net Position | free text field to enter the position size, negative for short position

4. Click "+" or press Enter after each position
5. Click "Recalculate margin"
6. [Read the results](#read-the-results)

## Upload OTC Portfolio

Upload of OTC portfolio is similar to ETD portfolio upload:

1. [launch CPME GUI](#launch-cpme-gui)
2. Prepare your [OTC trades in CSV format](#otc-portfolio-csv-format)
  - you can use [Excel template] to generate the CSV:
    - save the template and open it in Excel
    - use "Insert trade" to enter the trades using the Excel form, see [OTC template description]
    - use "Export portfolio" which saves the portfolio in CSV format in the same folder as the template
3. Click "Upload OTC portfolio" and select the prepared CSV file
4. [Read the results](#read-the-results), only the top box will be shown, not individual trades

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

## Historical calculation

By default the margin is calculated as of the latest snapshot, i.e. using the most recent market data.
To calculate margin as of a historical snapshot, e.g. to compare against end-of-day reports,
select the historical calculation in GUI:

1. check "Historical calculation"
2. use "Select an available date" to pick the desired date
3. in case an intraday margin (and not end-of-day margin) is required, check "Live"
4. if "Live" is checked, use "Select timestamp" to pick the desired time


[https://eurexmargins.prod.dbgservice.com]:https://eurexmargins.prod.dbgservice.com
[liquidation groups]:https://deutsche-boerse-risk.github.io/CloudPrismaMarginEstimator/#what-liquidation-groups-are-there-and-what-is-liquidation-group-split
[Excel template]:https://github.com/Deutsche-Boerse-Risk/CloudPrismaMarginEstimator/blob/master/templates/otc/OTC_trade_template.xlsm?raw=true
[OTC template description]:https://github.com/Deutsche-Boerse-Risk/CloudPrismaMarginEstimator/blob/master/templates/otc/OTC_template_description.xls?raw=true
[EurexOTC Clear IRS Product List]:https://www.eurexclearing.com/resource/blob/227404/ff4638f2a3bfedbf511868ef54c6a153/data/ec15075e_Attach.pdf
