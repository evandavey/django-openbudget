"""
Finance functions contributed by Skipper Seabold.

Somre are extensions and finishing of numpy.lib.financial

Todo: pull out Newton-Raphson method into it's own function for reuse
"""

import numpy as np
from numpy.testing import *

def _discf(rate, pmts, dates):
    '''
    Convenience function for calculating discrete time dpv and its derivative.
    '''
    from datetime import date
    dcf=[]
    dcfprime=[]
    if isinstance(dates[0],date):
        for i,cf in enumerate(pmts):
            d=dates[i]-dates[0]
            dcf.append(cf*(1+rate)**(-d.days/365.))
            dcfprime.append((-d.days/365.)*cf*(1+rate)**(-d.days/365. - 1))
        return np.add.reduce(dcf),np.add.reduce(dcfprime)
    for i,cf in enumerate(pmts):
        if i==0:
            dcf.append(cf)
        else:
            dcf.append(cf*(1+rate)**(-dates[i-1]/365.))
            dcfprime.append((-dates[i-1]/365.)*cf*(1+rate)**\
            (-dates[i-1]/365.-1))
    return np.add.reduce(dcf),np.add.reduce(dcfprime)

def xirr(pmts, dates, guess=.10, maxiter=100, tol=1.48e-8):
    '''
    IRR function that accepts irregularly spaced cash flows

    Parameters
    ----------
    values: array_like
          Contains the cash flows including the initial investment
    dates: array_like
          Contains the dates of payments as in the form (year, month, day)

    Returns: Float
          Internal Rate of Return

    Examples
    --------------
    dates=[[2008,2,5],[2008,7,5],[2009,1,5]]
    for i, dt in enumerate(dates):
        dates[i]=date(*dt) 
    pmts=[-2750,1000,2000]
    print xirr(pmts,dates)
 
    or

    dates==[151,335]
    pmt=[-2750,100,2000]
    print xirr(pmts,dates)

    Notes
    -----
    In general the xirr is the solution to

    .. math:: \sum_{t=0}^M{\frac{v_t}{(1+xirr)^{(date_t-date_0)/365}}} = 0

    To Do
    -----
    Get rid of reliance on date type or days difference.
    Write a *simple* date parser?
    Add tests. What behavior for only one cashflow?

    '''
#   how to do it with scipy, _discf doesn't need derivative   
#    f = lambda x: _discf(x, pmts, dates)
#    try: 
#        from scipy.optimize import newton
#        print "scipy did it"
#        return newton(f, guess)
#    except:
#        pass

#   Newton-Raphson iterations

    x0 = guess
    for iter in range(maxiter):
        func,funcp = _discf(x0,pmts,dates)
        if funcp == 0:
            print "Warning: Stopped on zero-derivative.\n"
            print "Solution set to current guess %s." % (x0)
            return x0
        x = x0 - func/funcp
        if abs(x-x0) < tol:
            return x
        x0 = x
    raise RuntimeError, "Failed to converge after %d iterations, returnging %s." % (maxiter, x)


#if __name__=="__main__":



##############################################

from numpy.lib.financial import _when_to_num,_convert_when,pmt

#_when_to_num = {'end':0, 'begin':1,
#                'e':0, 'b':1,
#                0:0, 1:1,
#                'beginning':1,
#                'start':1,
#                'finish':0}

#def _convert_when(when):
#    try:
#        return _when_to_num[when]
#    except KeyError:
#        return [_when_to_num[x] for x in when]

#def pmt(rate, nper, pv, fv=0, when='end'):
#    """
#    Compute the payment against loan principal plus interest.
#
#    Parameters
#    ----------
#    rate : array_like
#        Rate of interest (per period)
#    nper : array_like
#        Number of compounding periods
#    pv : array_like
#        Present value
#    fv : array_like
#        Future value
#    when : {{'begin', 1}, {'end', 0}}, {string, int}
#        When payments are due ('begin' (1) or 'end' (0))
#
#    Returns
#    -------
#    out : ndarray
#        Payment against loan plus interest.  If all input is scalar, returns a
#        scalar float.  If any input is array_like, returns payment for each
#        input element. If multiple inputs are array_like, they all must have
#        the same shape.

#    Notes
#    -----
#    The payment ``pmt`` is computed by solving the equation::

#     fv +
#     pv*(1 + rate)**nper +
#     pmt*(1 + rate*when)/rate*((1 + rate)**nper - 1) == 0
#
#    or, when ``rate == 0``::
#
#      fv + pv + pmt * nper == 0
#
#    Examples
#    --------
#    What would the monthly payment need to be to pay off a $200,000 loan in 15
#    years at an annual interest rate of 7.5%?
#
#    >>> np.pmt(0.075/12, 12*15, 200000)
#    -1854.0247200054619
#
#    In order to pay-off (i.e. have a future-value of 0) the $200,000 obtained
#    today, a monthly payment of $1,854.02 would be required.
#
#    """
#    when = _convert_when(when)
#    rate, nper, pv, fv, when = map(np.asarray, [rate, nper, pv, fv, when])
#    temp = (1+rate)**nper
#    miter = np.broadcast(rate, nper, pv, fv, when)
#    zer = np.zeros(miter.shape)
#    fact = np.where(rate==zer, nper+zer, (1+rate*when)*(temp-1)/rate+zer)
#    return -(fv + pv*temp) / fact


def ipmt(rate, per, nper, pv, fv=0.0, when='end'):
    """
    Not implemented. Compute the payment portion for loan interest.

    Parameters
    ----------
    rate : scalar or array_like of shape(M, )
        Rate of interest as decimal (not per cent) per period
    per : scalar or array_like of shape(M, )
        Interest paid against the loan changes during the life or the loan.
        The `per` is the payment period to calculate the interest amount.
    nper : scalar or array_like of shape(M, )
        Number of compounding periods
    pv : scalar or array_like of shape(M, )
        Present value
    fv : scalar or array_like of shape(M, ), optional
        Future value
    when : {{'begin', 1}, {'end', 0}}, {string, int}, optional
        When payments are due ('begin' (1) or 'end' (0)).
        Defaults to {'end', 0}.

    Returns
    -------
    out : ndarray
        Interest portion of payment.  If all input is scalar, returns a scalar
        float.  If any input is array_like, returns interest payment for each
        input element. If multiple inputs are array_like, they all must have
        the same shape.

    See Also
    --------
    ppmt, pmt, pv

    Notes
    -----
    The total payment is made up of payment against principal plus interest.

    ``pmt = ppmt + ipmt``

    Gnumeric and KSpread disagree vs. Excel and OO for ipmt(.05/12,100,360,100000,0,1)
    Need to derive the results and state assumptions.

    """
    m = pmt(rate, nper, pv, fv, when)
    when = _convert_when(when)
    return -(rate*(pv+when*m)*(1+rate)**(per-1-when) + m*((1+rate)**(per-1-when)-1))

def ppmt(rate, per, nper, pv, fv=0.0, when='end'):
    """
    Not implemented. Compute the payment against loan principal.

    Parameters
    ----------
    rate : array_like
        Rate of interest (per period)
    per : array_like, int
        Amount paid against the loan changes.  The `per` is the period of
        interest.
    nper : array_like
        Number of compounding periods
    pv : array_like
        Present value
    fv : array_like, optional
        Future value
    when : {{'begin', 1}, {'end', 0}}, {string, int}
        When payments are due ('begin' (1) or 'end' (0))

    See Also
    --------
    pmt, pv, ipmt

    """
    m = pmt(rate, nper, pv, fv, when)
    if per == 1:
        return m
    else:
        return m - ipmt(rate, per, nper, pv, fv, when)

### Patch for MIRR ###
# Notes: test just happens to be right for the first value given
# The second compare to value is wrong
# Does not work compare mirr((-5000,1000,2000,3000), .05, .08) to OO calc answer
# Also tested with OpenFormula tests etc.
# This patch works as expected
def mirr(values, finance_rate, reinvest_rate):
    """
    Modified internal rate of return.

    Parameters
    ----------
    values : array_like
        Cash flows (must contain at least one positive and one negative value)
        or nan is returned.
    finance_rate : scalar
        Interest rate paid on the cash flows
    reinvest_rate : scalar
        Interest rate received on the cash flows upon reinvestment

    Returns
    -------
    out : float
        Modified internal rate of return

    """

    values = np.asarray(values)
    initial = values[0]
    values = values[1:]
    n = values.size
    pos = values * (values>0)
    neg = values * (values<0) 
    if not (pos.size > 0 and neg.size > 0):
        return np.nan

    numer = np.abs(np.npv(reinvest_rate, pos))
    denom = np.abs(np.npv(finance_rate, neg))
    if initial>0:
        return ((initial + numer) / denom)**(1.0/n)*(1+reinvest_rate) - 1
    else:
        return ((numer / (-initial + denom)))**(1.0/n)*(1+reinvest_rate) - 1
    
#if __name__=="__main__":
#    print "xirr functions"    
#    dates=[[2008,2,5],[2008,7,5],[2009,1,5]]
#    from datetime import date
#    for i,dt in enumerate(dates):
#         dates[i]=date(*dt)
#    pmts=[-2750,1000,2000]
#    print xirr(pmts,dates)
#    print
#    dates2=[151,335]
#    print xirr(pmts,dates2) 
