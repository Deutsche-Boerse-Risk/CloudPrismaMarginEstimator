"""
The following example generates a portfolio in CSV format. The portfolio
consists of a 10Y EUR interest rate swap starting two days from today
and a short position in Euro-Bund futures. Initial margin is calculated
with (xm = True) and without (xm = False) cross margining and results are 
printed. 

Remember to replace x's in api_header with your own API-key

To register for an API-key please visit

https://console.developer.deutsche-boerse.com/apis
"""

import requests 
import json 
import datetime

url_base = ("https://api.developer.deutsche-boerse.com/prod/prisma-margin-estimator/1.0.0/")
api_header = {"X-DBP-APIKEY": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}

effective_date = datetime.date.today() + datetime.timedelta(days=2)
maturity_date = effective_date.replace(year=effective_date.year+10)

otc_header = ('internalTradeID,tradeType,currency,effectiveDate,terminationDate,'
              'payLegType,payLegSpread,payLegIndex,payInterestFixedAmount,'
              'payNotional,payPaymentPeriod,payPeriodStartVNS,payCompounding,'
              'payCompoundingIndexPeriod,payStub,payFirstRate,'
              'payFirstInterpolationTenor,paySecondInterpolationTenor,'
              'payDayCountMethod,payBusinessDayConvention,payPaymentCalendar,'
              'payAdjustment,payRollMethod,rcvLegType,rcvLegSpread,rcvLegIndex,'
              'rcvInterestFixedAmount,rcvNotional,rcvPaymentPeriod,'
              'rcvPeriodStartVNS,rcvCompounding,rcvCompoundingIndexPeriod,rcvStub,'
              'rcvFirstRate,rcvFirstInterpolationTenor,rcvSecondInterpolationTenor,'
              'rcvDayCountMethod,rcvBusinessDayConvention,rcvPaymentCalendar,'
              'rcvAdjustment,rcvRollMethod\n')
          
otc_trade = ('OTC1,IRS,EUR,{},{},floatingLeg,,EURIBOR,,100000000,6M,,,,,,,,'
         'ACT/360,MODFOLLOWING,EUTA,UNADJUSTED,Standard,fixedLeg,0.833,,,'
         '100000000,12M,,,,,,,,30/360,MODFOLLOWING,EUTA,UNADJUSTED,'
         'Standard').format(effective_date.strftime("%d/%m/%Y"),
                           maturity_date.strftime("%d/%m/%Y"))

otc_csv = otc_header + otc_trade

series = requests.get(url_base + "series",
                 params = {'products': 'FGBL'},
                 headers = api_header).json()

maturity = series['list_series'][-1]['expiry_maturity']
version_number = series['list_series'][-1]['version_number']

etd_header = ('Product ID,Maturity,Call Put Flag,Exercise Price,'
              'Version Number,Net LS Balance\n')
etd_position = ('FGBL,{},,,{},-500'.format(maturity, version_number))

etd_csv = etd_header + etd_position

results = {}
for xm in [True, False]:
    results[xm] = requests.post(url_base + 'estimator', 
                                headers = api_header,
                                   json = {'etd_csv': {'csv': etd_csv},
                                           'otc_csv': {'csv': otc_csv},
                                           'clearing_currency': 'EUR',
                                           'is_cross_margined': xm}).json()
print('Example of margin output:')
print(json.dumps(results[False]['portfolio_margin'], indent=4, sort_keys=True))

for xm in [False, True]:
    print('XM: {}'.format(['Off', 'On'][xm]))
    margin = 0
    for lgs in results[xm]['portfolio_margin']:
        print('IM {}: {:>11,.0f}'.format(lgs['liquidation_group_split'], 
                                         lgs['initial_margin']))
        margin += lgs['initial_margin']
    print('IM Total:     {:>11,.0f}'.format(margin))

benefit = [-lgs['initial_margin']*(-1)**xm for xm in [True, False] 
               for lgs in results[xm]['portfolio_margin']]
print('XM benefit:   {:>11,.0f}'.format(sum(benefit)))