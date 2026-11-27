# Examples

## Good case: behavior from code

Assumptions: the evidence shows the fifth failed attempt locks the account for 15 minutes and shows the message below. The QA environment has an unlocked synthetic account.

### QA-001 — Fifth failed sign-in shows the temporary lockout

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

The quoted message is only valid because the code shows it. Without that evidence, write "a lockout message" and ask the exact text under Questions.

The same case as a CSV row (one line, every cell quoted, steps and results flattened, inner quotes doubled):

```csv
"QA-001","Fifth failed sign-in shows the temporary lockout","High","Web","Use an unlocked test account with no prior failed attempts.","qa.user.1@example.test and an invalid test password.","1. Open the sign-in page. 2. Submit four sign-in attempts with the invalid test password. 3. Submit a fifth sign-in attempt with the same invalid test password.","1. After step 3, the page shows ""Too many attempts. Try again in 15 minutes.""","Code","Not run"
```

## Good case: two users

Assumptions: a shared workspace sends an in-app notification when a member is mentioned. Sender A and Recipient B are fixture aliases defined once in Summary.

### QA-002 — Mentioned member sees the mention notification

- **Priority:** Medium
- **Platform:** Web
- **Precondition:** Sender A and Recipient B belong to the same test workspace. Recipient B is signed in on a second browser profile.
- **Test Data:** A comment that mentions Recipient B by display name.

**Steps**

1. As Sender A, open any project and post the comment.
2. As Recipient B, open the notifications list.

**Expected Result**

1. After step 1, Sender A sees the comment in the thread.
2. After step 2, Recipient B sees one new notification that names Sender A.

- **Basis:** Spec
- **Status:** Not run

If the evidence does not define a restriction (for example, who cannot be mentioned), do not add a restricted-user case. Ask under Questions.

## Good case: depends on config

Assumptions: a status badge shows "Not open to work" when the `BADGE_STATUS` env variable is empty, and shows the variable's text when set. You cannot read the env file.

### QA-003 — Status badge shows the default text

- **Priority:** High
- **Platform:** Web
- **Precondition:** Applies when `BADGE_STATUS` is not set on the tested deployment.
- **Test Data:** None.

**Steps**

1. Open `/api/badge?kind=status`.

**Expected Result**

1. After step 1, the value reads "Not open to work".

- **Basis:** Code
- **Status:** Not run

Add a second case for the set state only if QA can change the variable. Otherwise list it under Questions: "Can QA set `BADGE_STATUS` on a test deployment?"

The badge also shows a clock. Write its expected text as a pattern ("a time in HH:MM form followed by 'local'"), not a fixed time. The code may draw the label in uppercase, so write "may display in uppercase" unless a build check shows the exact casing. Cap Priority at Medium here, since a README badge is not a core workflow.

## Review a developer handoff

- **“Verify the save endpoint returns HTTP 409.”** If the evidence shows that saving in the app displays a conflict message, write the user journey and check that message. If it only shows the HTTP response, list a technical check under Questions for the developer.
- **“Verify the dependency was upgraded.”** If the update affects a known user path, such as opening an in-app document, smoke-test that path. Otherwise ask for CI or build evidence and write zero cases.
- **“Check the notification on a locked phone.”** Include the case only when the device, build, account and notification setup are available. Otherwise name what QA needs under Questions.
- **“Update README and docs.”** No manual case. These do not change what a user sees.

## Bad case

“Test login works correctly” gives the tester no steps and no visible result to check.
