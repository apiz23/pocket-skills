# Test case format

For the default format, start the Markdown with a title, then **Summary**, **Questions**, **Security notes** (if any), and **Test cases**. In Summary, record the number of cases, **Target for testing**, and what was read. Include shared setup only where needed, such as a test account alias or a fixture shared by multiple cases. Flag unavailable prerequisites under Questions. Under Test cases, give each case its own subsection with the following fields in order.

1. ID — temporary reference in this set of cases, starting at QA-001.
2. Title — describe the behavior without relying on the ID.
3. Priority — High for a blocked core workflow, access or data risk, or a failure that blocks the remaining checks. Medium for an important degraded workflow. Low for copy, layout, or other low-impact checks. Base priority on what happens to the user if the case fails.
4. Platform — use the supported surface, such as Web, iOS or Android. Leave blank when the evidence does not identify it. Put a relevant viewport, browser, device or account state in Precondition.
5. Precondition — the starting state and any case-specific prerequisites. Refer to shared setup by alias. If the case changes state, include a safe reset or cleanup when needed.
6. Test Data — concrete synthetic inputs or reusable fixture aliases.
7. Steps — numbered actions using visible labels and realistic navigation.
8. Expected Result — numbered observations. Name the triggering step when the numbers do not align. For a refusal, name the visible message or state and any observable side effect that must not happen.
9. Basis — Code, Spec or Unclear. Put unsupported claims in Questions.
10. Status — Not run.

## Target for testing

State the evidence-backed app version, build number or release tag. Include the target environment and surface when known. If web and mobile use different builds, identify which one applies to each group. This is the intended target for the cases; their execution status stays Not run.

If the app version or build is unknown, say so and use the best available reference: a commit SHA or merge commit, a branch or PR, a named requirement or spec revision, or an environment and route. Label each reference by what it is. A commit identifies the source reviewed; only say it is deployed when the evidence establishes that. If the build mapping is needed to run the cases, ask for it under Questions.

Examples:

- **Target for testing:** App 1.4.2 (build 96), Android staging.
- **Target for testing:** Build unknown. Source reviewed: `master` at `0b32bf9`; Web route: `/simple`. Questions: Which QA deployment contains this commit?
- **Target for testing:** Version unknown. Scope: signed-out sign-in page on staging. Questions: Which build is deployed on staging?
- **Target for testing:** Build unknown. Requirements: checkout handoff, revision 3. Questions: Which QA build implements this revision?

## Manual E2E scope check

For each proposed case, ask whether QA can reach the starting point, perform the action through the supported product, and see the result with their available setup. Use a browser, app, accessible test inbox or device notification when the evidence calls for it. Credentials are represented by fixture aliases, never values.

- **API, database, or background job change:** test the visible journey that calls it and the visible result that changes. If the handoff only asks for an endpoint response, logs, a database check, or a private flag, put it under **Questions** as **Technical verification**. Ask the developer for an automated check or a reproducible user-facing path. If the requester explicitly wants direct API testing and confirms the access and tools, treat that as a separately scoped technical check.
- **Version or dependency update:** name the affected feature or user path before selecting a smoke or regression case. Verify the app version in the UI only when there is an actual user-facing version display or upgrade behavior to check. If the only known change is a version string, lockfile or build metadata, ask which user path is at risk or what CI verifies. Use zero manual cases when none are supported.
- **Missing access or setup:** if testing needs an unreleased build, an admin-only setup, a second device, a test inbox, a clock control or a special account, name the prerequisite and ask the owner to provide it. Keep it out of the runnable list until the required setup is available. Never add a guess or a direct production data change to make the case runnable.

## Choose coverage that helps QA

- Start with affected user goals. Cover the normal path and one likely failure or boundary when they matter. For a limit, select the nearest useful values around it. Keep the exact limit and timing grounded in evidence.
- Exercise a relevant contrast when it could change the result: allowed and restricted access, enabled and disabled settings, new and returning state, or a supported device or locale. Group variants that share steps and results. Split variants with different setup or outcomes. Keep a matrix optional for larger handoffs.
- Add a nearby regression only if the change touches its path. Start a short smoke check first when other cases depend on the feature opening or loading. Note known overlap or an important excluded scenario under Questions instead of claiming it passed elsewhere.
- Describe timing, retries, external dependencies and cleanup only when they are relevant. Keep every included case Not run. Do not ask QA to guess a delay or manipulate internal state.
- Use shared aliases for multi-user workflows (for example, Sender A and Recipient B). Say who acts and who observes the result. An optional team's template can add run or sign-off fields, but keep execution results separate from expected results.

## Temporary IDs

Finalize the case order before numbering. Assign QA-001, QA-002, QA-003 and so on, once each within this set of cases. If cases are reordered while drafting, number them in the final order. When reproducing the same finalized set in another format, keep its assigned IDs and case order. Use a heading such as `### QA-001 — Open the portfolio without a splash screen`.

Prefer the title in reviews and discussions. Decide whether cases overlap by comparing their purpose, steps and expected results. The ID is just a reference within this set. If a team imports the cases, the destination may assign its own permanent IDs and optionally map the temporary ones. Keep the title and content independent of the ID. Generated IDs must never serve as database primary keys or reuse identifiers from external QA systems. Always use the QA prefix, regardless of project.

Use the same cases in Markdown and CSV. Replace slashes in the branch name with hyphens for all filenames. The CSV header is exactly:

```csv
ID,Title,Priority,Platform,Precondition,Test Data,Steps,Expected Result,Basis,Status
```

Put each numbered list in one cell, such as `1. Open the page. 2. Enter the email.` Quote any cell containing a comma or a quote and double any quote inside a quoted cell.

These fields are defaults. When a team supplies a requested format, use its fields and labels while preserving runnable steps, observable results, grounded coverage and a clear unexecuted status. Keep all requested formats aligned on cases, order and temporary references.

## Optional HTML and PDF

Use the same finalized cases, IDs, order, fields and Not run statuses in every format. Include the Summary and target in HTML and PDF. Keep the default CSV schema unchanged; the target stays in the accompanying handoff. For HTML, save `qa-cases-<branch>.html` as a standalone document. Use a clear heading per case, numbered lists for steps and results, and simple styles that wrap at narrow widths. Escape text and attribute values from supplied evidence. Keep styles embedded and omit scripts, remote fonts and other external dependencies.

When the developer requests a project-themed export, read the theme of the surface under test. Reuse its color, typography and layout cues where they suit a readable QA handoff. Use local font fallbacks when needed to keep the file standalone. If the codebase has no usable theme, use simple neutral styling.

If a PDF is requested, print the same HTML to `qa-cases-<branch>.pdf` using an available local browser or PDF tool. Provide print styles for legible text and comfortable margins. Keep case headings with their first lines and allow long cases to flow across pages. Verify that the resulting PDF contains the first and last cases. If no PDF tool is available, provide the print-ready HTML and explain how to save it as PDF from the browser.
