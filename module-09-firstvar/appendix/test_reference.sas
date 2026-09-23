/* THREE NAMED SAS ACCEPTANCE TESTS: AUTHORED, UNEXECUTED.
   In SAS, set APPENDIX_DIR to this directory before including this file.
   %let APPENDIX_DIR=/absolute/path/module-09-firstvar/appendix;
   %include "&APPENDIX_DIR/test_reference.sas";
   A failed check issues ERROR and aborts. Python/R execution is not SAS proof. */
%let APPENDIX_TEST_ONLY=1;
%include "&APPENDIX_DIR/reference.sas";
%load_cases(out=cases);

%macro require_count(data=, n=, test=);
  %local actual_n;
  proc sql noprint;
    select count(*) into :actual_n trimmed from &data;
  quit;
  %if &actual_n ne &n %then %do;
    %put ERROR: &test expected &n rows, received &actual_n.;
    %abort cancel;
  %end;
%mend;

%macro check_values(case=, n=, test=);
  data sample;
    set cases;
    where case_id="&case";
  run;
  %require_count(data=sample, n=&n, test=&test);
  %transform(in=sample, out=actual);
  %require_count(data=actual, n=&n, test=&test);
  data _null_;
    set actual end=last;
    if first_flag ne expected_first_flag or last_flag ne expected_last_flag then do;
      put "ERROR: &test value or missing-position mismatch";
      abort cancel;
    end;
    if last then put "PASS &test";
  run;
%mend;

%macro test_T1_known_answer;
  %check_values(case=fixture, n=6, test=T1_original_fixture);
%mend;
%macro test_T2_boundary;
  %check_values(case=edge, n=1, test=T2_single_row_has_both_explicit_flags);
%mend;
%macro test_T3_contract;
  %local compare_rc;
  data contract_source; set cases; where case_id='fixture'; run;
  data source_snapshot; set contract_source; run;
  %transform(in=contract_source, out=contract_actual);
  %require_count(data=contract_actual, n=6, test=T3_preserve_rows_and_integer_flags);
  proc compare base=source_snapshot compare=contract_actual noprint;
    var id group value;
  run;
  %let compare_rc=&sysinfo;
  %if &compare_rc ne 0 %then %do;
    %put ERROR: T3 source columns or row order changed.;
    %abort cancel;
  %end;
  proc compare base=source_snapshot compare=contract_source noprint;
  run;
  %let compare_rc=&sysinfo;
  %if &compare_rc ne 0 %then %do;
    %put ERROR: T3 input data set changed.;
    %abort cancel;
  %end;
  data _null_;
    set contract_actual end=last;
    if vtype(first_flag) ne 'N' or vtype(last_flag) ne 'N' or
       first_flag not in (0,1) or last_flag not in (0,1) then do;
      put 'ERROR: T3 output type or representation contract failed';
      abort cancel;
    end;
    if first_flag ne expected_first_flag or last_flag ne expected_last_flag then do;
      put 'ERROR: T3 output values or missing positions changed';
      abort cancel;
    end;
    if last then put 'PASS T3_preserve_rows_and_integer_flags';
  run;
%mend;

%test_T1_known_answer;
%test_T2_boundary;
%test_T3_contract;
