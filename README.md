# Overview

Provide a quick method of extracting prow data and logs for analysis.

# Data Output

Data is collected and output to mimick a `must-gather`.  This allows other tools such as [omg](https://github.com/kxr/o-must-gather/) and CCX Insights to natively interface with prow test results.  This data is placed in the `out` folder relative to where `prowler.py` is run.

Additionally, the result of all prow jobs are output in a report shown at the completion of data extraction.

# Analyzing data with `omg`

~~~
omg use ./out

omg get co

omg get pods -A
~~~

# Plugins

Plugins are created by extending the `Handler` class and registering the class in `prowler.py`.