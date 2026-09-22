data test;
  infile datalines truncover;
  input text $char20.;
  no_spaces = compress(text);
  no_digits = compress(text, '0123456789');
  only_letters = compress(text, '', 'ka');
  datalines;
ABC 123 XYZ
Phone: 555-1234
ID-2023-Q4
;
run;
proc print data=test noobs;
run;
