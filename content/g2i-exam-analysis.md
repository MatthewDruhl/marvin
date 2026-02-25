# G2i DevSkiller Exam Analysis

**Date:** 2026-02-24
**Test:** Python Developer | Python 3 | Refactoring the SMS application
**Overall Score:** 46% (16/35 points)
**Result:** Rejected

---

## Section 1: Multiple Choice (12/15, 80%)

| Question | Score | Notes |
|----------|-------|-------|
| Class Inheritance (MRO) | 3/3 | Correct — knew Foo resolves first |
| List performance (middle removal) | 3/3 | Correct — O(n) |
| **Mutable Default Arguments** | **0/3** | **Missed — selected `[0, 1, 2]`, correct was `[0, 1, 0, 1, 2]`** |
| Operator overloading (`__add__`) | 3/3 | Correct |
| Generators vs list comprehensions | 3/3 | Correct — memory efficiency |

## Section 3: Code Refactoring (4/20, 20%)

### The Task
Refactor procedural SMS functions (`app/old.py`) into an OOP class hierarchy:
- `BaseSmsProvider` (abstract base class with chainable setters, validation decorator)
- `PrimarySmsApiProvider` (concrete, extends base)
- `SecondarySmsApiProvider` (concrete, extends base)
- `sms_factory()` function (factory pattern, returns correct provider instance)

### What Passed
- `sms_factory` implementation (dictionary dispatch, NotImplementedError for unknown)
- `_process_response` on PrimarySmsApiProvider (status check, tuple return)
- All structure tests (class/method signatures existed)

### What Failed and Why

**1. Methods defined inside other methods (indentation/nesting)**
- Defined `_validate_set_content` and `_validate_set_recipient` inside the `set_content` method body in `base.py`
- Should have been separate class-level methods
- Root cause: misunderstanding of Python class structure / indentation significance

**2. Missing `self.` on method calls**
- Wrote `if not _validate_set_content():` instead of `self._validate_set_content()`
- Caused `NameError` that failed 4 Primary tests
- Root cause: forgetting that methods on the same class still need `self.` prefix

**3. Undefined variables in `_prepare_payload`**
- Used `country_code` (not in scope)
- Used `self.phone` (attribute was stored as `self.recipient`)
- Used `API_KEY` (needed settings reference or class constant)
- Root cause: not tracking variable names from the existing codebase

**4. SecondarySmsApiProvider not implemented (Task 4)**
- Class left completely empty
- All 3 secondary tests failed with AttributeError
- Root cause: ran out of time (1:46 spent on 1:30 suggested)

**5. Time management**
- Section 4 (video) skipped entirely
- Overran suggested time by 16 minutes on Section 3
- Didn't prioritize completing all tasks partially before perfecting any one task

### Test Results Detail

| Test | Result | Error |
|------|--------|-------|
| test_primary_factory | PASS | — |
| test_process_response_method_ok | PASS | — |
| test_recipient_not_set (Primary) | FAIL | NameError: `_validate_set_content` not defined |
| test_api_response (Primary) | FAIL | NameError: `_validate_set_content` not defined |
| test_api_wrong_auth_key (Primary) | FAIL | NameError: `_validate_set_content` not defined |
| test_compare_old_and_new (Primary) | FAIL | NameError: `_validate_set_content` not defined |
| test_recipient_not_set (Secondary) | FAIL | AttributeError: no `set_content` |
| test_api_response (Secondary) | FAIL | AttributeError: no `set_recipient` |
| test_compare_old_and_new (Secondary) | FAIL | AttributeError: no `set_recipient` |

---

## Skills Gap Summary

### Direct Failures (caused lost points)
1. Mutable default arguments (Python gotcha)
2. `self.method()` vs bare `method()` calls
3. Variable scoping in class methods
4. Method nesting vs class-level method definition
5. Time management under exam pressure

### Concepts That Need Practice
1. Factory design pattern
2. Chainable methods (`return self`)
3. Refactoring procedural code → OOP
4. Reading and extending unfamiliar codebases
5. Abstract base class with concrete implementations
6. Decorator patterns (the `_validation` wrapper)

---

*Analysis created 2026-02-25 by MARVIN*
