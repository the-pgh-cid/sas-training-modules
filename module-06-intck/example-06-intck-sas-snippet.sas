data test;
  input start_date :date9. end_date :date9.;
  days = intck('day', start_date, end_date);
  months = intck('month', start_date, end_date);
  years = intck('year', start_date, end_date);
  format start_date end_date date9.;
  datalines;
01JAN2023 15JAN2023
01JAN2023 01FEB2023
01JAN2023 31DEC2023
15MAR2023 20MAR2023
31JAN2023 01FEB2023
31DEC2023 01JAN2024
;
run;
proc print data=test noobs;
run;
