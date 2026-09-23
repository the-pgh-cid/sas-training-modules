/* SAS reference authored for Base SAS. UNEXECUTED in this environment.
   Set APPENDIX_DIR to this directory (no trailing slash) before %include.
   Example:
     %let APPENDIX_DIR=/absolute/path/module-02-substr/appendix;
     %include "&APPENDIX_DIR/reference.sas";
   Ordinary ASCII character data only. Loader decodes numeric sentinel.
*/
%macro require_appendix_dir;
  %if not %symexist(APPENDIX_DIR) %then %do;
    %put ERROR: Set APPENDIX_DIR to the absolute appendix directory.;
    %abort cancel;
  %end;
%mend;
%require_appendix_dir;

%macro load_cases(out=appendix_cases);
data &out;
  length case_id $8 row_id $8 text $20 expected_text $20 expected_first_three $3 expected_middle $4 expected_from_seventh $14;
  infile "&APPENDIX_DIR/fixtures.csv" dsd dlm=',' firstobs=2
         truncover lrecl=32767;
  input
    case_id :$char8.
    row_id :$char8.
    text :$char20.
    expected_text :$char20.
    expected_first_three :$char3.
    expected_middle :$char4.
    expected_from_seventh :$char14.
  ;
  _seq = _n_;
run;
%mend;

%macro translate(in=, out=);
data &out;
  length text $20 first_three $3
         middle $4 from_seventh $14;
  set &in;
  first_three = substr(text, 1, 3);
  middle = substr(text, 5, 4);
  from_seventh = substr(text, 7);
run;
%mend;

/* Including this file loads the fixture and prints the reference output. */
%load_cases;
data fixture_input;
  set appendix_cases;
  where case_id = 'fixture';
run;
%translate(in=fixture_input, out=fixture_output);
proc print data=fixture_output noobs;
  var row_id text first_three middle from_seventh;
run;
