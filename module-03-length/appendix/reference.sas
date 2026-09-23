/* SAS reference authored for Base SAS. UNEXECUTED in this environment.
   Set APPENDIX_DIR to this directory (no trailing slash) before %include.
   Example:
     %let APPENDIX_DIR=/absolute/path/module-03-length/appendix;
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
  length case_id $8 row_id $8 text $10 expected_text $10 _raw0 $32;
  infile "&APPENDIX_DIR/fixtures.csv" dsd dlm=',' firstobs=2
         truncover lrecl=32767;
  input
    case_id :$char8.
    row_id :$char8.
    text :$char10.
    expected_text :$char10.
    _raw0 :$char32.
  ;
  if _raw0 = "__MISSING__" then expected_len = .;
  else expected_len = input(_raw0, best32.);
  drop _raw0;
  _seq = _n_;
run;
%mend;

%macro translate(in=, out=);
data &out;
  length text $10;
  set &in;
  len = length(text);
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
  var row_id text len;
run;
