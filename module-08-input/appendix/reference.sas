/* Authored SAS reference, NOT EXECUTED in this environment.
   Set %let APPENDIX_DIR=/absolute/path/to/this/appendix; before %include.
   Define APPENDIX_TEST_ONLY=1 when including from the test harness. */
options locale=en_US; /* English DATE9 input; controlled standalone session. */
%macro load_cases(out=cases);
  data &out;
    length case_id $7 char_num $8 char_date $9 expected_iso $10;
    infile "&APPENDIX_DIR/fixtures.csv" dsd dlm=',' firstobs=2 truncover;
    input case_id :$7. row_id char_num :$8. char_date :$9.
          expected_num_value expected_iso :$10.;
    expected_date_value = input(expected_iso, yymmdd10.);
    drop expected_iso;
  run;
%mend;
%macro transform(in=, out=);
  data &out;
    set &in;
    num_value = input(char_num, best12.);
    date_value = input(char_date, date9.);
    format date_value date9.;
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
      var char_num char_date num_value date_value;
    run;
  %end;
%mend;
%appendix_demo;
