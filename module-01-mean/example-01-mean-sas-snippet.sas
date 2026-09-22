data test;
    input x y z;
    average = mean(x, y, z);
    datalines;
1 2 3
4 . 6
. . .
;
run;

proc print data=test noobs;
run;
