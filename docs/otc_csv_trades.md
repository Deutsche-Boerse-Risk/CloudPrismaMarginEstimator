# OTC Trades in CSV Format

One line contains all information for one trade, including both its legs.
All columns must be present, although some can be empty.
Mandatory columns are marked by asterisk *.
For certain trade types, even some optional columns must be filled, see the description.
If unsure about possible combinations of attribute values please check
  [EurexOTC Clear IRS Product List](https://www.eurexclearing.com/resource/blob/227404/ff4638f2a3bfedbf511868ef54c6a153/data/ec15075e_Attach.pdf).

## Basic OTC trade attributes

- internalTradeID*: id of the trade to distinguish it in drilldown, must be unique
- tradeType*: IRS (or Swap), OIS, FRA, ZC
- currency*: ISO code of currency, e.g. EUR, CHF, USD, GBP
- effectiveDate*: effective date as DD/MM/YYYY, e.g. 20/12/2018
- terminationDate*: termination date as DD/MM/YYYY, e.g. 20/12/2028

## Pay leg attributes

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

## Receive leg attributes

The receive leg has the same attributes as pay leg above, except prefix "pay" is replaced by "rcv".

## Example

```csv
internalTradeID,tradeType,currency,effectiveDate,terminationDate,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod\n1,FRA,EUR,20/12/2018,20/08/2019,fixedLeg,0.15,,,100000000,3M,,,,,,,,ACT/360,,,,,floatingLeg,,,,100000000,3M,,,,,,,,ACT/360,,,,
```

