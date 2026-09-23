/* SAS reference authored for Base SAS. UNEXECUTED in this environment.
   Set APPENDIX_DIR to this directory (no trailing slash) before %include.
   Example:
     %let APPENDIX_DIR=/absolute/path/module-01-mean/appendix;
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
  length case_id $8 row_id $8 _raw0 $32 _raw1 $32 _raw2 $32 _raw3 $32;
  infile "&APPENDIX_DIR/fixtures.csv" dsd dlm=',' firstobs=2
         truncover lrecl=32767;
  input
    case_id :$char8.
    row_id :$char8.
    _raw0 :$char32.
    _raw1 :$char32.
    _raw2 :$char32.
    _raw3 :$char32.
  ;
  if _raw0 = "__MISSING__" then x = .;
  else x = input(_raw0, best32.);
  if _raw1 = "__MISSING__" then y = .;
  else y = input(_raw1, best32.);
  if _raw2 = "__MISSING__" then z = .;
  else z = input(_raw2, best32.);
  if _raw3 = "__MISSING__" then expected_average = .;
  else expected_average = input(_raw3, best32.);
  drop _raw0 _raw1 _raw2 _raw3;
  _seq = _n_;
run;
%mend;

%macro translate(in=, out=);
data &out;
  set &in;
  average = mean(x, y, z);
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
  var row_id x y z average;
run;
