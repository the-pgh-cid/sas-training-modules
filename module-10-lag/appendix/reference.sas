/* Authored SAS reference, NOT EXECUTED in this environment.
   Set %let APPENDIX_DIR=/absolute/path/to/this/appendix; before %include.
   Define APPENDIX_TEST_ONLY=1 when including from the test harness. */
%macro load_cases(out=cases);
  data &out;
    length case_id $7 _ep _e2 _ec $16;
    infile "&APPENDIX_DIR/fixtures.csv" dsd dlm=',' firstobs=2 truncover;
    input case_id :$7. id value _ep :$16. _e2 :$16. _ec :$16.;
    if _ep = '__MISSING__' then expected_prev_value = .;
    else expected_prev_value = input(_ep, best32.);
    if _e2 = '__MISSING__' then expected_prev2_value = .;
    else expected_prev2_value = input(_e2, best32.);
    if _ec = '__MISSING__' then expected_change = .;
    else expected_change = input(_ec, best32.);
    drop _ep _e2 _ec;
  run;
%mend;
%macro transform(in=, out=);
  data &out;
    set &in;
    prev_value = lag(value);
    prev2_value = lag2(value);
    change = value - prev_value;
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
      var id value prev_value prev2_value change;
    run;
  %end;
%mend;
%appendix_demo;
