# Examples

## Good case

Example assumptions: the supplied feature evidence shows that the fifth failed attempt immediately locks the account for 15 minutes. The QA environment provides an unlocked synthetic account, so the tester can start from a known state.

### QA-001 — Fifth failed sign-in shows the temporary lockout

- **ID:** QA-001
- **Title:** Fifth failed sign-in shows the temporary lockout
- **Priority:** High
- **Platform:** Web
- **Precondition:** Use an unlocked test account with no prior failed attempts.
- **Test Data:** qa.user.1@example.test and an invalid test password.

**Steps**

1. Open the sign-in page.
2. Submit four sign-in attempts with the invalid test password.
3. Submit a fifth sign-in attempt with the same invalid test password.

**Expected Result**

1. After step 3, the page shows “Too many attempts. Try again in 15 minutes.”

- **Basis:** Code
- **Status:** Not run

## How to adapt this example

If the change also establishes when the lock expires, cover that boundary separately when QA can control the clock or reproduce the elapsed time. If the timing or reset is unavailable, put it under Questions. When several cases need the same account, define its alias and reset instructions once in Summary and add case-specific setup only where it differs.

For a different workflow, keep the pattern and change the evidence. For example, in a shared workspace test that needs two roles, name which user performs the action and which user should see it. Add a distinct restricted-user case only if the current change or spec defines the restriction.

## Review a developer handoff

- **“Verify the save endpoint returns HTTP 409.”** If the supplied evidence shows that saving through the app displays a conflict message, write the user journey and check that message. If it only shows the HTTP response, list a technical check under Questions for the developer.
- **“Verify the dependency was upgraded.”** If the update affects a known user path, such as opening an in-app document, smoke-test that path. Otherwise ask for the CI or build evidence and generate zero manual cases if there is nothing else in scope.
- **“Check the notification on a locked phone.”** Include the case only when the supported device, build, account and notification setup are available. Ask what QA needs when any prerequisite is missing.

## Bad case

“Test login works correctly” gives the tester no steps and no visible result to check.
