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
  length case_id $8 row_id value expected_rounded 8;
  length _value _expected_rounded $40;
  input case_id :$8. row_id :best32. _value :$40. _expected_rounded :$40.;
  if _value='__MISSING__' then value=.;
  else value=input(_value,best32.);
  if _expected_rounded='__MISSING__' then expected_rounded=.;
  else expected_rounded=input(_expected_rounded,best32.);
  drop _value _expected_rounded;
run;
filename appcsv clear;
%mend;

%macro transform(in=, out=);
data &out;
  set &in;
  rounded = round(value);
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
      var value rounded;
    run;
  %end;
%mend;
%fixture_demo;
