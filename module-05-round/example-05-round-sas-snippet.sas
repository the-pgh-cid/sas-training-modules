data test;
    input value;
    rounded = round(value);
    datalines;
2.3
2.7
-1.4
-1.6
3.0
;
run;

proc print data=test noobs;
run;
