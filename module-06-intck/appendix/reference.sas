/* UNEXECUTED: SAS is not available in the authoring environment.
   Set APPENDIX_DIR to the absolute appendix directory before %include.
   Without APPENDIX_DIR, paths are relative to the current SAS working directory.
   APPENDIX_TESTING=1 suppresses the fixture demonstration when sourced by tests. */
%macro appendix_path;
  %if not %symexist(APPENDIX_DIR) %then %do;
    %global APPENDIX_DIR;
    %let APPENDIX_DIR=.;
  %end;
%mend;
%appendix_path;

%macro load_fixtures(out=shared);
filename appcsv "&APPENDIX_DIR/fixtures.csv";
data &out;
  infile appcsv dsd dlm=',' firstobs=2 truncover lrecl=32767;
  length case_id $8 row_id start_date end_date 8;
  length expected_days expected_months expected_years 8;
  length _start _end $9 _days _months _years $40;
  input case_id :$8. row_id :best32. _start :$9. _end :$9.
        _days :$40. _months :$40. _years :$40.;
  start_date=input(_start,date9.);
  end_date=input(_end,date9.);
  if _days='__MISSING__' then expected_days=.;
  else expected_days=input(_days,best32.);
  if _months='__MISSING__' then expected_months=.;
  else expected_months=input(_months,best32.);
  if _years='__MISSING__' then expected_years=.;
  else expected_years=input(_years,best32.);
  format start_date end_date date9.;
  drop _start _end _days _months _years;
run;
filename appcsv clear;
%mend;

%macro transform(in=, out=);
data &out;
  set &in;
  days = intck('day',
    start_date, end_date);
  months = intck('month',
    start_date, end_date);
  years = intck('year',
    start_date, end_date);
  format start_date end_date date9.;
run;
%mend;

%macro fixture_demo;
  %if not %symexist(APPENDIX_TESTING) %then %do;
    %load_fixtures(out=shared);
    data fixture_input;
      set shared;
      where case_id='fixture';
    run;
    %transform(in=fixture_input,out=fixture_result);
    proc print data=fixture_result noobs;
      var start_date end_date days months years;
    run;
  %end;
%mend;
%fixture_demo;
