/* Authored SAS reference, NOT EXECUTED in this environment.
   Set %let APPENDIX_DIR=/absolute/path/to/this/appendix; before %include.
   Define APPENDIX_TEST_ONLY=1 when including from the test harness. */
%macro load_cases(out=cases);
  data &out;
    length case_id $7 group $8;
    infile "&APPENDIX_DIR/fixtures.csv" dsd dlm=',' firstobs=2 truncover;
    input case_id :$7. id group :$8. value
          expected_first_flag expected_last_flag;
  run;
%mend;
%macro transform(in=, out=);
  data &out;
    set &in;
    by group;
    first_flag = first.group;
    last_flag = last.group;
  run;
%mend;
%macro appendix_demo;
  %if not %symexist(APPENDIX_TEST_ONLY) %then %do;
    %load_cases(out=appendix_cases);
    data fixture_source;
      set appendix_cases;
      where case_id = 'fixture';
    run;
    %transform(in=fixture_source, out=fixture_result);
    proc print data=fixture_result noobs;
      var id group value first_flag last_flag;
    run;
  %end;
%mend;
%appendix_demo;
