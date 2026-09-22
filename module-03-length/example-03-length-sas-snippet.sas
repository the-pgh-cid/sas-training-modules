data test;
    length text $10;
    input text $;
    len = length(text);
    datalines;
ABC
ABC
ABCDEFGHIJ
X
.
;
run;

proc print data=test noobs;
run;
