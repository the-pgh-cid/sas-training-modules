# Onboarding Materials Status

> **Current PDF status, 23 September 2026:** All ten PDFs contain the preserved three-page v0.2 lesson plus a two-page SAS/Python/R and acceptance-test appendix. Use [APPENDICES.md](APPENDICES.md) for current execution status and rebuild instructions. The status, paths and predictions below are historical planning notes, not the current trial status.

**Created**: 2026-09-17 09:35am
**Purpose**: Trust-building materials for LLM-assisted SAS conversion

## Completed

### Guide Documents
- ✅ `README.md` - Project overview and structure
- ✅ `01-why-output-varies.md` - Plain language explanation of LLM variance
- ✅ `02-degrees-of-freedom.md` - Controllable factors in prompt design
- ✅ `03-pattern-recognition.md` - Recognizing high/low variance prompt patterns

### Examples
- ✅ `examples/example-01-mean.md` - Complete template for MEAN function
  - SAS code with expected output
  - Prompt A (high degrees of freedom)
  - Prompt B (low degrees of freedom)
  - Explanation of what each leaves unspecified/specifies
  - Testing instructions
  - Expected learning outcomes

### Infrastructure
- ✅ `test-results/` directory for recording independent test runs

## Pending

### Testing Results
- ✅ **Example-01 tested** (2026-09-17, Sonnet 4.5)
  - Surprising result: ZERO variance in Prompt A (strong model priors for pandas)
  - Critical learning: Constraints needed even when priors seem strong
  - Full analysis: `test-results/ANALYSIS-example-01.md`

### Examples Completed (10 total)
- ✅ `example-01-mean` - Statistical aggregation (common, lucky consistency)
- ✅ `example-02-substr` - String slicing (indexing trap)
- ✅ `example-03-length` - String length (silent failure trap)
- ✅ `example-04-cat` - String concatenation (multiple idioms)
- ✅ `example-05-round` - Basic rounding (calibration example - simple case)
- ✅ `example-06-intck` - Date intervals (domain-specific, high variance expected)
- ✅ `example-07-compress` - Character removal (modifier system, maximum variance)
- ✅ `example-08-input` - Type conversion (format notation translation)
- ✅ `example-09-firstvar` - BY-group boundaries (idiom translation, maximum complexity)
- ✅ `example-10-lag` - Previous value (universal concept, moderate variance)

### Example Spectrum Document
- ✅ `EXAMPLE-SPECTRUM.md` - Explains ordering, teaching points, variance expectations

### Future (102-level)
- Landmine examples (rounding half-away, missing value sorts, PROC FREQ denominators)
- AWS-specific constructs (KB declaration via MCP)
- Multi-step workflows
- Complex edge cases

## Next Actions

1. ✅ **DONE**: User tested example-01, provided results
2. ✅ **DONE**: Analysis documented, example updated with actual findings
3. ✅ **DONE**: All 10 examples built with .sas snippets + .md documentation
4. **READY FOR TESTING**: User can test examples 02-10 to observe variance spectrum
5. **PENDING**: Guide document iteration based on feedback
6. **PENDING**: Consider cross-model testing if additional LLM access becomes available

## Notes

- Guide emphasizes trust-building through output consistency, not DMF evangelism
- Plain language throughout, concepts data scientists already understand
- Examples designed as test fixtures, not just documentation
- User testing independently and reporting variance observed

## Key Learning from Example-01 Test

**The "lucky consistency" problem**: Strong model priors can mask the need for constraints on common patterns. This makes the teaching harder (can't just show variance and say "see?"), but more important (users will encounter lucky consistency and wrongly conclude constraints don't matter).

**Updated teaching approach**: 
- Acknowledge when priors produce consistency
- Emphasize: Relying on priors = gambling, not engineering
- Need mix of examples: common (shows lucky consistency) + uncommon (shows actual variance)
