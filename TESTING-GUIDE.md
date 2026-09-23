# Testing Guide for Onboarding Examples

> **Current edition, 23 September 2026:** Use each module's `prompts.md` and paired SAS snippet for exact historical trial inputs. See [APPENDICES.md](APPENDICES.md) for new reference implementations and acceptance tests, and [PDF-BUILD.md](PDF-BUILD.md) for reported trial evidence. The paths and predicted model behavior below belong to the original planning guide; they are not findings from the completed trial summaries.

## Quick Start

Each example has two files:
- `example-NN-[name]-sas-snippet.sas` - Standalone SAS code (can upload to LLM)
- `example-NN-[name].md` - Full documentation with Prompt A and Prompt B

## Testing Workflow

### 1. Choose an Example
Start with example-06 (INTCK) or example-07 (COMPRESS) to see actual variance.

### 2. Run Prompt A (3-5 times)
- Open fresh LLM session
- Copy Prompt A from the .md file (or upload the .sas snippet with "Convert this to Python")
- Record output in `test-results/`
- **Name pattern**: `20260917-e[NN]-[name]-pA-t[N].txt`
- Close session, repeat 3-5 times

### 3. Run Prompt B (3-5 times)
- Open fresh LLM session for each run
- Copy full Prompt B text from the .md file
- Record output in `test-results/`
- **Name pattern**: `20260917-e[NN]-[name]-pB-t[N].txt`

### 4. Analyze Variance
Compare outputs:
- **Prompt A**: Count unique approaches (library choices, methods)
- **Prompt B**: Count unique approaches (should be minimal)
- **Correctness**: Do outputs match expected SAS values?

## Recommended Testing Priority

### Option 1: Show Variance First (For Skeptics)
Demonstrate the problem before explaining the solution.

1. **Example-06 (INTCK)** - Date intervals
   - High variance expected in Prompt A
   - Likely errors in month counting (semantic confusion)
   - Shows where model priors fail

2. **Example-07 (COMPRESS)** - Character removal
   - Maximum variance expected
   - 'ka' modifier likely misunderstood in Prompt A
   - Shows domain-specific notation problem

3. **Example-02 (SUBSTR)** - String slicing
   - Off-by-one errors expected in Prompt A
   - Clear demonstration of index basis trap

4. **Example-01 (MEAN)** - Already tested
   - Use existing results to show that even "working" examples are lucky

### Option 2: Build Understanding Gradually
Start simple, increase complexity.

1. **Example-01 (MEAN)** - Already tested
2. **Example-05 (ROUND)** - Basic, should work well
3. **Example-10 (LAG)** - Moderate complexity
4. **Example-02 (SUBSTR)** - Introduce traps
5. **Example-06 (INTCK)** - High complexity

### Option 3: Systematic (All 10 in Order)
Examples 01-10 are ordered by increasing complexity/variance.

## What to Observe

### Low Variance Examples (MEAN, ROUND, LAG)
- **Prompt A**: May show consistency due to strong model priors
- **Learning**: Lucky consistency is not reliability
- **Key point**: Cannot predict which constructs will be lucky

### High Variance Examples (INTCK, COMPRESS, FIRST.var)
- **Prompt A**: Expect 4-5 completely different approaches
- **Learning**: Model has weak priors for domain-specific constructs
- **Key point**: Constraints are critical, not optional

### Trap Examples (SUBSTR, LENGTH)
- **Prompt A**: May look correct but have subtle errors
- **Learning**: Silent failures are dangerous
- **Key point**: Verification against SAS output is mandatory

## Quick Variance Check

For each example, count:
1. **Library choices** (pandas, numpy, built-in, other)
2. **Method choices** (for same library, different approaches)
3. **Correctness** (matches SAS expected output?)

**High variance signal:**
- Prompt A: 3+ different approaches across 5 runs
- Prompt B: 1-2 approaches across 5 runs

## Expected Results Summary

| Example | Expected Prompt A Variance | Primary Failure Mode |
|---------|---------------------------|---------------------|
| 01 MEAN | LOW (lucky) | None (may work correctly) |
| 02 SUBSTR | MODERATE-HIGH | Off-by-one indexing |
| 03 LENGTH | MODERATE | Wrong length (includes spaces) |
| 04 CAT | HIGH | Not stripping spaces |
| 05 ROUND | LOW-MODERATE | None (should work) |
| 06 INTCK | VERY HIGH | Wrong month counting |
| 07 COMPRESS | MAXIMUM | 'ka' modifier confusion |
| 08 INPUT | VERY HIGH | Date format parsing failure |
| 09 FIRST.var | MAXIMUM | Conceptual misunderstanding |
| 10 LAG | MODERATE | Different methods, mostly correct |

## Analysis Template

For each example tested, document:

```markdown
## Example-[NN]: [Name]

**Test Date**: YYYY-MM-DD
**Model**: [LLM name/version]

### Prompt A Results (N runs)
- **Unique approaches**: [count]
- **Library choices**: [pandas: X, numpy: Y, other: Z]
- **Correct outputs**: [N out of M]
- **Common errors**: [list]

### Prompt B Results (N runs)
- **Unique approaches**: [count] (should be 1-2)
- **Correct outputs**: [should be N out of N]

### Variance Analysis
- Prompt A: [HIGH/MODERATE/LOW]
- Prompt B: [Should be LOW]
- **Key finding**: [What did this example demonstrate?]
```

## Tips

### For Efficiency
- Test high-variance examples first (06, 07, 09) - most instructive
- Can skip testing obvious cases if time-limited
- 3 runs per prompt is minimum; 5 is better for statistical confidence

### For Documentation Quality
- Save complete LLM output, not just code snippet
- Include any explanations or reasoning the model provided
- Note any errors or warnings in output

### For Presenting Results
- Compare side-by-side: Prompt A variance vs Prompt B consistency
- Highlight: Correctness matters more than consistency (consistent wrong answers are worse than varying correct answers)
- Emphasize: Constraints FORCE both consistency AND correctness
