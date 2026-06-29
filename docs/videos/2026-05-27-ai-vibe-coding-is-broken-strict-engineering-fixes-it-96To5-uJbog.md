# AI Vibe Coding Is Broken. Strict Engineering Fixes It.

URL: https://www.youtube.com/watch?v=96To5-uJbog
Channel: [nunomaduro](https://www.youtube.com/@nunomaduro)
Upload date: 2026-05-27
Duration: 18:39
Status: manual-processed
Topics: ai

## Why This Helps Programming
Argues that AI-assisted coding only works well when the project already has strict engineering guardrails. Treat every generated line as your responsibility, and use strong typing, conventions, static analysis, linting, tests, coverage, CI, and explicit AI instructions to push generated code toward production quality.

## Tips And Tricks
- 00:21 - Make types the first AI guardrail. Use PHPStan for PHP and TypeScript for frontend code so generated mistakes are caught across the whole project.
- 01:02 - Run static analysis against real application mistakes. Tools should verify generated code against model properties, imports, and symbols, not just against the file currently open in the editor.
- 02:11 - Apply the same strictness to frontend code. TypeScript should catch bad imports and missing components before AI-generated React or Inertia code reaches review.
- 03:24 - Keep conventions consistent because AI agents copy what they inspect. Typed classes, form requests, actions, clean migrations, and predictable structure give the agent better examples to imitate.
- 04:20 - Use strict PHP defaults everywhere. Strict types and native type declarations give humans, tools, and AI a clearer contract than loose code plus vague comments.
- 05:11 - Standardize Laravel boundaries. Keep validation in form requests, orchestration in controllers or actions, and business behavior in dedicated classes so generated code has obvious places to go.
- 06:23 - Treat the quality pipeline as more than unit tests. Formatting, linting, type coverage, code coverage, static analysis, and tests are the safety net for AI-assisted changes.
- 07:15 - Hide quality tooling behind Composer scripts. Commands like `composer lint` and `composer test` give teammates, CI, and AI agents stable entry points for the same checks.
- 08:18 - Separate local fixing from CI checking. Let local lint commands format or fix code, but make CI verify formatting without mutating files.
- 08:48 - Enforce type coverage. Failing the build for missing types turns typed code from a preference into an automated rule.
- 10:14 - Run tests in parallel and require coverage so strict checks stay practical and AI-generated features include tests, not only implementation.
- 11:54 - Add AI-specific project instructions that tell agents to run the full test command before finishing and to follow the repository's established conventions.

## Source Notes
- Tips are paraphrased or normalized from available YouTube captions/metadata.
- Video media is not stored in this repository.
