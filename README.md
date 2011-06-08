# How to use

You need to grab the HTML page for netflix instant streaming history
(https://account.netflix.com/WiViewingActivity). I found that using "save
page"  in Chrome only gave me the most recent viewings, and that I had to use
the inspector to grab the rest of the times.

Once you have the html in a file, call the script with that file as the
first argument. file will be parsed and will output viewing times by month and
day of the week. Doesn't currently split on years, will do that eventually.
