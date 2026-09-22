data test;
  input id value;
  prev_value = lag(value);
  prev2_value = lag2(value);
  change = value - prev_value;
  datalines;
1 10
2 15
3 12
4 18
5 20
;
run;
proc print data=test noobs;
run;
