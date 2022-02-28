WIP

Testing folder will contain a python module that tests payment_engine and reports... When I get to doing that...

This module would print a test report detailing which methods failed etc and contain expansive tests for PaymentEngine object

In this directory are some input files used to test. The same file was edited so they don't reflect all the testing
 done. Not much testing with large data sets was done but some strategy went into design so it *should* be ok. 
 Honestly anything python is dicy with large data sets. The main concern is getting near O(1) look ups on past transactions
 and client information without ballooning resource usage too bad. I ran out of time to really test and iterate the
 design so handling large data sets is all theorectical right now...