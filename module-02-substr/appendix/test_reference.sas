/* EXACTLY THREE named acceptance checks. SAS: AUTHORED, UNEXECUTED.
   From any SAS working directory, submit:
     %let APPENDIX_DIR=/absolute/path/module-02-substr/appendix;
     %include "&APPENDIX_DIR/test_reference.sas";
   Each check calls the reference translate macro; a mismatch aborts.
*/
%macro require_appendix_dir;
  %if not %symexist(APPENDIX_DIR) %then %do;
    %put ERROR: Set APPENDIX_DIR before including this harness.;
    %abort cancel;
  %end;
%mend;
%require_appendix_dir;
%include "&APPENDIX_DIR/reference.sas";
%global test_failed;

%macro finish_check(name=);
  %if &test_failed ne 0 %then %do;
    %put ERROR: FAIL &name;
    %abort cancel;
  %end;
  %put NOTE: PASS &name;
%mend;

%macro values_check(case=, name=);
  data check_input;
    set appendix_cases;
    where case_id = "&case";
  run;
  proc sql noprint;
    select count(*) into :expected_rows trimmed from check_input;
  quit;
  %translate(in=check_input, out=check_output);
  %let test_failed=1;
  data _null_;
    set check_output end=_is_last;
    retain bad 0 n 0;
    n + 1;
  if first_three ne expected_first_three then bad + 1;
  if middle ne expected_middle then bad + 1;
  if from_seventh ne expected_from_seventh then bad + 1;
  if text ne expected_text then bad + 1;
    if _is_last then do;
      if n ne &expected_rows or n = 0 then bad + 1;
      call symputx('test_failed', bad, 'G');
    end;
  run;
  %finish_check(name=&name);
%mend;

/* T1: the original teaching rows, including known expected values. */
%values_check(case=fixture, name=T1 original_fixture);
/* T2: added validation rows; these are not additional model trials. */
%values_check(case=edge, name=T2 added_boundary);

/* T3: reversed order, no input mutation, types and stored widths. */
proc sort data=appendix_cases out=contract_input;
  by descending _seq;
run;
data contract_before;
  set contract_input;
run;
%translate(in=contract_input, out=contract_output);
proc compare base=contract_before compare=contract_input noprint;
run;
%let preservation_rc=&sysinfo;
proc sql noprint;
  select count(*) into :expected_rows trimmed from contract_before;
quit;
%let test_failed=1;
data _null_;
  merge contract_output(in=has_output)
        contract_before(in=has_before keep=row_id case_id _seq text rename=(row_id=before_id case_id=before_case _seq=before_seq text=before_text)) end=_is_last;
  retain bad 0 n 0;
  n + 1;
  if not has_output or not has_before then bad + 1;
  if row_id ne before_id then bad + 1;
  if case_id ne before_case then bad + 1;
  if _seq ne before_seq then bad + 1;
  if text ne before_text then bad + 1;
  if vtype(text) ne 'C' or vlength(text) ne 20 then bad + 1;
  if vtype(first_three) ne 'C' or vlength(first_three) ne 3 then bad + 1;
  if vtype(middle) ne 'C' or vlength(middle) ne 4 then bad + 1;
  if vtype(from_seventh) ne 'C' or vlength(from_seventh) ne 14 then bad + 1;

  if first_three ne expected_first_three then bad + 1;
  if middle ne expected_middle then bad + 1;
  if from_seventh ne expected_from_seventh then bad + 1;
  if text ne expected_text then bad + 1;
  if _is_last then do;
    if n ne &expected_rows or n = 0 then bad + 1;
    if &preservation_rc ne 0 then bad + 1;
    call symputx('test_failed', bad, 'G');
  end;
run;
%finish_check(name=T3 preservation_type_order);
%put NOTE: Exactly 3 SAS acceptance checks passed in this SAS session.;
