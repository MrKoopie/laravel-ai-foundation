from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tools.archive_tools import write_text


@dataclass(frozen=True)
class TopicGuide:
    slug: str
    title: str
    description: str
    rules: list[str]
    tips: list[dict[str, str]]
    examples: list[dict[str, str]]
    source_videos: list[dict[str, str]]
    related: list[str]
    source_articles: list[dict[str, str]] | None = None


def render_topic_guide(guide: TopicGuide) -> str:
    lines = [
        f"# {guide.title}",
        "",
        "## The Short Version",
        guide.description,
        "",
        "## Practical Rules",
    ]

    if guide.rules:
        lines.extend(f"- {rule}" for rule in guide.rules)
    else:
        lines.append("- No practical rules have been curated for this topic yet.")

    lines.extend(["", "## Tips And Tricks"])
    if guide.tips:
        for tip in guide.tips:
            source = tip.get("source", "")
            source_link = f" ([source]({_relative_source_link(source)}))" if source else ""
            lines.extend(
                [
                    f"### {tip['title']}",
                    f"{tip['body']}{source_link}",
                    "",
                ]
            )
    else:
        lines.append("No curated tips have been added for this topic yet.")
        lines.append("")

    lines.append("## Examples")
    if guide.examples:
        for example in guide.examples:
            lines.extend(
                [
                    f"### {example['title']}",
                    example.get("body", ""),
                    "",
                    f"```{example.get('language', '').strip()}".rstrip(),
                    example["code"].rstrip(),
                    "```",
                    "",
                ]
            )
    else:
        lines.append("No examples have been added for this topic yet.")
        lines.append("")

    lines.append("## Source Videos")
    if guide.source_videos:
        for video in guide.source_videos:
            lines.append(f"- [{video['title']}]({_relative_source_link(video['path'])})")
    else:
        lines.append("- No source videos have been linked yet.")

    source_articles = guide.source_articles or []
    if source_articles:
        lines.extend(["", "## Source Articles"])
        for article in source_articles:
            lines.append(f"- [{article['title']}]({_relative_source_link(article['path'])})")

    if guide.related:
        lines.extend(["", "## Related Topics"])
        lines.extend(f"- [{related_title(slug)}]({slug}.md)" for slug in guide.related)

    lines.append("")
    return "\n".join(lines)


def render_topic_landing(guides: list[TopicGuide]) -> str:
    lines = [
        "# Topic Guides",
        "",
        "Start here when searching by programming problem. These pages synthesize tips across multiple videos and link back to the source notes.",
        "",
    ]

    for guide in sorted(guides, key=lambda item: item.title.lower()):
        lines.append(f"- [{guide.title}](../topics/{guide.slug}.md) - {guide.description}")

    lines.extend(
        [
            "",
            "## Source Indexes",
            "- [Video topic map](video-topics.md)",
            "- [Blog source index](blog-sources.md)",
            "",
        ]
    )

    return "\n".join(lines)


def render_examples_index(guides: list[TopicGuide]) -> str:
    lines = [
        "# Examples",
        "",
        "Concrete snippets and configurations distilled from the topic guides.",
        "",
    ]

    for guide in sorted(guides, key=lambda item: item.title.lower()):
        if not guide.examples:
            continue
        lines.extend([f"## {guide.title}", ""])
        for example in guide.examples:
            lines.extend(
                [
                    f"### {example['title']}",
                    example.get("body", ""),
                    "",
                    f"```{example.get('language', '').strip()}".rstrip(),
                    example["code"].rstrip(),
                    "```",
                    "",
                ]
            )

    return "\n".join(lines)


def write_topic_guides(repo: Path, guides: list[TopicGuide] | None = None) -> None:
    guide_set = guides if guides is not None else TOPIC_GUIDES
    for guide in guide_set:
        write_text(repo / "docs/topics" / f"{guide.slug}.md", render_topic_guide(guide))
    write_text(repo / "docs/indexes/topics.md", render_topic_landing(guide_set))
    write_text(repo / "docs/examples/index.md", render_examples_index(guide_set))


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").title()


def related_title(slug: str) -> str:
    for guide in TOPIC_GUIDES:
        if guide.slug == slug:
            return guide.title
    return slug_to_title(slug)


def _relative_source_link(path: str) -> str:
    if path.startswith("docs/videos/"):
        return "../videos/" + Path(path).name
    if path.startswith("docs/articles/"):
        parts = Path(path).parts
        return "../articles/" + "/".join(parts[2:])
    return path


TOPIC_GUIDES = [
    TopicGuide(
        slug="ai-engineering",
        title="AI Engineering Guardrails",
        description="Use strict project defaults so AI-generated code is easier to review, test, and trust.",
        rules=[
            "Treat generated code as your responsibility, not as an external artifact.",
            "Give agents stable commands for linting, testing, static analysis, and coverage.",
            "Make conventions obvious in the codebase because agents copy nearby patterns.",
            "Prefer automated checks over prose instructions when a rule can be enforced.",
        ],
        tips=[
            {
                "title": "Use types as the first guardrail",
                "body": "Run PHPStan for PHP and TypeScript for frontend code so generated mistakes are caught across the project.",
                "source": "docs/videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md",
            },
            {
                "title": "Hide checks behind stable commands",
                "body": "Expose commands such as `composer lint` and `composer test` so humans, agents, and CI all run the same quality pipeline.",
                "source": "docs/videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md",
            },
            {
                "title": "Write repo-level AI instructions",
                "body": "Tell agents which commands to run, which conventions to follow, and when work is not complete yet.",
                "source": "docs/videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md",
            },
        ],
        examples=[
            {
                "title": "Composer quality gate",
                "body": "Use one command for CI and agents. Keep mutation-free checks separate from local fixers.",
                "language": "json",
                "code": '{\n  "scripts": {\n    "lint": "pint && rector --dry-run && phpstan analyse",\n    "test": "pest --parallel --coverage --min=80",\n    "ci": "composer lint && composer test"\n  }\n}',
            },
            {
                "title": "Agent instruction snippet",
                "body": "Keep instructions short, enforceable, and tied to actual commands.",
                "language": "md",
                "code": "Before finishing:\n- Run `composer ci`.\n- Do not mark work complete while tests, static analysis, or formatting fail.\n- Follow existing Laravel action, form request, and typed model patterns.",
            },
        ],
        source_videos=[
            {
                "title": "AI Vibe Coding Is Broken. Strict Engineering Fixes It.",
                "path": "docs/videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md",
            },
            {
                "title": "How I Code With AI Right Now",
                "path": "docs/videos/2026-05-31-how-i-code-with-ai-right-now-heAVDeRZiUA.md",
            },
            {
                "title": "AI Vibe Coding Just Got 10x Better (With Rules Files)",
                "path": "docs/videos/2025-03-24-ai-vibe-coding-just-got-10x-better-with-rules-files-Hi6zlum3K2k.md",
            },
        ],
        related=["testing", "phpstan-type-safety", "tooling"],
    ),
    TopicGuide(
        slug="laravel-actions",
        title="Laravel Actions",
        description="Move reusable application behavior into action classes so controllers, jobs, commands, and other actions can share it.",
        rules=[
            "Keep HTTP concerns out of action classes.",
            "Validate at the boundary, then pass plain data or DTOs into the action. The reason is that validation is a boundary concern: HTTP requests, queued jobs, console commands, and tests all enter the application differently, while the action should receive trusted, already-shaped input.",
            "Wrap multi-step mutations in transactions when partial success would corrupt state.",
            "Do not create an action just to wrap a single obvious Eloquent call.",
            "Keep simple one-off HTTP-only behavior in the controller until a use-case name, reuse pressure, or business invariant appears.",
            "Use actions for behavior that needs a name, has more than one entry point, coordinates multiple collaborators, or protects a business rule.",
        ],
        tips=[
            {
                "title": "Keep controllers thin",
                "body": "Controllers should translate HTTP into application calls; actions should hold the behavior.",
                "source": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
            {
                "title": "Pass validated data",
                "body": "Call `validated()` on a form request and pass that result into the action instead of passing the request object. This keeps malformed user input, redirect behavior, authorization messages, and other HTTP-only concerns at the edge of the system. The action can then focus on the business operation and can be reused from non-HTTP entry points without pretending a request exists.",
                "source": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
            {
                "title": "Reuse behavior across entry points",
                "body": "The same action can be called from a controller, console command, queued job, or another action.",
                "source": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
            {
                "title": "Do not action all the things",
                "body": "An action is useful when behavior has a clear use-case name, more than one entry point, multiple collaborators, a transaction boundary, or a business rule worth testing. A one-line create/update that is only used by one controller can stay inline until the code shows pressure.",
                "source": "docs/articles/stitcher-io/2023-06-02-dont-be-clever.md",
            },
            {
                "title": "Avoid Action per model method",
                "body": "Do not create `CreateUserAction`, `UpdateUserAction`, `DeleteUserAction`, and `FindUserAction` simply because a `User` model exists. That hides ordinary CRUD behind ceremony and teaches agents to route every change through an action. Name actions after real application behavior, such as `InviteTeamMember` or `PublishPost`.",
                "source": "docs/articles/stitcher-io/2025-10-22-reducing-code-motion.md",
            },
        ],
        examples=[
            {
                "title": "Inline simple CRUD",
                "body": "A single validated write with no reuse and no extra business rule can stay in the controller. This is less ceremony, not less architecture.",
                "language": "php",
                "code": "<?php\n\nfinal class StoreTagController\n{\n    public function __invoke(StoreTagRequest $request): RedirectResponse\n    {\n        $tag = Tag::query()->create($request->validated());\n\n        return redirect()->route('tags.show', $tag);\n    }\n}",
            },
            {
                "title": "Action class boundary",
                "body": "The action receives application data, not an HTTP request.",
                "language": "php",
                "code": "<?php\n\ndeclare(strict_types=1);\n\nfinal readonly class CreateUser\n{\n    public function handle(array $data): User\n    {\n        return DB::transaction(fn () => User::query()->create($data));\n    }\n}",
            },
            {
                "title": "Controller calls an action",
                "body": "The controller owns HTTP concerns; the action owns behavior.",
                "language": "php",
                "code": "<?php\n\nfinal class StoreUserController\n{\n    public function __invoke(StoreUserRequest $request, CreateUser $createUser): RedirectResponse\n    {\n        $user = $createUser->handle($request->validated());\n\n        return redirect()->route('users.show', $user);\n    }\n}",
            },
            {
                "title": "Job reuses the same action",
                "body": "Because validation stayed outside the action, a queued job can call it with data that came from another trusted source.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class ImportUserJob\n{\n    public function __construct(private array $row) {}\n\n    public function handle(CreateUser $createUser): void\n    {\n        $createUser->handle([\n            'name' => $this->row['name'],\n            'email' => $this->row['email'],\n        ]);\n    }\n}",
            },
            {
                "title": "Action-worthy workflow",
                "body": "Create an action when the behavior coordinates several steps or protects a rule that deserves a named test surface.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class InviteTeamMember\n{\n    public function __construct(private Mailer $mailer) {}\n\n    public function handle(Team $team, User $invitedBy, string $email): Invitation\n    {\n        return DB::transaction(function () use ($team, $invitedBy, $email) {\n            $invitation = $team->invitations()->create([\n                'email' => $email,\n                'invited_by_id' => $invitedBy->id,\n            ]);\n\n            $this->mailer->send(new TeamInvitationMail($invitation));\n\n            return $invitation;\n        });\n    }\n}",
            },
        ],
        source_videos=[
            {
                "title": "The Action Pattern Is Key to Clean Code",
                "path": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
            {
                "title": "Laravel Actions: The Secret Sauce",
                "path": "docs/videos/2024-12-02-laravel-actions-the-secret-sauce-r1480BoFulQ.md",
            },
            {
                "title": "Clean Laravel Controllers with Actions and Form Requests",
                "path": "docs/videos/2025-01-29-clean-laravel-controllers-with-actions-and-form-requests-nLNdQ9q_RxA.md",
            },
        ],
        related=["avoid-overengineering", "clean-code", "database-integrity", "phpstan-type-safety"],
        source_articles=[
            {
                "title": "Don't be clever",
                "path": "docs/articles/stitcher-io/2023-06-02-dont-be-clever.md",
            },
            {
                "title": "Reducing code motion",
                "path": "docs/articles/stitcher-io/2025-10-22-reducing-code-motion.md",
            },
        ],
    ),
    TopicGuide(
        slug="avoid-overengineering",
        title="Avoid Overengineering",
        description="Add structure only when it makes Laravel and PHP code easier to change, test, reuse, or reason about.",
        rules=[
            "Start with direct Laravel code when behavior is simple, local, and obvious.",
            "Wait for pressure before adding patterns: repeated behavior, multiple entry points, hidden business rules, or coordination across collaborators.",
            "Add an action only when the behavior has earned a name, not because every controller line needs a class.",
            "Use DDD terms only when they clarify business language the team actually uses.",
            "Prefer deleting unnecessary states, flags, and indirection before adding more coordination code.",
        ],
        tips=[
            {
                "title": "Wait for pressure before adding patterns",
                "body": "A pattern should pay rent. If a small exception needs flags, hooks, base classes, or override methods, the abstraction may be more expensive than the duplication it removed.",
                "source": "docs/articles/stitcher-io/2023-06-02-dont-be-clever.md",
            },
            {
                "title": "Use actions after the use case appears",
                "body": "Actions are not the default destination for code. Add one when a behavior has a real use-case name, needs reuse outside HTTP, coordinates multiple collaborators, or owns a transaction boundary.",
                "source": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
            {
                "title": "Keep persistence boring until it hurts",
                "body": "Do not add repositories, query buses, or data mappers around ordinary Eloquent calls unless persistence complexity is already making callers harder to test or change.",
                "source": "docs/articles/stitcher-io/2025-10-22-reducing-code-motion.md",
            },
            {
                "title": "Do not let DDD become decoration",
                "body": "Value objects, aggregates, events, and policies help when they express domain language or protect invariants. They are noise when they only rename framework operations.",
                "source": "docs/articles/stitcher-io/2019-06-07-tests-and-types.md",
            },
        ],
        examples=[
            {
                "title": "What not to add",
                "body": "For a one-screen admin form, skip an action, DTO hierarchy, repository, command bus, event stream, and module boundary unless the behavior shows real pressure for them.",
                "language": "text",
                "code": "Use the smallest design that explains the current behavior:\n- FormRequest for HTTP validation\n- Controller for HTTP orchestration\n- Eloquent model call for the single write\n- Focused test for the user-visible result",
            },
            {
                "title": "Small controller before abstraction",
                "body": "This code has no reuse pressure, no multi-step consistency boundary, and no hidden domain rule. Keeping it direct makes the behavior easier to scan.",
                "language": "php",
                "code": "<?php\n\nfinal class StoreLabelController\n{\n    public function __invoke(StoreLabelRequest $request): RedirectResponse\n    {\n        $label = Label::query()->create($request->validated());\n\n        return redirect()->route('labels.show', $label);\n    }\n}",
            },
            {
                "title": "Extraction when pressure appears",
                "body": "Once the same behavior is needed from HTTP and a queued import, and it has a consistency rule, the action earns its place.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class RegisterSubscriber\n{\n    public function handle(SubscriberData $data): Subscriber\n    {\n        return DB::transaction(function () use ($data) {\n            $subscriber = Subscriber::query()->create($data->toArray());\n\n            SubscribeToDefaultList::dispatchSync($subscriber);\n\n            return $subscriber;\n        });\n    }\n}",
            },
        ],
        source_videos=[
            {
                "title": "The Action Pattern Is Key to Clean Code",
                "path": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
            {
                "title": "Clean Laravel Controllers with Actions and Form Requests",
                "path": "docs/videos/2025-01-29-clean-laravel-controllers-with-actions-and-form-requests-nLNdQ9q_RxA.md",
            },
        ],
        related=["laravel-actions", "domain-modeling", "event-sourcing", "dependencies-and-maintenance"],
        source_articles=[
            {
                "title": "Don't be clever",
                "path": "docs/articles/stitcher-io/2023-06-02-dont-be-clever.md",
            },
            {
                "title": "Reducing code motion",
                "path": "docs/articles/stitcher-io/2025-10-22-reducing-code-motion.md",
            },
            {
                "title": "Strategies",
                "path": "docs/articles/stitcher-io/2022-04-06-strategies.md",
            },
            {
                "title": "What event sourcing is not about",
                "path": "docs/articles/stitcher-io/2021-04-09-what-event-sourcing-is-not-about.md",
            },
        ],
    ),
    TopicGuide(
        slug="phpstan-type-safety",
        title="PHPStan And Type Safety",
        description="Use static analysis and native types to catch defects before runtime and to give AI tools a stricter contract.",
        rules=[
            "Prefer native type declarations where PHP supports them.",
            "Use PHPStan or Larastan to check model properties, request data, and return types.",
            "Raise strictness gradually, but make the configured level non-negotiable in CI.",
            "Use type coverage to prevent new untyped code from quietly entering the codebase.",
        ],
        tips=[
            {
                "title": "Catch property mistakes before runtime",
                "body": "Static analysis can detect access to model properties or array keys that do not exist.",
                "source": "docs/videos/2025-03-25-phpstan-loves-this-trick-strongly-typed-requests-E9ixq-dlcjQ.md",
            },
            {
                "title": "Make typed requests visible to tools",
                "body": "Strongly typed form request data makes downstream code easier for PHPStan, humans, and agents to understand.",
                "source": "docs/videos/2025-03-25-phpstan-loves-this-trick-strongly-typed-requests-E9ixq-dlcjQ.md",
            },
            {
                "title": "Treat PHPStan like TypeScript for PHP",
                "body": "Use static analysis as a daily feedback loop, not as an occasional cleanup task.",
                "source": "docs/videos/2025-01-14-phpstan-is-typescript-for-php-sOQC_-pkMYk.md",
            },
        ],
        examples=[
            {
                "title": "Typed form request shape",
                "body": "Expose a typed method so callers do not pass unknown arrays around the app.",
                "language": "php",
                "code": "<?php\n\nfinal class StoreUserRequest extends FormRequest\n{\n    /** @return array{name: string, email: string} */\n    public function validatedData(): array\n    {\n        return $this->validated();\n    }\n}",
            },
            {
                "title": "PHPStan command",
                "body": "Keep analysis easy to run locally and in CI.",
                "language": "bash",
                "code": "vendor/bin/phpstan analyse --memory-limit=1G",
            },
        ],
        source_videos=[
            {
                "title": "AI Vibe Coding Is Broken. Strict Engineering Fixes It.",
                "path": "docs/videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md",
            },
            {
                "title": "PHPStan is TypeScript for PHP!",
                "path": "docs/videos/2025-01-14-phpstan-is-typescript-for-php-sOQC_-pkMYk.md",
            },
            {
                "title": "Modern PHP Type Safety with PHPStan..",
                "path": "docs/videos/2025-10-28-modern-php-type-safety-with-phpstan-rSMi1vJ942o.md",
            },
        ],
        related=["ai-engineering", "clean-code", "testing"],
        source_articles=[
            {
                "title": "Tests and types",
                "path": "docs/articles/stitcher-io/2019-06-07-tests-and-types.md",
            },
            {
                "title": "Uncertainty, doubt, and static analysis",
                "path": "docs/articles/stitcher-io/2022-07-16-uncertainty-doubt-and-static-analysis.md",
            },
            {
                "title": "What about typed request classes?",
                "path": "docs/articles/stitcher-io/2021-06-29-what-about-request-classes.md",
            },
        ],
    ),
    TopicGuide(
        slug="testing",
        title="Testing Strategy",
        description="Use fast, focused tests plus coverage and quality gates so code changes are safe to accept.",
        rules=[
            "Start with smoke tests for broad confidence, then add focused tests for risky behavior.",
            "Prefer arrange-act-assert structure so test intent is obvious.",
            "Avoid mocks when a real collaborator gives better confidence at acceptable cost.",
            "Run tests in parallel when suite time would discourage frequent checks.",
        ],
        tips=[
            {
                "title": "Make the first test a smoke test",
                "body": "A smoke test proves the critical path still works before you spend time on smaller cases.",
                "source": "docs/videos/2025-01-06-why-smoke-tests-should-always-be-your-first-test-6iz1uPS-s3A.md",
            },
            {
                "title": "Keep test shape readable",
                "body": "Arrange-act-assert keeps setup, behavior, and expectations separate.",
                "source": "docs/videos/2024-12-03-clean-tests-with-arrange-act-assert-bBZ44BeDVTg.md",
            },
            {
                "title": "Use coverage as a guardrail",
                "body": "Coverage thresholds are most useful when they prevent AI-generated code from shipping without tests.",
                "source": "docs/videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md",
            },
        ],
        examples=[
            {
                "title": "Arrange-act-assert test",
                "body": "Make the test read as a tiny story.",
                "language": "php",
                "code": "<?php\n\nit('creates a user from valid input', function () {\n    $data = User::factory()->raw();\n\n    $user = app(CreateUser::class)->handle($data);\n\n    expect($user)->email->toBe($data['email']);\n});",
            },
            {
                "title": "Parallel coverage gate",
                "body": "Fast checks are easier to run often.",
                "language": "bash",
                "code": "vendor/bin/pest --parallel --coverage --min=80",
            },
        ],
        source_videos=[
            {
                "title": "Your PHP Tests Are Not Enough in 2026",
                "path": "docs/videos/2026-05-26-your-php-tests-are-not-enough-in-2026-WhXf_mM5k7c.md",
            },
            {
                "title": "3 testing tips you need to know...",
                "path": "docs/videos/2024-12-19-3-testing-tips-you-need-to-know-shgXQUkCixw.md",
            },
            {
                "title": "Why Smoke Tests Should Always Be Your First Test",
                "path": "docs/videos/2025-01-06-why-smoke-tests-should-always-be-your-first-test-6iz1uPS-s3A.md",
            },
        ],
        related=["ai-engineering", "phpstan-type-safety", "tooling"],
        source_articles=[
            {
                "title": "Testing Patterns",
                "path": "docs/articles/stitcher-io/2024-03-22-testing-patterns.md",
            },
            {
                "title": "Tests and types",
                "path": "docs/articles/stitcher-io/2019-06-07-tests-and-types.md",
            },
        ],
    ),
    TopicGuide(
        slug="database-integrity",
        title="Database Integrity",
        description="Protect application state with explicit constraints, transactions, and schema changes that match production behavior.",
        rules=[
            "Use database constraints for invariants the application must never violate.",
            "Wrap multi-step writes in transactions when partial success would be wrong.",
            "Prefer migrations over production seeders for production data changes.",
            "Be cautious with cascade deletes and defaults because they can hide destructive behavior.",
        ],
        tips=[
            {
                "title": "Use composite unique constraints",
                "body": "Let the database enforce uniqueness when an invariant depends on multiple columns.",
                "source": "docs/videos/2025-01-21-keep-your-db-in-check-with-composite-unique-constraints-yT4euHDveVc.md",
            },
            {
                "title": "Avoid partial writes",
                "body": "Use transactions around workflows that update multiple records or call external services.",
                "source": "docs/videos/2025-01-28-avoid-this-mistake-in-your-laravel-db-transactions-N0jlh912xcM.md",
            },
            {
                "title": "Do production data changes with migrations",
                "body": "Migrations make production data changes reviewable, ordered, and repeatable.",
                "source": "docs/videos/2025-02-28-using-laravel-seeders-in-production-stop-use-migrations-instead-HNgDhZYg3VI.md",
            },
        ],
        examples=[
            {
                "title": "Composite unique constraint",
                "body": "Enforce the invariant where concurrent requests cannot bypass it.",
                "language": "php",
                "code": "<?php\n\nSchema::table('team_user', function (Blueprint $table) {\n    $table->unique(['team_id', 'user_id']);\n});",
            },
            {
                "title": "Transactional workflow",
                "body": "Roll back the whole mutation if any step fails.",
                "language": "php",
                "code": "<?php\n\nDB::transaction(function () use ($data) {\n    $order = Order::query()->create($data);\n    ReserveInventory::dispatchSync($order);\n});",
            },
        ],
        source_videos=[
            {
                "title": "AVOID This Mistake in Your Laravel DB Transactions",
                "path": "docs/videos/2025-01-28-avoid-this-mistake-in-your-laravel-db-transactions-N0jlh912xcM.md",
            },
            {
                "title": "Keep Your DB in Check with Composite Unique Constraints!",
                "path": "docs/videos/2025-01-21-keep-your-db-in-check-with-composite-unique-constraints-yT4euHDveVc.md",
            },
            {
                "title": "Using Laravel Seeders in Production? STOP! Use Migrations Instead!",
                "path": "docs/videos/2025-02-28-using-laravel-seeders-in-production-stop-use-migrations-instead-HNgDhZYg3VI.md",
            },
        ],
        related=["laravel-actions", "testing"],
        source_articles=[
            {
                "title": "Unsafe SQL functions in Laravel",
                "path": "docs/articles/stitcher-io/2019-04-10-unsafe-sql-functions-in-laravel.md",
            },
        ],
    ),
    TopicGuide(
        slug="clean-code",
        title="Clean Laravel Code",
        description="Keep code readable by giving each layer one job: requests validate, controllers orchestrate, actions perform behavior, and tests describe outcomes.",
        rules=[
            "Use strict equality and strict types when possible.",
            "Move validation to form requests.",
            "Move reusable behavior to actions or dedicated classes.",
            "Use DTOs when they clarify boundaries; avoid them when arrays are simpler and well typed.",
        ],
        tips=[
            {
                "title": "Do not let controllers become workflows",
                "body": "Controllers should be thin enough that the application behavior has a reusable name elsewhere.",
                "source": "docs/videos/2025-12-26-laravel-clean-code-invokable-controllers-form-requests-jobs-and-more-ZdzdOcdRowk.md",
            },
            {
                "title": "Use form requests for validation",
                "body": "A form request gives validation a home and keeps controller methods from turning into input parsing code.",
                "source": "docs/videos/2025-03-20-laravel-clean-code-how-to-write-perfect-form-requests-FfDu-XR-8YQ.md",
            },
            {
                "title": "Prefer strict comparisons",
                "body": "Strict equality avoids PHP coercion surprises and makes intent easier to inspect.",
                "source": "docs/videos/2025-02-05-always-use-strict-equality-hcI06mTlbzM.md",
            },
        ],
        examples=[
            {
                "title": "Thin invokable controller",
                "body": "One HTTP endpoint, one orchestration path.",
                "language": "php",
                "code": "<?php\n\nfinal class PublishPostController\n{\n    public function __invoke(PublishPostRequest $request, PublishPost $publish): RedirectResponse\n    {\n        $publish->handle($request->validated());\n\n        return back();\n    }\n}",
            },
        ],
        source_videos=[
            {
                "title": "Laravel Clean Code: Invokable Controllers, Form Requests, Jobs, and More",
                "path": "docs/videos/2025-12-26-laravel-clean-code-invokable-controllers-form-requests-jobs-and-more-ZdzdOcdRowk.md",
            },
            {
                "title": "Laravel Clean Code: How to Write Perfect Form Requests!",
                "path": "docs/videos/2025-03-20-laravel-clean-code-how-to-write-perfect-form-requests-FfDu-XR-8YQ.md",
            },
            {
                "title": "Always use STRICT EQUALITY",
                "path": "docs/videos/2025-02-05-always-use-strict-equality-hcI06mTlbzM.md",
            },
        ],
        related=["laravel-actions", "phpstan-type-safety", "testing"],
        source_articles=[
            {
                "title": "Don't be clever",
                "path": "docs/articles/stitcher-io/2023-06-02-dont-be-clever.md",
            },
            {
                "title": "Reducing code motion",
                "path": "docs/articles/stitcher-io/2025-10-22-reducing-code-motion.md",
            },
            {
                "title": "Laravel view models vs. view composers",
                "path": "docs/articles/stitcher-io/2018-10-16-laravel-view-models-vs-view-composers.md",
            },
        ],
    ),
    TopicGuide(
        slug="request-data-boundaries",
        title="Request Data Boundaries",
        description="Validate raw input at the edge, then pass typed, trusted data into application behavior.",
        rules=[
            "Treat HTTP request objects as boundary objects, not application-service input.",
            "Convert validated request data into a DTO, typed accessor, or value object before calling reusable actions.",
            "Let types express required fields, nullability, enums, and simple scalar expectations where practical.",
            "Keep custom validation for rules the type system cannot express.",
        ],
        tips=[
            {
                "title": "Make application input visible to tools",
                "body": "Validated arrays are easy for Laravel, but weak for static analysis. A typed request method or DTO tells IDEs, PHPStan, tests, and reviewers what the action receives.",
                "source": "docs/articles/stitcher-io/2021-06-29-what-about-request-classes.md",
            },
            {
                "title": "Design around the object the use case needs",
                "body": "The rest of the application usually wants a typed object, not an HTTP request. Build the boundary so the controller maps raw input into that object early.",
                "source": "docs/articles/stitcher-io/2025-03-17-request-objects-in-tempest.md",
            },
            {
                "title": "Keep validation outside reusable actions",
                "body": "Validation belongs at the entry boundary because web requests, jobs, CLI commands, imports, and tests all enter the application differently. The action should receive already-shaped data and enforce behavior-specific invariants.",
                "source": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
        ],
        examples=[
            {
                "title": "Typed request data before the action",
                "body": "The request owns HTTP validation; the action receives application data.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class StorePostData\n{\n    public function __construct(\n        public string $title,\n        public PostStatus $status,\n        public string $body,\n    ) {}\n}\n\nfinal class StorePostRequest extends FormRequest\n{\n    public function data(): StorePostData\n    {\n        $validated = $this->validated();\n\n        return new StorePostData(\n            title: $validated['title'],\n            status: PostStatus::from($validated['status']),\n            body: $validated['body'],\n        );\n    }\n}\n\nfinal class StorePostController\n{\n    public function __invoke(StorePostRequest $request, StorePost $storePost): RedirectResponse\n    {\n        $post = $storePost->handle($request->data());\n\n        return redirect()->route('posts.show', $post);\n    }\n}\n",
            },
        ],
        source_videos=[
            {
                "title": "The Action Pattern Is Key to Clean Code",
                "path": "docs/videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md",
            },
        ],
        related=["laravel-actions", "phpstan-type-safety", "domain-modeling"],
        source_articles=[
            {
                "title": "What about typed request classes?",
                "path": "docs/articles/stitcher-io/2021-06-29-what-about-request-classes.md",
            },
            {
                "title": "Request objects in Tempest",
                "path": "docs/articles/stitcher-io/2025-03-17-request-objects-in-tempest.md",
            },
        ],
    ),
    TopicGuide(
        slug="domain-modeling",
        title="Domain Modeling In PHP",
        description="Use types, enums, value objects, and clear object relationships to make business rules explicit.",
        rules=[
            "Promote primitives to value objects when a business constraint is reused or easy to violate.",
            "Use enums for named states; add backing values only for persistence or serialization.",
            "Use inheritance for true specialization and interfaces for acts-as capabilities.",
            "Avoid clever abstractions before the real business variation is visible.",
        ],
        tips=[
            {
                "title": "Let domain types narrow invalid input",
                "body": "A primitive such as `int` or `string` usually permits values the business does not. Small value objects make those invalid states unrepresentable after construction.",
                "source": "docs/articles/stitcher-io/2019-06-07-tests-and-types.md",
            },
            {
                "title": "Keep enum values technical",
                "body": "Enum backing values should be stable persistence or serialization contracts. Labels belong in translation, presentation, or enum methods.",
                "source": "docs/articles/stitcher-io/2022-05-30-php-enum-style-guide.md",
            },
            {
                "title": "Distinguish is-a from acts-as",
                "body": "Inheritance should describe true domain specialization. Interfaces are better for technical roles such as billable, searchable, exportable, or publishable.",
                "source": "docs/articles/stitcher-io/2024-08-21-extends-vs-implements.md",
            },
        ],
        examples=[
            {
                "title": "Value object plus enum",
                "body": "Types carry business language across actions, jobs, tests, and models.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class Percentage\n{\n    public function __construct(public int $value)\n    {\n        if ($value < 0 || $value > 100) {\n            throw new InvalidArgumentException('Percentage must be between 0 and 100.');\n        }\n    }\n}\n\nenum DiscountType: string\n{\n    case FIXED = 'fixed';\n    case PERCENTAGE = 'percentage';\n\n    public function requiresPercentage(): bool\n    {\n        return $this === self::PERCENTAGE;\n    }\n}\n",
            },
        ],
        source_videos=[
            {
                "title": "Why use DTOs? Data Transfer Objects",
                "path": "docs/videos/2025-04-02-why-use-dtos-data-transfer-objects-c6CP1C8liyU.md",
            },
        ],
        related=["request-data-boundaries", "phpstan-type-safety", "clean-code"],
        source_articles=[
            {
                "title": "Tests and types",
                "path": "docs/articles/stitcher-io/2019-06-07-tests-and-types.md",
            },
            {
                "title": "My PHP enum style guide",
                "path": "docs/articles/stitcher-io/2022-05-30-php-enum-style-guide.md",
            },
            {
                "title": "Extend or implement",
                "path": "docs/articles/stitcher-io/2024-08-21-extends-vs-implements.md",
            },
            {
                "title": "Don't be clever",
                "path": "docs/articles/stitcher-io/2023-06-02-dont-be-clever.md",
            },
        ],
    ),
    TopicGuide(
        slug="event-sourcing",
        title="Event Sourcing",
        description="Use event streams when history, auditability, temporal reporting, or process reconstruction is central to the domain.",
        rules=[
            "Do not event-source every table by default.",
            "Name events as facts that already happened.",
            "Keep projections rebuildable and free of irreversible business writes.",
            "Use ordinary stateful models for parts of the system that do not benefit from history.",
        ],
        tips=[
            {
                "title": "Choose event sourcing by domain need, not application size",
                "body": "The question is whether the workflow needs historical facts and replayable state, not whether the project is large enough to justify a pattern.",
                "source": "docs/articles/stitcher-io/2021-04-09-what-event-sourcing-is-not-about.md",
            },
            {
                "title": "Mix event-sourced and stateful models deliberately",
                "body": "Admin CRUD, lookup tables, and simple configuration often work better as normal state. Money movement, order flows, and audit-heavy domains may justify event streams.",
                "source": "docs/articles/stitcher-io/2020-04-14-combining-event-sourcing-and-stateful-systems.md",
            },
            {
                "title": "Use event queries before permanent projections when reads are occasional",
                "body": "A projection has maintenance cost. If a read is infrequent, querying the stream directly can be simpler until usage proves otherwise.",
                "source": "docs/articles/stitcher-io/2021-06-15-a-new-major-version-of-laravel-event-sourcing.md",
            },
        ],
        examples=[
            {
                "title": "Fact event and projection",
                "body": "The event records what happened; the projection answers a read question.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class OrderWasPaid\n{\n    public function __construct(\n        public string $orderId,\n        public Money $amount,\n        public DateTimeImmutable $paidAt,\n    ) {}\n}\n\nfinal class OrdersToShipProjector\n{\n    public function onOrderWasPaid(OrderWasPaid $event): void\n    {\n        OrdersToShip::query()->create([\n            'order_id' => $event->orderId,\n            'paid_at' => $event->paidAt,\n        ]);\n    }\n}\n",
            },
        ],
        source_videos=[
            {
                "title": "Event Sourcing in Laravel Step by Step",
                "path": "docs/videos/2024-12-14-event-sourcing-in-laravel-step-by-step-hW9pWY4bx-A.md",
            },
        ],
        related=["database-integrity", "domain-modeling", "testing"],
        source_articles=[
            {
                "title": "Starting with event sourcing",
                "path": "docs/articles/stitcher-io/2021-04-09-what-event-sourcing-is-not-about.md",
            },
            {
                "title": "Combining event sourcing and stateful systems",
                "path": "docs/articles/stitcher-io/2020-04-14-combining-event-sourcing-and-stateful-systems.md",
            },
            {
                "title": "A new major version of Laravel Event Sourcing",
                "path": "docs/articles/stitcher-io/2021-06-15-a-new-major-version-of-laravel-event-sourcing.md",
            },
        ],
    ),
    TopicGuide(
        slug="dependencies-and-maintenance",
        title="Dependencies And Maintenance",
        description="Keep collaborators, packages, and upgrade work explicit so the codebase stays understandable and safe to evolve.",
        rules=[
            "Inject collaborators instead of locating them from the container inside domain or action code.",
            "Audit why packages are installed and remove unused dependencies.",
            "Treat deprecations as early upgrade work, not as ignorable noise.",
            "Contribute upstream fixes before forking dependencies.",
        ],
        tips=[
            {
                "title": "Avoid service location in application code",
                "body": "Resolving dependencies from the container inside a class hides what the class needs. Constructor injection makes dependencies visible to tests, reviewers, and static analysis.",
                "source": "docs/articles/stitcher-io/2019-07-30-things-dependency-injection-is-not-about.md",
            },
            {
                "title": "Use package hygiene commands regularly",
                "body": "`composer why`, `composer audit`, and `composer outdated --direct` help you understand the code you trust and whether it is still needed.",
                "source": "docs/articles/stitcher-io/2026-04-03-dependency-hygiene.md",
            },
            {
                "title": "Turn deprecations into a rolling backlog",
                "body": "Deprecations are future failures with a grace period. Fix them in small batches while the application still runs.",
                "source": "docs/articles/stitcher-io/2022-05-18-dealing-with-deprecations.md",
            },
        ],
        examples=[
            {
                "title": "Dependency maintenance script",
                "body": "Give teams and agents a boring way to inspect package health.",
                "language": "json",
                "code": "{\n  \"scripts\": {\n    \"deps:audit\": \"composer audit && composer outdated --direct\",\n    \"deps:why\": \"composer why\"\n  }\n}\n",
            },
        ],
        source_videos=[
            {
                "title": "Important Composer Security Update",
                "path": "docs/videos/2026-05-30-important-composer-security-update-vebiqijeswQ.md",
            },
        ],
        related=["tooling", "testing", "clean-code"],
        source_articles=[
            {
                "title": "Dependency injection for beginners",
                "path": "docs/articles/stitcher-io/2018-04-30-dependency-injection-for-beginners.md",
            },
            {
                "title": "Things dependency injection is not about",
                "path": "docs/articles/stitcher-io/2019-07-30-things-dependency-injection-is-not-about.md",
            },
            {
                "title": "Dealing with dependencies",
                "path": "docs/articles/stitcher-io/2022-01-19-dealing-with-dependencies.md",
            },
            {
                "title": "Dependency Hygiene",
                "path": "docs/articles/stitcher-io/2026-04-03-dependency-hygiene.md",
            },
            {
                "title": "Dealing with deprecations",
                "path": "docs/articles/stitcher-io/2022-05-18-dealing-with-deprecations.md",
            },
        ],
    ),
    TopicGuide(
        slug="tooling",
        title="Developer Tooling",
        description="Make quality tools easy to run, easy to automate, and boring enough that the team actually uses them.",
        rules=[
            "Put repeated tool commands behind scripts.",
            "Use formatting and static analysis as part of the normal development loop.",
            "Document repo conventions in config files, not only in memory.",
            "Adopt upgrade tools when they reduce risky manual work.",
        ],
        tips=[
            {
                "title": "Use Composer scripts as the stable interface",
                "body": "A single script can hide Pint, Rector, PHPStan, Pest, or other tools behind one command.",
                "source": "docs/videos/2024-10-19-why-were-using-composer-scripts-on-laravel-cloud-and-you-should-too-iVcLGN5Kcyc.md",
            },
            {
                "title": "Keep repo config explicit",
                "body": "Files such as `.editorconfig`, `.gitattributes`, and `.gitignore` teach both humans and tools how the project behaves.",
                "source": "docs/videos/2025-02-13-understanding-editorconfig-gitattributes-gitignore-etc-hmiNi7jDa-I.md",
            },
            {
                "title": "Use Rector for repeatable upgrades",
                "body": "Automated refactors reduce manual migration risk when modernizing PHP or Laravel code.",
                "source": "docs/videos/2025-01-04-why-you-should-start-using-rector-php-today-upgrade-legacy-php-to-modern-15tsiv6AvnE.md",
            },
        ],
        examples=[
            {
                "title": "Repository scripts",
                "body": "Scripts make tool usage discoverable.",
                "language": "json",
                "code": '{\n  "scripts": {\n    "format": "pint",\n    "analyse": "phpstan analyse",\n    "refactor": "rector --dry-run",\n    "test": "pest"\n  }\n}',
            },
        ],
        source_videos=[
            {
                "title": "Why We are Using Composer Scripts on Laravel Cloud (And You Should Too!)",
                "path": "docs/videos/2024-10-19-why-were-using-composer-scripts-on-laravel-cloud-and-you-should-too-iVcLGN5Kcyc.md",
            },
            {
                "title": "understanding .editorconfig, .gitattributes, .gitignore, etc...",
                "path": "docs/videos/2025-02-13-understanding-editorconfig-gitattributes-gitignore-etc-hmiNi7jDa-I.md",
            },
            {
                "title": "Rector PHP For Laravel is ACTUALLY INSANE",
                "path": "docs/videos/2025-10-10-rector-php-for-laravel-is-actually-insane-pmWUDBoFKhs.md",
            },
        ],
        related=["ai-engineering", "testing", "phpstan-type-safety"],
        source_articles=[
            {
                "title": "Dealing with deprecations",
                "path": "docs/articles/stitcher-io/2022-05-18-dealing-with-deprecations.md",
            },
            {
                "title": "Dependency Hygiene",
                "path": "docs/articles/stitcher-io/2026-04-03-dependency-hygiene.md",
            },
        ],
    ),
    TopicGuide(
        slug="frontend",
        title="Frontend Integration",
        description="Keep frontend choices type-safe, framework-aware, and connected to the backend contracts they depend on.",
        rules=[
            "Use TypeScript to catch bad imports, missing components, and contract drift.",
            "Keep routing, props, and generated helpers aligned with Laravel or backend state.",
            "Choose framework tools based on workflow fit, not only popularity.",
            "Test browser behavior when server-rendered assumptions are not enough.",
        ],
        tips=[
            {
                "title": "Use TypeScript as a contract check",
                "body": "Frontend code generated by AI needs the same compile-time pressure as backend code.",
                "source": "docs/videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md",
            },
            {
                "title": "Keep Laravel routes visible to JavaScript",
                "body": "Ziggy-style route helpers reduce stringly typed route drift between Laravel and Inertia.",
                "source": "docs/videos/2025-03-26-most-laravel-devs-miss-this-ziggy-config-inertia-pro-tip-OjtVtbyFRN8.md",
            },
            {
                "title": "Evaluate framework tradeoffs through real workflows",
                "body": "Compare React, Vue, Livewire, Inertia, and TanStack by how they affect shipping, testing, and team habits.",
                "source": "docs/videos/2026-05-08-why-react-developers-are-leaving-next-js-for-tanstack-6moPS3AAbe4.md",
            },
        ],
        examples=[
            {
                "title": "Typed page props",
                "body": "Make backend-provided props explicit in frontend code.",
                "language": "ts",
                "code": "type UserPageProps = {\n  user: {\n    id: number;\n    name: string;\n    email: string;\n  };\n};\n\nexport default function ShowUser({ user }: UserPageProps) {\n  return <h1>{user.name}</h1>;\n}",
            },
        ],
        source_videos=[
            {
                "title": "Why React Developers Are Leaving Next.js for TanStack",
                "path": "docs/videos/2026-05-08-why-react-developers-are-leaving-next-js-for-tanstack-6moPS3AAbe4.md",
            },
            {
                "title": "Most Laravel Devs Miss This Ziggy Config... (Inertia Pro Tip)",
                "path": "docs/videos/2025-03-26-most-laravel-devs-miss-this-ziggy-config-inertia-pro-tip-OjtVtbyFRN8.md",
            },
            {
                "title": "inertia v3 is really, really good",
                "path": "docs/videos/2026-03-06-inertia-v3-is-really-really-good-W8r-GoasK_A.md",
            },
        ],
        related=["ai-engineering", "tooling", "testing"],
    ),
]
