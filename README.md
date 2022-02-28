# payment_engine
Author: Ryan Sedlacek
Purpose: Dummy payment engine! Super exciting!

SOME NOTES:

0 is not a valid client id in this implementation!
negative numbers are not valid transaction ids in this implementation!
It seems disputes are mainly for deposits... But the logic could be applied to withdrawals abiet with strange results, by default withdrawals cannot be disputed but it can be toggled to allow

Setup:

You will need the following...
- Python 3.10 (you can get it here: https://www.python.org/downloads/release/python-3100/) and add to path (you can google how to do that yourself)
- Pandas (can be installed by 'python pip install pandas' in terminal)
- Numpy (can be installed by 'python pip install numpy' in terminal)

To run:
- place csv with values like (with or without trailing and leading whitespace) in same directory as payment_engine (or figure out relative path to file):

    type, client, tx, amount
    deposit, 1, 1, 1.0
    deposit, 2, 2, 2.0
    deposit, 1, 3, 2.0
    withdrawal, 1, 4, 1.5
    withdrawal, 2, 5, 3.0
    ...

- execute command 'python payment_engine.py [path to your csv] > client_accounts.csv

The output will be a csv with the final state of accounts after transactions in you provided csv are applied in order

Other things:
There is some unused capabilities you can make use of by either modifying payment_engine.py main() method or by importing payment_engine.py to another
python module. The comments in payment_engine.py should cue you into what those are.

