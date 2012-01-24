{% load pyformat %}Title: Investment Portfolio Report
Date: <report_date>
css: /Users/evandavey/Dropbox/Cochrane Davey/Business Enterprise/Marketing/Brand/Stylesheets/documentation-policy.css

#Investment Report ({{start_dt|date:"d/m/Y"}} to {{end_dt|date:"d/m/Y"}})

##Summary

* ROE [^ROE] for the period was {% pyformat data.roe '{0:.2f}' %}% p.q or  {% pyformat data.roe_pa '{0:.2f}' %}% p.a [^ROE-PA]

* YTD ROE was {% pyformat data.roe_ytd '{0:.2f}' %}%

* Equity ended at AUD {% pyformat data.equity_end '{:20,.2f}' %} from AUD {% pyformat data.equity_start '{:20,.2f}' %} at the start of the period and AUD {% pyformat data.equity_yearstart '{:20,.2f}' %} at the start of the year

* Portfolio net income was AUD {% pyformat data.income_net '{:20,.2f}' %} making YTD net income AUD {% pyformat data.income_net_ytd '{:20,.2f}' %}[^Unrealised-Equity]

* Tax payable was estimated as AUD {% pyformat data.liabilities_end '{:20,.2f}' %}

* Net contributions were AUD {% pyformat data.contributions '{:20,.2f}' %} during the period and AUD {% pyformat data.contributions_ytd '{:20,.2f}' %} YTD


##Detail

* Income was AUD {% pyformat data.income '{:20,.2f}' %}, expenses were AUD {% pyformat data.expenses '{:20,.2f}' %}

* YTD Income was AUD {% pyformat data.income_ytd '{:20,.2f}' %}, expenses {% pyformat data.expenses_ytd '{:20,.2f}' %}


###Interest Bearing Accounts

* Net income was AUD {% pyformat ib_data.net '{:20,.2f}' %} or {% pyformat ib_data.return '{0:.2f}' %}% p.q, {% pyformat ib_data.return_pa '{0:.2f}' %}% p.a [^Net-Interest-Income] 

* Gross income was AUD {% pyformat ib_data.income '{:20,.2f}' %}, expenses AUD {% pyformat ib_data.expenses '{:20,.2f}' %}

* The balance ended at AUD {% pyformat ib_data.end '{:20,.2f}' %} from AUD {% pyformat ib_data.start '{:20,.2f}' %}


###Stock Accounts

* Net income was AUD {% pyformat s_data.net '{:20,.2f}' %} or {% pyformat s_data.return '{0:.2f}' %}% p.q, {% pyformat s_data.return_pa '{0:.2f}' %}% p.a [^Equity-Net-Income] 

* Gross income was AUD {% pyformat s_data.income '{:20,.2f}' %}, expenses AUD {% pyformat s_data.expenses '{:20,.2f}' %}

* The balance ended at AUD {% pyformat s_data.end '{:20,.2f}' %} from AUD {% pyformat s_data.start '{:20,.2f}' %} ({% pyformat s_data.p_return '{0:.2f}' %}%) at the start of the period and AUD {% pyformat s_data.yearstart '{:20,.2f}' %} ({% pyformat s_data.p_return_ytd '{0:.2f}' %}%) at the start of the year.

* The total return YTD [^Equity-Total-Return] was {% pyformat s_data.total_return_ytd '{0:.2f}' %}% 

* The unrealised move was AUD {% pyformat s_data.change '{:20,.2f}' %} for the period to be AUD {% pyformat s_data.change_ytd '{:20,.2f}' %} YTD

###Pension Accounts

* Net income was AUD {% pyformat p_data.net '{:20,.2f}' %} or {% pyformat p_data.return '{0:.2f}' %}% p.q, {% pyformat p_data.return_pa '{0:.2f}' %}% p.a [^Pension-Net-Income] 

* Gross income was AUD {% pyformat p_data.income '{:20,.2f}' %}, expenses AUD {% pyformat p_data.expenses '{:20,.2f}' %}

* The balance ended at AUD {% pyformat p_data.end '{:20,.2f}' %} from AUD {% pyformat p_data.start '{:20,.2f}' %}



##Asset Allocation

|             |         {{start_dt|date:"d/m/Y"}} || {{end_dt|date:"d/m/Y"}}          ||
              | Value 		  | Weight       | Value         | Weight       |
 ------------ | :-----------: | -----------: | :-----------: | -----------: |
{%for aa in aa_data%}{{aa.label}}|{% pyformat aa.val1 '{:20,.2f}' %}|{% pyformat aa.weight1 '{:0.2f}' %}%|{% pyformat aa.val2 '{:20,.2f}' %}|{% pyformat aa.weight2 '{0:.2f}' %}%|
{%endfor%}




##Investment / Market Review

###Price Moves

|			  | Weight | Weighted Return | Period Return | Change   | Now    | Period Start  | Year Start  |
 ------------ | ----:  | -----------:    | -----------:  | ------:  | ------:|-------------: | ----------: |
{%for key,s in share_data.items %}{{key}} | {% pyformat s.Wp '{0:.2f}'%}% | {% pyformat s.Rp '{0:.2f}'%}% | {% pyformat s.p_return '{0:.2f}'%}% | ${% pyformat s.p_change '{0:.2f}'%} | ${% pyformat s.p_end '{0:.2f}'%}| ${% pyformat s.p_start '{0:.2f}'%} | ${% pyformat s.p_yearstart '{0:.2f}'%} |
{%endfor%}

###Interest Rates

|			  | Weight | Period Interest | Effective Rate |
 ------------ | -----: |-----------:    | ----------------------:   |
{%for i in i_data %}{{i.account}} | {% pyformat i.Ws '{0:.2f}'%}% | ${% pyformat i.interest '{0:.2f}'%} | {% pyformat i.rate '{0:.2f}'%}% | 
{%endfor%}

##Notes

[^ROE-after-inflation]: YOY ROE p.a - RBA's preferred inflation measure (average of weighted median and trimmed mean)

[^ROE]: Calculated as (Net Income - Net Contributions) / Starting Equity

[^ROE-PA]: Calculated as ROE p.q * 4
	
[^Net-Interest-Income]: Net Interest Income = Interest Income - Tax Estimate on Income.  Return = Net Interest Income / Starting Income Investments

[^Equity-Net-Income]: Net Equity Income = Dividends - Tax Estimate on Dividends.  Return = Net Equity Income / Starting Equity Investments.

[^Equity-Total-Return]: Total Return = (Unrealised Equity + Net Realised Equity + Net Income) / Starting Equity Investments

[^Pension-Net-Income]: Net Pension Income = Returns - Management Fees - Insurance Premiums - Tax on Contributions

[^AU-Cash]: See [RBA Official Cash Rate](http://www.rba.gov.au/statistics/cash-rate.html)

[^Inflation]: See [RBA inflation statistics](http://www.rba.gov.au/inflation/measures-cpi.html)

[^Unrealised-Equity]: This figure includes unrealised P&L of AUD {% pyformat s_data.change_ytd '{:20,.2f}' %}