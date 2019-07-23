# GUI User Guide

[cPME GUI](https://eurexmargins.prod.dbgservice.com/estimator) offers margin calculation for:

- Eurex derivatives (ETD)
    - [uploaded in a simplified CSV format](#upload-etd-portfolio)
    - or entered directly directly on GUI
- OTC trades accepted by Eurex OTC, except FX swaps and inflation swaps
    - uploaded in CSV format known from Margin Calculator

It is assumed that the uploaded portfolio belongs to one account and the positions can offset each other.

The following sections describe separate entry of ETD and OTC portfolio, but it is possible to enter both. In that case you can select whether cross-margining between ETD and OTC should be applied using "Cross margin" checkbox.

## Upload ETD Portfolio

### Launch cPME GUI

1. Navigate to [https://eurexmargins.prod.dbgservice.com](https://eurexmargins.prod.dbgservice.com).
1. If you entered the first time, Terms of Use are shown, read them and accept them.

### Prepare ETD Portfolio

1. Download an example clicking "Eurex Portfolio Example" - "Download as a CSV file".
1. Edit the CSV file to replace the example with the positions you wish.

Columns in the CSV have the following meaning:

column | mandatory for Options / Futures? | example
--- | --- | ---: 
Product ID | | ODAX
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

1. Top box displays "Initial Margin" and "Premium Margin" for each liquidation group

## ETD GUI Entry

Positions can also be entered manually on GUI:

column | description
--- | ---
Product ID | dropdown with eligible products
Maturity | dropdown with contract year/month of standard series, e.g. "201712"
P/C | Call/Put flag, for options dropdown with "C" or "P", empty and disabled for futures
Strk | Strike, for options dropdown filled with exercise price of standard series of selected maturity, empty and disabled for flex
Version | dropdown with distinct version numbers for given maturity and strike, non-editable if only one version exists
Net Position | free text field to enter the position size, negative for short position

## OTC CSV Format

One line contains all information for one trade, including both its legs.
All columns must be present, although some can be empty.
Mandatory columns are marked by asterisk *.
For certain trade types, even some optional columns must be filled, see the description.
If unsure about possible combinations of attribute values please check
  [EurexOTC Clear IRS Product List](https://www.eurexclearing.com/resource/blob/227404/ff4638f2a3bfedbf511868ef54c6a153/data/ec15075e_Attach.pdf).

### Basic OTC trade attributes

- internalTradeID*: id of the trade to distinguish it in drilldown, must be unique
- tradeType*: IRS (or Swap), OIS, FRA, ZC
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

## Results

The calculated margin is displayed by default on liquidation group level.

The drilldown icon next to each liquidation group shows further details - different margin components on liquidation group split level.

In the ETD position table, each position has:

- Initial margin, this is approximate contribution of the position to Initial margin based on so-called component VaR; note that this is only an indication, given the nature of portfolio margining there is no such thing as exact contribution of single position to the margin
- Premium margin
- drilldown icon which shows distribution of the margins to liquidation group splits - this is relevant on for Fixed Income/Money Market products in case of cross-margining with OTC, other liquidation groups have only one split

