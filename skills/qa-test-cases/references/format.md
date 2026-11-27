# Test case format

Start the Markdown with a title, then **Summary**, **Questions**, **Security notes** (if any), and **Test cases**.

In Summary, record:
- the number of cases;
- **Target for testing**;
- **Evidence level** ("from code only" or "checked in a running build");
- what was read;
- shared setup (test account alias, fixture, env state) that several cases use.

Give each case its own subsection. The heading carries the ID and Title: `### QA-001 — Title`. Do not repeat them as fields in Markdown. List Priority, Platform, Precondition and Test Data as bold one-line fields under the heading. Then give **Steps** and **Expected Result** as bold headings with numbered lists, then Basis and Status as one-line fields. references/example.md shows this layout. CSV keeps ID and Title as columns.

1. **Priority** — see "Priority" below.
2. **Platform** — Web, iOS, Android, Desktop app or Email. Leave blank when the evidence does not say. Put viewport, browser, device or account state in Precondition.
3. **Precondition** — the starting state and any case-specific prerequisite. Refer to shared setup by alias. Define each alias once in Summary, such as "Deployment = the QA deployment that contains this commit". Add a safe reset when the case changes state. Add "Applies when: ..." if the case only holds in one env or config state.
4. **Test Data** — concrete synthetic inputs or fixture aliases.
5. **Steps** — numbered actions using visible labels and realistic navigation.
6. **Expected Result** — numbered observations. Name the triggering step when numbers do not align. For a refusal, name the visible message or state and any side effect that must not happen.
7. **Basis** — Code, Spec or Unclear. Put unsupported claims in Questions.
8. **Status** — Not run.

## Priority

- **High:** a core workflow is blocked, access or data is at risk, or the failure blocks other checks.
- **Medium:** an important workflow is degraded.
- **Low:** copy, layout or other low-impact checks.

Base priority on what happens to the user if the case fails. When two levels fit, choose the higher one. Cap at Medium for a surface that is not a core product workflow, such as a README badge, a preview page or a docs page, unless failure exposes data or blocks other cases.

## Target for testing

State the app version, build number or release tag, plus the environment and surface, when the evidence gives them. If web and mobile use different builds, name the build for each group.

If the build is unknown, say so and give the best reference, labelled by type: commit SHA, branch or PR, spec revision, or environment and route. A commit names the source reviewed. Call it deployed only when the evidence shows that. If QA needs the build mapping, ask for it under Questions.

Examples:
- **Target for testing:** App 1.4.2 (build 96), Android staging.
- **Target for testing:** Build unknown. Source reviewed: `master` at `0b32bf9`; Web route: `/simple`. Questions: Which QA deployment contains this commit?
- **Target for testing:** Build unknown. Requirements: checkout handoff, revision 3. Questions: Which QA build implements this revision?

## Manual E2E scope check

For each proposed case, ask: can QA reach the start, do the action through the product, and see the result with their setup? Credentials appear as fixture aliases, never values.

- **API, database or background job change:** test the visible journey that calls it and the visible result. If the handoff only asks for an endpoint response, logs, a database check or a private flag, list it under Questions as **Technical verification** and ask for an automated check or a user-facing path. Treat direct API testing as a separate technical check only when the requester asks for it and confirms access and tools.
- **Endpoint that returns something a user sees** (an image, a page, a download): opening its URL in a browser is a valid manual case. Say in Precondition how users reach it, such as "embedded in a README". If only the embed route is a real user path, say that under Questions.
- **Dynamic or rendered text:** for values that change (clock time, counts from live data), write the pattern, such as "a time in HH:MM form followed by 'local'". Do not invent a value. For text drawn into an image, quote the string from code. Check which strings the renderer transforms (uppercase, truncation). Add "may display in uppercase" only to those strings, and leave the rest as written. Do not claim exact casing or layout without a build check.
- **Expected value unknown to you** (a version, a count from live data): do not write "ask the developer" inside an Expected Result. Write the pattern in the result, and put the question in Questions. Hold the case until the owner gives the value only if the pattern alone cannot show a pass or fail.
- **Hard-coded text beside shared data** (a header count next to a list, copy that repeats a value from code): if the two could drift apart, list it under Questions as **Drift risk** with the file name. Add a case only when the current build shows a visible mismatch.
- **Version or dependency update:** name the affected user path before choosing a case. Check a version in the UI only when the UI shows one. If only a version string, lockfile or build metadata changed, ask which user path is at risk or what CI covers. Use zero cases if none is supported.
- **Docs, comments or config-example edits:** no manual case. Mention them in Summary only if they change a visible default.
- **Env or config dependent behavior:** do not open secret files. Write one case per state that matters, with "Applies when: ..." in Precondition. Keep the case in the runnable list when QA can check or set that state. Ask under Questions which state the QA environment has. If QA cannot know or set the state, move the case to Questions.
- **Missing access or setup** (unreleased build, admin setup, second device, test inbox, clock control, special account): name the prerequisite and ask the owner. Keep the case out of the runnable list until setup exists. Never guess, and never change production data to make a case runnable.

## Choose coverage

- Start with the affected user goal. Add one likely failure or boundary when it matters. For a limit, test the nearest useful values on each side. Keep exact limits and timing grounded in evidence.
- Add a contrast only when it can change the result: allowed and restricted access, enabled and disabled setting, new and returning state, device or locale.
- Group variants that share steps and results. Split variants with different setup or outcomes. Near-identical variants, such as several badge kinds or pages, get one case each when their data source, env state or expected text differs. Group them in one case only when steps and results are the same except for a name.
- Add a regression case only when the change touches that path. Note known overlap or an excluded scenario under Questions. Do not claim it passed elsewhere.
- Describe timing, retries, external dependencies and cleanup only when relevant. Never ask QA to guess a delay or manipulate internal state.
- For multi-user flows, use aliases (Sender A, Recipient B). Say who acts and who observes.
- A team template may add run or sign-off fields. Keep execution results apart from expected results.

## IDs and CSV

Finalize the order, then number from QA-001. Reuse the same IDs and order in every format. Use a heading like `### QA-001 — Open the portfolio without a splash screen`.

The ID is a reference inside this set only. A destination tool may assign permanent IDs. Never use these IDs as primary keys or reuse an external tool's IDs. Always use the QA prefix. Keep titles and content independent of the ID.

Replace slashes in the branch name with hyphens in filenames. The CSV header is exactly:

```csv
ID,Title,Priority,Platform,Precondition,Test Data,Steps,Expected Result,Basis,Status
```

Put each numbered list in one cell, on one line, like `1. Open the page. 2. Enter the email.` Keep the "After step N" wording and the exact text of every result. Do not add line breaks. Wrap every data cell in double quotes, even short ones, and double any quote inside a cell. A comma in an unquoted cell splits the row and breaks the import. Every row must have exactly 10 cells. Leave the header line exactly as shown above, or quote each header cell the same way; both import correctly.

When a team supplies its own format, use its fields and labels. Keep runnable steps, observable results and the "Not run" status.

## Optional HTML and PDF

Use the same cases, IDs, order, fields and statuses as Markdown. Include Summary and target.

- **HTML:** save `qa-cases-<branch>.html` as a standalone file. Use one heading per case and numbered lists for steps and results. Use embedded styles that wrap at narrow widths. Escape text taken from evidence. No scripts, remote fonts or external files.
- **Themed export:** only when asked. Read the theme of the surface under test and reuse its color, type and layout cues where they keep the page readable. Use local font fallbacks. With no usable theme, use neutral styling.
- **PDF:** print the same HTML to `qa-cases-<branch>.pdf` with a local browser or PDF tool. Use print styles with legible text and margins. Keep each case heading with its first lines. Check that the first and last cases appear. If no PDF tool exists, give the print-ready HTML and say how to save it as PDF from a browser.
