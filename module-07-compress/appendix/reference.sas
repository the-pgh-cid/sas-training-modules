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
  length case_id $8 row_id 8 text $20;
  length expected_no_spaces expected_no_digits expected_only_letters $20;
  input case_id :$8. row_id :best32. text :$char20.
        expected_no_spaces :$char20. expected_no_digits :$char20.
        expected_only_letters :$char20.;
run;
filename appcsv clear;
%mend;

%macro transform(in=, out=);
data &out;
  set &in;
  no_spaces = compress(text);
  no_digits = compress(text,
    '0123456789');
  only_letters = compress(text, '', 'ka');
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
      var text no_spaces no_digits only_letters;
    run;
  %end;
%mend;
%fixture_demo;
