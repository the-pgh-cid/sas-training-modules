/* THREE NAMED SAS ACCEPTANCE TESTS: AUTHORED, UNEXECUTED.
   In SAS, set APPENDIX_DIR to this directory before including this file.
   %let APPENDIX_DIR=/absolute/path/module-08-input/appendix;
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
    if num_value ne expected_num_value or date_value ne expected_date_value then do;
      put "ERROR: &test value or missing-position mismatch";
      abort cancel;
    end;
    if last then put "PASS &test";
  run;
%mend;

%macro test_T1_known_answer;
  %check_values(case=fixture, n=3, test=T1_original_fixture);
%mend;
%macro test_T2_boundary;
  %check_values(case=edge, n=2, test=T2_valid_leap_day_and_numeric_boundary);
%mend;
%macro test_T3_contract;
  %local compare_rc;
  data contract_source; set cases; run;
  proc sort data=contract_source; by descending row_id; run;
  data source_snapshot; set contract_source; run;
  %transform(in=contract_source, out=contract_actual);
  %require_count(data=contract_actual, n=5, test=T3_source_order_and_result_types);
  proc compare base=source_snapshot compare=contract_actual noprint;
    var char_num char_date;
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
    if vtype(char_num) ne 'C' or vtype(char_date) ne 'C' or
       vtype(num_value) ne 'N' or vtype(date_value) ne 'N' or
       upcase(vformat(date_value)) ne 'DATE9.' then do;
      put 'ERROR: T3 output type or representation contract failed';
      abort cancel;
    end;
    if num_value ne expected_num_value or date_value ne expected_date_value then do;
      put 'ERROR: T3 output values or missing positions changed';
      abort cancel;
    end;
    if last then put 'PASS T3_source_order_and_result_types';
  run;
%mend;

%test_T1_known_answer;
%test_T2_boundary;
%test_T3_contract;
