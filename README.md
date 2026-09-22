# Building Trust in LLM-Assisted SAS Conversion

**Purpose**: Demonstrate that prompt technique directly affects output consistency in LLM-assisted code translation.

**Audience**: Data scientists with SAS experience who need to understand how to elicit deterministic behavior from LLMs, without access to model parameter tuning.

## Structure

### Guide Documents
1. **01-why-output-varies.md** - Plain-language explanation of LLM output variability
2. **02-degrees-of-freedom.md** - The controllable factors in prompt design
3. **03-pattern-recognition.md** - What makes a prompt produce consistent output

### Example Set
Each example follows the format:
- One SAS code snippet
- Prompt A: Low-determinism approach
- Prompt B: High-determinism approach  
- Explanation of why outputs vary between approaches

Examples are designed to be run independently in any LLM interface to observe variance.

### Test Results Directory
`test-results/` - Reserved for recorded outputs from running examples across different sessions/models

## Usage

**For learners:**
1. Read the guide documents (01-03) to understand the conceptual framework
2. Run the examples yourself to observe the variance
3. Compare your results to the patterns described in the guide

**For instructors:**
Run examples across multiple sessions and document variance in `test-results/` to build evidence base for training materials.

## Current Status

- **Examples ready**: 5 (MEAN, SUBSTR, LENGTH, CAT, ROUND)
- **Guide status**: In development
- **Test corpus**: Awaiting results from independent testing
