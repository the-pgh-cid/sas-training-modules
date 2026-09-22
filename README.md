# SAS to Python: LLM collaboration modules

Version 0.1.0 | 18 September 2026

Ten self-contained modules, three PDF pages each: (1) example and setup, (2) Prompt A and why, (3) Prompt B and why. Modules 01-05 are the starting sequence. Modules 06-10 are continuation examples; macro-conversion landmines remain for a later course.

## Start here

1. Open the module PDF.
2. Use the paired `.sas` file and copy a prompt from `prompts.md`. Attach the SAS file or paste its code after the prompt.
3. Use a fresh conversation for every attempt and keep the same source and setup for A and B. Both prompts use the same instruction to return code in the response, avoid creating or running files, and avoid reading existing Python files.
4. Save the initial response, then run and check the generated code separately. Record observations in `trial-log.md`.
5. Compare the requested behavior and expected values, as well as library and method choices. Agreement under A is a valid finding.

## Teaching intent

The learners know SAS and are new to LLM collaboration. Each module connects a familiar requirement to an explicit prompt instruction and a visible check. A leaves implementation choices open; B specifies key choices and behavior. The anti-pattern is accepting an unstated or unchecked assumption. A concise prompt can work well. A constrained prompt still needs checking.

Construct familiarity is a working explanation to investigate, not a measured training-data count. Three runs per variant provide examples for discussion; they do not establish population failure rates or guaranteed determinism.

## What was checked

Source semantics were reviewed against the linked SAS references. Local Python reference implementations passed the supplied and revised sample checks for all ten modules. The validation scripts and their output are in `validation/`. These checks establish the expected fixture results in Python. They are not repeated LLM generations, live Bedrock tests, or execution in SAS.

All SAS baseline executions and A/B trials for the revised prompts remain pending. Only the original MEAN transcripts were supplied. Expected-output tables show values for comparison; they are not captured SAS printouts. Character storage padding and alternate date displays are identified where relevant.

## Original MEAN evidence

Original MEAN evidence consists of six user-supplied transcripts dated 2026-09-17 by filename. Their headers identify Claude Code v2.1.274, Sonnet 4.5, and Amazon Bedrock. The broader authoring-session export identifies Claude Code v2.1.276. These original records accompany the teaching modules as historical evidence; they are not tests of any revised teaching prompt or revised SAS fixture. Revised prompts and examples 02-10 require fresh A/B trials before an observed-outcome claim is added. No original run is silently replaced or relabeled.

All three original A responses selected pandas and the same row-wise mean calculation. They displayed 2.0, 5.0, and NaN. Wording and code layout differed; A1 also offered a second version. These are displayed answers: the supplied A transcripts do not show the code being executed.

B1 created a Python file and reported a successful run. B2 and B3 encountered a write error, then read and ran an existing file. This shows a useful collaboration lesson: clearing the conversation did not remove the saved code. These records do not establish three independent B conversions.

The raw original logs are in `recorded-runs/mean-original/`. They are kept distinct from the blank logs for this edition. The shared response-only instruction is an addition to both teaching prompts, so the original transcripts must not be reported as tests of those revised prompts.

## Run the remaining trials

Keep the same model, initial instructions, SAS fixture, knowledge sources, and visible settings across all six attempts. Mark unavailable inference settings as unknown. Save three A and three B first responses in separate conversations. Do not carry prior outputs into later attempts. A separate clean working directory per run adds isolation when tool access is available. Preserve generated code and its execution output after the response has been captured.

## Source revisions and references

The original uploaded files remain unchanged. Module source copies, prompts, and explanations were adapted for a short teaching format. The companion snippets are the source to use with this edition. The common prompt policy and removal of unsupported predictions apply across all ten modules. Individual revisions follow.

### 01: MEAN: make missing values explicit

Adapted from `example-01-mean.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Added the same response-only policy to both prompts. The original MEAN records used earlier prompts; they are not trials of these revised prompts.
- Removed unsupported predictions about model training frequency and guarantees of identical or correct output. Describe open choices and checks instead.
- Expected results are derived from documented semantics and checked in local Python; SAS and AWS Bedrock execution remain pending.
- Preserved the original three input rows and MEAN calculation; added NOOBS for a compact SAS display.

- [SAS Functions Reference: MEAN, pp. 658-659](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/PDF/default/lefunctionsref.pdf)

### 02: SUBSTR: specify the positions

Adapted from `example-02-substr.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Added the same response-only policy to both prompts. The original MEAN records used earlier prompts; they are not trials of these revised prompts.
- Removed unsupported predictions about model training frequency and guarantees of identical or correct output. Describe open choices and checks instead.
- Expected results are derived from documented semantics and checked in local Python; SAS and AWS Bedrock execution remain pending.
- Corrected expected HelloWorld remainder to orld and SAS-to-Python remainder to -Python. The middle result to-P is retained.
- Removed the incorrect statement that Python text[0:3] is an off-by-one error; it is the correct translation of SUBSTR(text,1,3).
- Added explicit output widths 3, 4, 14 instead of SAS's implicit width inherited from text; input text remains width 20.
- Changed source reading to modified list input text :$20. for these no-space strings; comparisons distinguish stored padding from readable display.

- [SAS Functions Reference: SUBSTR (right of =), pp. 892-893](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/PDF/default/lefunctionsref.pdf)

### 03: LENGTH: say which spaces count

Adapted from `example-03-length.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Added the same response-only policy to both prompts. The original MEAN records used earlier prompts; they are not trials of these revised prompts.
- Removed unsupported predictions about model training frequency and guarantees of identical or correct output. Describe open choices and checks instead.
- Expected results are derived from documented semantics and checked in local Python; SAS and AWS Bedrock execution remain pending.
- Added one all-blank input row so the module verifies SAS LENGTH's documented return value of 1 for blank strings.
- Corrected the original trim-and-count recipe to include a minimum result of 1; limited trimming to ordinary trailing spaces.
- Removed the unsupported claim that row 2 contains distinctive source trailing spaces. The original two ABC rows are identical and both acquire storage padding.

- [SAS Functions Reference: LENGTH, pp. 617-618](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/PDF/default/lefunctionsref.pdf)

### 04: CAT: preserve the intended spaces

Adapted from `example-04-cat.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Added the same response-only policy to both prompts. The original MEAN records used earlier prompts; they are not trials of these revised prompts.
- Removed unsupported predictions about model training frequency and guarantees of identical or correct output. Describe open choices and checks instead.
- Expected results are derived from documented semantics and checked in local Python; SAS and AWS Bedrock execution remain pending.
- Corrected the source explanation: CAT preserves leading and trailing blanks in character arguments. CATS, not CAT, strips them.
- Retained CAT and CATX; did not replace CAT with CATS merely to match the former incorrect expected table.
- Corrected list-input character missing interpretation: unquoted period here produces blanks, not a literal period in the stored middle name.
- Changed Bob Smith to Bob . Smith so the intended missing middle and last name occupy distinct list-input fields.
- Declared input widths of 8 and result widths of 24 explicitly; the original implicit CAT/CATX result width was 200.
- Replaced all expected CAT results with padded, space-preserving strings and corrected CATX missing-value results.

- [SAS Functions Reference: CAT, pp. 263-265; CATX, pp. 274-276](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/PDF/default/lefunctionsref.pdf)

### 05: ROUND: keep the promise specific

Adapted from `example-05-round.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Added the same response-only policy to both prompts. The original MEAN records used earlier prompts; they are not trials of these revised prompts.
- Removed unsupported predictions about model training frequency and guarantees of identical or correct output. Describe open choices and checks instead.
- Expected results are derived from documented semantics and checked in local Python; SAS and AWS Bedrock execution remain pending.
- Preserved all five source inputs and their basic rounding results; halfway values remain excluded.
- Removed the incorrect blanket claim that floor(value + 0.5) fails for the supplied negative values; those specific values do round as expected by that expression.
- Avoided claims that these cases prove general equivalence between SAS ROUND and Python or pandas rounding.

- [SAS Functions Reference: ROUND, pp. 833-837](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/PDF/default/lefunctionsref.pdf)

### 06: INTCK

Adapted from `example-06-intck.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Added 31JAN2023 to 01FEB2023 and 31DEC2023 to 01JAN2024 as contrasting boundary tests; original four rows retained.
- Scoped explanation to default discrete INTCK on SAS dates; continuous, shifted, multiplied, custom, and datetime intervals excluded.
- Removed unsupported predictions about training exposure, failure frequency, and guaranteed output convergence.
- Removed blanket claim that dateutil.relativedelta yields discrete boundary counts without additional logic.
- Removed expected-output comments from runnable source; used PROC PRINT NOOBS for clean display.

- [SAS INTCK function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p1md4mx2crzfaqn14va8kt7qvfhr.htm)
- [pandas.to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)

### 07: COMPRESS

Adapted from `example-07-compress.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Corrected source narrative that called ka alphanumeric: k keeps the selected class; a selects alphabetic characters.
- Used $CHAR20. plus INFILE DATALINES TRUNCOVER to preserve literal characters and handle short input lines explicitly.
- Explicitly limited the regex translation to ASCII sample strings and compared content after omitting trailing SAS storage padding.
- Removed claims that the model will fail or that output diversity proves incorrectness.
- Removed expected-output comments from source; preserved input values and all expected content.

- [SAS COMPRESS function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0fcshr0ir3h73n1b845c4aq58hz.htm)
- [pandas.Series.str.replace](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.replace.html)

### 08: INPUT

Adapted from `example-08-input.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Added LENGTH char_num $8 char_date $9 before INPUT; original simple character list input otherwise limits char_date to eight bytes and truncates nine-character date text.
- Clarified calendar-date equivalence versus SAS internal numeric date storage and DATE9. display.
- Limited exercise to provided valid values; no general equivalence claim for invalid-input behavior or all BEST12. inputs.
- Removed unsupported assertions that SAS date formats are unlikely to be known by the model.
- Removed expected-output comments from source and used PROC PRINT NOOBS.

- [SAS INPUT function](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000180357.htm)
- [SAS INPUT statement: list input](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000144370.htm)
- [pandas.to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)

### 09: FIRST. / LAST.

Adapted from `example-09-firstvar.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Explicitly scoped to the already sorted sample, one grouping variable, and no missing groups; general multi-key and NOTSORTED behavior excluded.
- Clarified that FIRST./LAST. are automatic variables, not ordinary functions.
- Removed original claim that duplicated-based methods are inherently wrong: appropriately inverted first/last duplicated flags can be correct for these sorted groups.
- Prompt explicitly handles endpoints to avoid reliance on missing-value comparison behavior.
- Preserved all sample rows and SAS calculations; omitted expected-output comments and used PROC PRINT NOOBS.

- [SAS: How the DATA step identifies BY groups](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000761931.htm)
- [SAS: Preprocessing input data for BY groups](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a001125212.htm)
- [pandas.Series.shift](https://pandas.pydata.org/docs/reference/api/pandas.Series.shift.html)

### 10: LAG

Adapted from `example-10-lag.md` and its paired SAS snippet. Original MEAN snippet had no filename extension.

- Restricted LAG-to-shift equivalence to this program, where each function occurrence executes once for every row.
- Corrected the implication that conditional execution breaks LAG: it advances the queue only for the calls that occur and therefore needs different analysis.
- Removed claim that numpy.roll alone is equivalent; wraparound values would need replacement with missing values.
- Removed unsupported predictions of unanimous shift usage or guaranteed output consistency.
- Preserved original input and calculations; removed expected-output comments and used PROC PRINT NOOBS.

- [SAS LAG function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm)
- [pandas.Series.shift](https://pandas.pydata.org/docs/reference/api/pandas.Series.shift.html)

## Updating a module

Add actual run records to the trial log and preserve raw transcripts. Keep predicted results, locally checked values, SAS execution evidence, and LLM response observations explicitly identified. If the source or prompt changes, record the new version before repeating the A/B trials.
