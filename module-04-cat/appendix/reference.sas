/* SAS reference authored for Base SAS. UNEXECUTED in this environment.
   Set APPENDIX_DIR to this directory (no trailing slash) before %include.
   Example:
     %let APPENDIX_DIR=/absolute/path/module-04-cat/appendix;
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
  length case_id $8 row_id $8 first $8 middle $8 last $8 expected_first $8 expected_middle $8 expected_last $8 expected_name1 $24 expected_name2 $24;
  infile "&APPENDIX_DIR/fixtures.csv" dsd dlm=',' firstobs=2
         truncover lrecl=32767;
  input
    case_id :$char8.
    row_id :$char8.
    first :$char8.
    middle :$char8.
    last :$char8.
    expected_first :$char8.
    expected_middle :$char8.
    expected_last :$char8.
    expected_name1 :$char24.
    expected_name2 :$char24.
  ;
  _seq = _n_;
run;
%mend;

%macro translate(in=, out=);
data &out;
  length first middle last $8
         name1 name2 $24;
  set &in;
  name1 = cat(first, middle, last);
  name2 = catx(' ', first, middle, last);
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
  var row_id first middle last name1 name2;
run;
