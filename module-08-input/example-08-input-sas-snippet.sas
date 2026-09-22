data test;
  length char_num $8 char_date $9;
  input char_num $ char_date $;
  num_value = input(char_num, best12.);
  date_value = input(char_date, date9.);
  format date_value date9.;
  datalines;
123 15JAN2023
456 01FEB2023
789 31DEC2023
;
run;
proc print data=test noobs;
run;
