/* UNEXECUTED ACCEPTANCE HARNESS: exactly three named tests.
   Run instructions are in README.md. Tests call the same transform macro
   used by reference.sas and read fixtures.csv, including its expected columns.
   SAS character equality ignores trailing storage padding; internal and leading
   blanks remain significant. Failure aborts this submitted program. */
%let APPENDIX_TESTING=1;
%macro test_path;
  %if not %symexist(APPENDIX_DIR) %then %do;
    %put ERROR: Set APPENDIX_DIR to an absolute appendix path first.;
    %abort cancel;
  %end;
%mend;
%test_path;
%include "&APPENDIX_DIR/reference.sas";
%load_fixtures(out=shared);

%macro assert_values(data=, count=, label=);
  %local observed bad;
  proc sql noprint;
    select count(*) into :observed trimmed from &data;
    select count(*) into :bad trimmed from &data
      where no_spaces ne expected_no_spaces or no_digits ne expected_no_digits or only_letters ne expected_only_letters;
  quit;
  %if &observed ne &count or &bad ne 0 %then %do;
    %put ERROR: &label row count or expected values failed.;
    %abort cancel;
  %end;
%mend;

%macro test_T1_original_fixture_known_answers;
  data t1_input;
    set shared;
    where case_id='fixture';
  run;
  %transform(in=t1_input,out=t1_actual);
  %assert_values(data=t1_actual,count=3,label=T1);
  %put PASS T1 original_fixture_known_answers;
%mend;

%macro test_T2_added_in_scope_boundaries;
  data t2_input;
    set shared;
    where case_id='edge';
  run;
  %transform(in=t2_input,out=t2_actual);
  %assert_values(data=t2_actual,count=5,label=T2);
  %put PASS T2 added_in_scope_boundaries;
%mend;

%macro test_T3_preservation_types_and_order;
  %local source_status contract_status wrong_types result_count;
  data t3_input;
    do point=total to 1 by -1;
      set shared point=point nobs=total;
      order_id=total-point+1;
      output;
    end;
    stop;
  run;
  data t3_before;
    set t3_input;
  run;
  %transform(in=t3_input,out=t3_actual);
  %assert_values(data=t3_actual,count=8,label=T3);
  proc compare base=t3_before compare=t3_input criterion=0 method=absolute noprint;
  run;
  %let source_status=&sysinfo;
  proc compare base=t3_before
    compare=t3_actual(keep=case_id row_id text expected_no_spaces expected_no_digits expected_only_letters order_id) criterion=0 method=absolute noprint;
  run;
  %let contract_status=&sysinfo;
  proc contents data=t3_actual out=t3_metadata noprint;
  run;
  proc sql noprint;
    select count(*) into :result_count trimmed from t3_metadata
      where upcase(name) in ('NO_SPACES', 'NO_DIGITS', 'ONLY_LETTERS');
    select count(*) into :wrong_types trimmed from t3_metadata
      where upcase(name) in ('NO_SPACES', 'NO_DIGITS', 'ONLY_LETTERS')
        and type ne 2;
  quit;
  %if &source_status ne 0 or &contract_status ne 0 or &wrong_types ne 0 or &result_count ne 3 %then %do;
    %put ERROR: T3 input preservation, ordering or result types failed.;
    %abort cancel;
  %end;
  %put PASS T3 preservation_types_and_order;
%mend;

%test_T1_original_fixture_known_answers;
%test_T2_added_in_scope_boundaries;
%test_T3_preservation_types_and_order;
%put All 3 named SAS acceptance checks completed.;
