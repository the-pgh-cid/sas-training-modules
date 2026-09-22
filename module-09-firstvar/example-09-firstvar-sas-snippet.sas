data test;
  input id group $ value;
  datalines;
1 A 10
2 A 20
3 B 30
4 B 40
5 B 50
6 C 60
;
run;
data flagged;
  set test;
  by group;
  first_flag = first.group;
  last_flag = last.group;
run;
proc print data=flagged noobs;
run;
