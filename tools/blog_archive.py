from __future__ import annotations

import json
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from tools.archive_tools import write_text


STITCHER_SOURCE = {
    "slug": "stitcher-io",
    "name": "Stitcher.io",
    "url": "https://stitcher.io/",
    "rss": "https://stitcher.io/rss",
    "sitemap": "https://stitcher.io/sitemap.xml",
    "author": "Brent Roose",
    "description": "Modern PHP, Laravel, web development, and programming practice articles by Brent Roose.",
}


@dataclass(frozen=True)
class CuratedBlogArticle:
    slug: str
    title: str
    url: str
    topics: list[str]
    why: str
    guidelines: list[dict[str, str]]
    examples: list[dict[str, str]]


STITCHER_CURATED_ARTICLES: list[CuratedBlogArticle] = [
    CuratedBlogArticle(
        slug="tests-and-types",
        title="Tests and types",
        url="https://stitcher.io/blog/tests-and-types",
        topics=["type-safety", "testing", "domain-modeling"],
        why="Shows why tests and types solve different parts of correctness. Types narrow the input space; tests still prove business behavior.",
        guidelines=[
            {
                "title": "Use types to remove whole classes of tests",
                "body": "A type signature can rule out nulls, strings, missing arguments, and other invalid shapes before business logic runs. Keep tests for behavior the type system cannot express.",
            },
            {
                "title": "Turn business ranges into domain types when the primitive is too wide",
                "body": "An integer type is still too broad for values such as RGB components, percentages, quantities, or ratings. Wrap constrained values in small domain objects when the range matters in more than one place.",
            },
            {
                "title": "Do not claim types replace tests",
                "body": "Types improve program correctness, but business correctness still needs examples. Use both: types for shape and invariants, tests for outcomes and workflows.",
            },
        ],
        examples=[
            {
                "title": "Constrained value object",
                "body": "Use a domain type when a primitive permits invalid business values.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class Rating\n{\n    public function __construct(public int $value)\n    {\n        if ($value < 1 || $value > 5) {\n            throw new InvalidArgumentException('Rating must be between 1 and 5.');\n        }\n    }\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="uncertainty-doubt-and-static-analysis",
        title="Uncertainty, doubt, and static analysis",
        url="https://stitcher.io/blog/uncertainty-doubt-and-static-analysis",
        topics=["type-safety", "static-analysis", "tooling"],
        why="Makes the case that modern PHP projects should lean into opt-in strictness instead of treating dynamic PHP as the default forever.",
        guidelines=[
            {
                "title": "Use static analysis as design feedback",
                "body": "PHPStan, Psalm, and IDE inspections are not only bug finders. They expose unclear shapes, weak return types, and APIs that force callers to guess.",
            },
            {
                "title": "Treat verbosity as a signal to improve boundaries",
                "body": "When typing feels noisy, look for missing concepts such as DTOs, value objects, collections, or named methods. The goal is clearer code, not annotations for their own sake.",
            },
        ],
        examples=[
            {
                "title": "Make array shapes explicit at the boundary",
                "body": "Static analysis becomes useful when boundary data has a documented shape.",
                "language": "php",
                "code": "<?php\n\n/** @return array{name: string, email: string} */\npublic function validatedData(): array\n{\n    return $this->validated();\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="what-about-request-classes",
        title="What about typed request classes?",
        url="https://stitcher.io/blog/what-about-request-classes",
        topics=["request-data", "laravel", "type-safety"],
        why="Explores the gap between Laravel validation arrays and typed request data that IDEs, static analysis, and application services can understand.",
        guidelines=[
            {
                "title": "Separate raw request validation from trusted application data",
                "body": "A form request is excellent at validating HTTP input, but the rest of the application benefits from a typed representation. Convert boundary arrays into a DTO or typed method before calling actions.",
            },
            {
                "title": "Make validation rules visible to tools where practical",
                "body": "String validation rules are easy for Laravel to run, but hard for PHPStan and IDEs to understand. Add typed accessors, DTOs, or dedicated data objects when the data crosses into reusable application code.",
            },
        ],
        examples=[
            {
                "title": "Request to data object",
                "body": "The controller converts HTTP input into typed data before calling the use case.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class UpdatePostData\n{\n    public function __construct(\n        public string $title,\n        public PostStatus $status,\n        public string $body,\n    ) {}\n}\n\nfinal class UpdatePostRequest extends FormRequest\n{\n    public function data(): UpdatePostData\n    {\n        $validated = $this->validated();\n\n        return new UpdatePostData(\n            title: $validated['title'],\n            status: PostStatus::from($validated['status']),\n            body: $validated['body'],\n        );\n    }\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="request-objects-in-tempest",
        title="Request objects in Tempest",
        url="https://stitcher.io/blog/request-objects-in-tempest",
        topics=["request-data", "type-safety", "framework-design"],
        why="Shows the same typed-boundary idea from a framework-design angle: the object you actually want should drive request validation and mapping.",
        guidelines=[
            {
                "title": "Design request handling around the target object",
                "body": "Instead of treating arrays as the application interface, define the object your use case needs and map the request into it as early as possible.",
            },
            {
                "title": "Infer obvious validation from types, then add explicit business rules",
                "body": "Required fields, nullability, scalar types, and enum values can often be derived from type signatures. Keep custom validation for rules the type system cannot express.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="deprecating-spatie-dto",
        title="Deprecating spatie/data-transfer-object",
        url="https://stitcher.io/blog/deprecating-spatie-dto",
        topics=["data-transfer", "type-safety", "dependencies"],
        why="A useful reminder that packages should become obsolete when the language and ecosystem grow better primitives for the same job.",
        guidelines=[
            {
                "title": "Do not keep a package only because it was once essential",
                "body": "When PHP native types, static analysis, or better mapping libraries cover the original need, retire or replace the older abstraction instead of stretching it into a different tool.",
            },
            {
                "title": "Choose DTO tooling for its current job",
                "body": "Runtime type checking, request mapping, serialization, and validation are related but different problems. Pick tools that match the job instead of expecting one DTO package to own all of them.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="php-enum-style-guide",
        title="My PHP enum style guide",
        url="https://stitcher.io/blog/php-enum-style-guide",
        topics=["enums", "domain-modeling", "type-safety"],
        why="Gives practical enum rules that help PHP domain states stay expressive without adding unnecessary backing values or label coupling.",
        guidelines=[
            {
                "title": "Use backed enums only when persistence or serialization needs a stable value",
                "body": "A pure enum is enough for in-code states. Add string or integer backing only when a database, API, queue payload, or external contract needs it.",
            },
            {
                "title": "Keep display labels out of enum backing values",
                "body": "Backing values are technical contracts. UI labels are presentation concerns and should live in methods, translation files, or presenters.",
            },
            {
                "title": "Allow simple behavior on enums",
                "body": "Small match-based methods can keep state-specific behavior close to the state while avoiding scattered switch statements.",
            },
        ],
        examples=[
            {
                "title": "Enum with behavior and separate label",
                "body": "Keep the stored value stable and the label replaceable.",
                "language": "php",
                "code": "<?php\n\nenum OrderStatus: string\n{\n    case DRAFT = 'draft';\n    case PAID = 'paid';\n    case CANCELLED = 'cancelled';\n\n    public function canBeShipped(): bool\n    {\n        return $this === self::PAID;\n    }\n\n    public function label(): string\n    {\n        return __('orders.status.' . $this->value);\n    }\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="testing-patterns",
        title="Testing Patterns",
        url="https://stitcher.io/blog/testing-patterns",
        topics=["testing", "maintainability"],
        why="Shows how test design affects whether people keep adding tests when the number of cases grows.",
        guidelines=[
            {
                "title": "Reduce test friction for repeated cases",
                "body": "When dozens of similar behaviors need coverage, move the common assertion shape into a reusable test helper and keep each case close to the behavior it documents.",
            },
            {
                "title": "Avoid a giant data-provider dumping ground",
                "body": "Centralized data providers can reduce duplication but become hard to navigate. Prefer distributed fixtures or per-feature cases when the list grows large.",
            },
            {
                "title": "Make test failures point to the broken case",
                "body": "A scalable test pattern should make it obvious which input, class, or pattern failed without making the developer search through a shared table.",
            },
        ],
        examples=[
            {
                "title": "Case object for repeated tests",
                "body": "Keep each case named and close to the domain concept being tested.",
                "language": "php",
                "code": "<?php\n\nit('parses invoice numbers', function (string $input, string $expected) {\n    expect(InvoiceNumber::fromString($input)->value)->toBe($expected);\n})->with([\n    'plain number' => ['INV-1001', 'INV-1001'],\n    'lowercase prefix' => ['inv-1001', 'INV-1001'],\n]);\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="what-event-sourcing-is-not-about",
        title="Starting with event sourcing",
        url="https://stitcher.io/blog/what-event-sourcing-is-not-about",
        topics=["event-sourcing", "ddd", "architecture"],
        why="Reframes event sourcing as a modeling choice, not only an enterprise-scale infrastructure pattern.",
        guidelines=[
            {
                "title": "Use event sourcing for behavior that needs history, not for every table",
                "body": "The useful question is not whether the app is big enough. Ask whether the domain benefits from replayable facts, auditability, temporal reporting, or process reconstruction.",
            },
            {
                "title": "Start from the event stream as the source of truth",
                "body": "In event-sourced code, state is derived from facts that happened. Name events in past tense and keep projections as read models, not as the primary record of truth.",
            },
        ],
        examples=[
            {
                "title": "Past-tense domain event",
                "body": "An event records a fact; commands and actions request work.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class InvoiceWasPaid\n{\n    public function __construct(\n        public string $invoiceId,\n        public Money $amount,\n        public DateTimeImmutable $paidAt,\n    ) {}\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="combining-event-sourcing-and-stateful-systems",
        title="Combining event sourcing and stateful systems",
        url="https://stitcher.io/blog/combining-event-sourcing-and-stateful-systems",
        topics=["event-sourcing", "ddd", "architecture"],
        why="Explains that a Laravel application can mix CRUD-style stateful models and event-sourced domains instead of forcing one architecture everywhere.",
        guidelines=[
            {
                "title": "Event source the domains that need it",
                "body": "Use ordinary Eloquent models for simple admin CRUD or low-history data. Use event sourcing where history, reporting, money movement, or workflow reconstruction is central.",
            },
            {
                "title": "Keep projections disposable",
                "body": "A projection exists to answer reads. It should be rebuildable from events, so do not hide irreversible business writes inside a projector.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="a-new-major-version-of-laravel-event-sourcing",
        title="A new major version of Laravel Event Sourcing",
        url="https://stitcher.io/blog/a-new-major-version-of-laravel-event-sourcing",
        topics=["event-sourcing", "laravel", "architecture"],
        why="Highlights implementation practices for Laravel event-sourced systems: consistent handler registration, event queries, aggregate partials, and command bus boundaries.",
        guidelines=[
            {
                "title": "Register event handlers by event type, not naming magic",
                "body": "Consistent event handling makes aggregates, projectors, and reactors easier to scan and safer to refactor.",
            },
            {
                "title": "Use event queries for occasional reads before adding projections",
                "body": "If a read model is only needed occasionally, an event query can avoid permanent projection maintenance. Promote it to a projection when read volume or complexity justifies it.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="dependency-injection-for-beginners",
        title="Dependency injection for beginners",
        url="https://stitcher.io/blog/dependency-injection-for-beginners",
        topics=["dependencies", "architecture", "object-design"],
        why="Explains dependency injection as composition: objects receive collaborators instead of constructing or locating everything themselves.",
        guidelines=[
            {
                "title": "Compose behavior from collaborators",
                "body": "Prefer giving an object the collaborator it needs over hard-coding concrete construction inside it. This makes variation explicit and testing simpler.",
            },
            {
                "title": "Do not inject every scalar or incidental value",
                "body": "Dependency injection is for services and collaborators. Runtime data should usually be method input or a value object.",
            },
        ],
        examples=[
            {
                "title": "Inject the collaborator, pass runtime data",
                "body": "The mailer is a dependency; the email address is input.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class InviteUser\n{\n    public function __construct(private Mailer $mailer) {}\n\n    public function handle(EmailAddress $email): void\n    {\n        $this->mailer->send(new InvitationMail($email));\n    }\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="things-dependency-injection-is-not-about",
        title="Things dependency injection is not about",
        url="https://stitcher.io/blog/things-dependency-injection-is-not-about",
        topics=["dependencies", "testing", "architecture"],
        why="Clarifies the difference between dependency injection and service location, which matters a lot in Laravel service-container-heavy codebases.",
        guidelines=[
            {
                "title": "Do not use the container as a service locator inside domain code",
                "body": "Calling the container from inside classes hides dependencies and makes tests guess what the object needs. Let Laravel resolve dependencies at the boundary, then pass them explicitly.",
            },
            {
                "title": "Constructor signatures are documentation",
                "body": "A constructor that names collaborators tells reviewers, static analysis, and tests what the object needs. Hidden container calls erase that information.",
            },
        ],
        examples=[
            {
                "title": "Avoid service location in an action",
                "body": "Ask for the dependency once instead of resolving it at the point of use.",
                "language": "php",
                "code": "<?php\n\nfinal readonly class PublishPost\n{\n    public function __construct(private SearchIndexer $indexer) {}\n\n    public function handle(Post $post): void\n    {\n        $post->publish();\n        $this->indexer->index($post);\n    }\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="dealing-with-dependencies",
        title="Dealing with dependencies",
        url="https://stitcher.io/blog/dealing-with-dependencies",
        topics=["dependencies", "maintenance", "upgrades"],
        why="Gives an upgrade playbook for external dependencies: test early, contribute fixes, look for alternatives, and fork only as a last resort.",
        guidelines=[
            {
                "title": "Test dependency compatibility before the release day",
                "body": "Start checking against PHP and framework release candidates so incompatibilities are discovered while there is still time to fix them upstream.",
            },
            {
                "title": "Prefer upstream contribution over local workarounds",
                "body": "If a package blocks an upgrade, first check existing issues and pull requests, then offer a focused fix. Forking transfers maintenance burden to your app and should be a last resort.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="dependency-hygiene",
        title="Dependency Hygiene",
        url="https://stitcher.io/blog/dependency-hygiene",
        topics=["dependencies", "security", "maintenance"],
        why="Turns package management into an explicit security and maintenance practice, not just `composer require` muscle memory.",
        guidelines=[
            {
                "title": "Audit why every package is installed",
                "body": "Use `composer why` and remove dependencies that are no longer used. Unused packages still expand the code you trust, update, and scan.",
            },
            {
                "title": "Treat transitive dependencies as part of your system",
                "body": "Package managers make dependency trees easy to ignore. Review high-impact transitive packages, especially around security, crypto, HTTP, file handling, and build tooling.",
            },
        ],
        examples=[
            {
                "title": "Dependency audit commands",
                "body": "Small checks make package ownership visible during maintenance.",
                "language": "bash",
                "code": "composer why symfony/polyfill-mbstring\ncomposer why-not php ^8.4\ncomposer audit\ncomposer outdated --direct\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="dealing-with-deprecations",
        title="Dealing with deprecations",
        url="https://stitcher.io/blog/dealing-with-deprecations",
        topics=["maintenance", "upgrades", "tooling"],
        why="Frames deprecations as early upgrade signals instead of noisy failures to ignore forever.",
        guidelines=[
            {
                "title": "Use deprecations as an upgrade backlog",
                "body": "A deprecation means the code still works today but has a known future break. Track and reduce them incrementally instead of waiting for the next major version to fail hard.",
            },
            {
                "title": "Automate deprecation cleanup where possible",
                "body": "Rector, static analysis, CI logs, and dependency update runs can turn deprecations into small regular fixes instead of a risky upgrade project.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="strategies",
        title="Dynamic Strategies",
        url="https://stitcher.io/blog/strategies",
        topics=["architecture", "extensibility", "type-safety"],
        why="Explores the strategy pattern from the API consumer's point of view, including how extensibility can weaken type guarantees if the boundary is not designed carefully.",
        guidelines=[
            {
                "title": "Design extension points from the implementer side too",
                "body": "A strategy interface should be pleasant for both the core object and third-party implementations. If implementers need awkward casts or broad mixed inputs, the extension point is leaking complexity.",
            },
            {
                "title": "Keep strategy inputs as narrow as possible",
                "body": "A strategy receiving `mixed` can support many cases but loses static guarantees. Split strategies or add typed adapters when the behavior has different input families.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="extends-vs-implements",
        title="Extend or implement",
        url="https://stitcher.io/blog/extends-vs-implements",
        topics=["object-design", "architecture", "ddd"],
        why="Offers a useful mental model for inheritance versus interfaces: inherit for real domain identity, implement for technical capability.",
        guidelines=[
            {
                "title": "Use inheritance for true specialization, not framework convenience",
                "body": "If a class is not really a subtype in the domain, prefer composition or an interface. Framework base classes can be practical, but do not let them define your domain model language.",
            },
            {
                "title": "Use interfaces for acts-as capabilities",
                "body": "An interface says the object can perform a role in this context. That is different from saying the object is fundamentally that thing.",
            },
        ],
        examples=[
            {
                "title": "Capability interface",
                "body": "A model may act as billable without making billing its whole identity.",
                "language": "php",
                "code": "<?php\n\ninterface Billable\n{\n    public function billingReference(): string;\n}\n\nfinal class Team implements Billable\n{\n    public function billingReference(): string\n    {\n        return 'team:' . $this->id;\n    }\n}\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="dont-be-clever",
        title="Don't be clever",
        url="https://stitcher.io/blog/dont-be-clever",
        topics=["clean-code", "architecture", "maintainability"],
        why="A warning against abstractions that look elegant until real business exceptions start accumulating around them.",
        guidelines=[
            {
                "title": "Do not abstract before the business variation is visible",
                "body": "Generic controllers, repositories, or service layers can hide duplication, but they also hide the places where workflows differ. Wait until the repeated shape and the exceptions are both understood.",
            },
            {
                "title": "Prefer boring explicit code over clever shared machinery",
                "body": "If a small business exception requires hooks, flags, and override methods, the abstraction is probably costing more than the duplication it removed.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="laravel-view-models-vs-view-composers",
        title="Laravel view models vs. view composers",
        url="https://stitcher.io/blog/laravel-view-models-vs-view-composers",
        topics=["laravel", "frontend", "explicit-boundaries"],
        why="Shows why explicit view data is easier to maintain than variables injected through global registration.",
        guidelines=[
            {
                "title": "Prefer explicit view models for complex screens",
                "body": "A view model makes it clear which data a view receives and where it comes from. View composers can be fine for global layout data, but they hide page-specific inputs.",
            },
            {
                "title": "Make reusable views receive their data intentionally",
                "body": "Create and edit screens can share a form more safely when the controller passes an explicit object instead of relying on ambient variables.",
            },
        ],
        examples=[],
    ),
    CuratedBlogArticle(
        slug="unsafe-sql-functions-in-laravel",
        title="Unsafe SQL functions in Laravel",
        url="https://stitcher.io/blog/unsafe-sql-functions-in-laravel",
        topics=["laravel", "security", "database"],
        why="A concrete Laravel reminder that framework helpers do not make user-controlled column names or raw SQL fragments safe by default.",
        guidelines=[
            {
                "title": "Whitelist user-selectable columns",
                "body": "Never let request input directly choose SQL columns, JSON paths, `orderBy` fields, or select expressions. Map public filter names to known internal columns.",
            },
            {
                "title": "Prefer framework-safe syntax over raw fragments",
                "body": "Use Laravel's supported JSON selector syntax and query builder APIs where possible, but still validate which fields the user is allowed to address.",
            },
        ],
        examples=[
            {
                "title": "Whitelist sortable fields",
                "body": "Map request values to known columns before passing them to the query builder.",
                "language": "php",
                "code": "<?php\n\n$sort = $request->string('sort')->toString();\n\n$column = [\n    'name' => 'users.name',\n    'created' => 'users.created_at',\n][$sort] ?? 'users.created_at';\n\nUser::query()->orderBy($column)->get();\n",
            },
        ],
    ),
    CuratedBlogArticle(
        slug="reducing-code-motion",
        title="Reducing code motion",
        url="https://stitcher.io/blog/reducing-code-motion",
        topics=["clean-code", "state-modeling", "maintainability"],
        why="Shows how simplifying state transitions can remove commands, schedules, tests, and moving parts at once.",
        guidelines=[
            {
                "title": "Model fewer states when a date or attribute captures the same truth",
                "body": "If a state exists only to schedule a future transition, consider whether a published state plus a publication date expresses the rule with less machinery.",
            },
            {
                "title": "Count operational motion, not only lines of code",
                "body": "A design with fewer cron jobs, commands, state transitions, and coordination points is often easier to test and operate even if the remaining code is not shorter.",
            },
        ],
        examples=[],
    ),
]

CURATED_BY_SLUG = {article.slug: article for article in STITCHER_CURATED_ARTICLES}
PROGRAMMING_TOPIC_KEYWORDS = {
    "architecture": ["architecture", "framework", "object", "objects", "strategy", "strategies", "extend", "implement", "dependency", "dependencies"],
    "database": ["database", "mysql", "sql", "uuid", "query", "foreign key"],
    "ddd": ["event sourcing", "domain", "aggregate", "state", "model"],
    "dependencies": ["dependency", "dependencies", "package", "composer", "deprecation", "upgrade"],
    "laravel": ["laravel", "eloquent", "nova", "request", "view model", "event sourcing"],
    "php": ["php", "enum", "generics", "readonly", "attribute", "typed", "type", "jit"],
    "security": ["security", "unsafe", "injection", "hygiene"],
    "testing": ["test", "testing", "tests"],
    "tooling": ["phpstorm", "static analysis", "composer", "homebrew", "rector"],
}
NON_PROGRAMMING_KEYWORDS = [
    "timeline taxi",
    "fiction",
    "novel",
    "motivator",
    "sponsor",
    "twitter",
    "mastodon",
    "ikea",
    "christmas",
    "light theme",
    "colour scheme",
    "jazz",
    "podcast",
]


def load_stitcher_rss(path: Path) -> list[dict]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = []

    for entry in root.findall("atom:entry", ns):
        link = entry.find("atom:link", ns)
        url = link.attrib.get("href", "") if link is not None else entry.findtext("atom:id", default="", namespaces=ns)
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        published = (entry.findtext("atom:published", default="", namespaces=ns) or "")[:10]
        author = entry.findtext("atom:author/atom:name", default=STITCHER_SOURCE["author"], namespaces=ns)
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        entries.append(
            {
                "slug": slug,
                "title": title,
                "url": url,
                "published": published,
                "author": author.strip() or STITCHER_SOURCE["author"],
            }
        )

    return entries


def enrich_stitcher_articles(entries: Iterable[dict]) -> list[dict]:
    enriched = []

    for entry in entries:
        article = dict(entry)
        curated = CURATED_BY_SLUG.get(article["slug"])
        if curated:
            article["archive_status"] = "curated-processed"
            article["topics"] = curated.topics
            article["reason"] = "curated programming guideline source"
            article["note_path"] = str(Path("docs/articles/stitcher-io") / f"{article['published']}-{article['slug']}.md")
        else:
            classification = classify_blog_article(article)
            article.update(classification)
        enriched.append(article)

    return enriched


def classify_blog_article(article: dict) -> dict:
    title = str(article.get("title") or "")
    url = str(article.get("url") or "")
    haystack = f"{title} {url}".lower()

    if any(keyword in haystack for keyword in NON_PROGRAMMING_KEYWORDS):
        return {
            "archive_status": "skipped",
            "topics": [],
            "reason": "not a focused reusable programming-practice source",
        }

    topics = [
        topic
        for topic, keywords in PROGRAMMING_TOPIC_KEYWORDS.items()
        if any(keyword in haystack for keyword in keywords)
    ]

    if topics:
        return {
            "archive_status": "candidate",
            "topics": sorted(set(topics)),
            "reason": "programming-related article not yet manually distilled",
        }

    return {
        "archive_status": "skipped",
        "topics": [],
        "reason": "no clear reusable programming guideline detected from metadata",
    }


def render_curated_article_note(article: CuratedBlogArticle, metadata: dict) -> str:
    published = metadata.get("published") or "unknown-date"
    lines = [
        f"# {article.title}",
        "",
        f"URL: {article.url}",
        "Source: [Stitcher.io](https://stitcher.io/)",
        f"Author: {metadata.get('author') or STITCHER_SOURCE['author']}",
        f"Published: {published}",
        "Status: curated-processed",
        f"Topics: {', '.join(article.topics)}",
        "",
        "## Why This Helps Programming",
        article.why,
        "",
        "## Guidelines",
    ]

    for guideline in article.guidelines:
        lines.extend([
            f"### {guideline['title']}",
            guideline["body"],
            "",
        ])

    lines.append("## Examples")
    if article.examples:
        for example in article.examples:
            lines.extend([
                f"### {example['title']}",
                example.get("body", ""),
                "",
                f"```{example.get('language', '').strip()}".rstrip(),
                example["code"].rstrip(),
                "```",
                "",
            ])
    else:
        lines.extend(["No concrete code example was added for this article yet.", ""])

    lines.extend(
        [
            "## Source Notes",
            "- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.",
            "- Use the URL above when the original wording, full context, or comments matter.",
            "",
        ]
    )

    return "\n".join(lines)


def render_articles_index(articles: list[dict]) -> str:
    lines = [
        "# Stitcher.io Article Inventory",
        "",
        "This file tracks Stitcher.io articles discovered from the RSS feed and whether they have been distilled into local guidance.",
        "",
        "| Status | Published | Title | Topics | Note |",
        "| --- | --- | --- | --- | --- |",
    ]

    for article in sorted(articles, key=lambda item: (item.get("published") or "", item.get("title") or ""), reverse=True):
        status = article.get("archive_status", "unknown")
        published = article.get("published") or "unknown-date"
        title = article.get("title") or article.get("slug") or "Untitled"
        topics = ", ".join(article.get("topics") or []) or "-"
        if note_path := article.get("note_path"):
            note = f"[note](../../../../{note_path})"
        else:
            note = "-"
        lines.append(f"| {status} | {published} | [{_escape_table(title)}]({article['url']}) | {_escape_table(topics)} | {note} |")

    lines.append("")
    return "\n".join(lines)


def render_blogs_readme() -> str:
    return "\n".join(
        [
            "# Source Blogs",
            "",
            "Each blog source gets its own source folder:",
            "",
            "```text",
            "data/source/blogs/<blog-slug>/",
            "  source.json",
            "  README.md",
            "  rss.raw.xml",
            "  articles.raw.jsonl",
            "  articles.jsonl",
            "```",
            "",
            "Store source metadata and curated analysis notes, not full copied article bodies. Generated Markdown should link to the original article and keep guidance paraphrased.",
            "",
            "## Current Blogs",
            "",
            "- [stitcher-io](stitcher-io/README.md)",
            "",
        ]
    )


def render_stitcher_readme(articles: list[dict]) -> str:
    total = len(articles)
    curated = sum(1 for article in articles if article.get("archive_status") == "curated-processed")
    candidates = sum(1 for article in articles if article.get("archive_status") == "candidate")
    skipped = sum(1 for article in articles if article.get("archive_status") == "skipped")

    return "\n".join(
        [
            "# Stitcher.io Source Snapshot",
            "",
            "This folder contains the source metadata used to distill programming guidelines from [Stitcher.io](https://stitcher.io/).",
            "",
            f"- Articles discovered from RSS: {total}",
            f"- Curated into local notes: {curated}",
            f"- Programming candidates not yet distilled: {candidates}",
            f"- Skipped: {skipped}",
            "",
            "## Files",
            "",
            "- `source.json` describes the source.",
            "- `rss.raw.xml` is the fetched RSS snapshot used for this crawl.",
            "- `articles.raw.jsonl` stores RSS article metadata.",
            "- `articles.jsonl` stores enriched processing status and note paths.",
            "- `articles.md` is the human-readable processing index.",
            "",
            "Full article bodies are not copied into the repository. Curated notes in `docs/articles/stitcher-io` link back to the original article and paraphrase the extracted guidance.",
            "",
            "## Regeneration",
            "",
            "```bash",
            "curl -L -o /tmp/stitcher-rss.xml https://stitcher.io/rss",
            "python3 -m tools.render_blog_archive --source stitcher-io --rss /tmp/stitcher-rss.xml --repo .",
            "```",
            "",
        ]
    )


def render_blog_sources_index(articles: list[dict]) -> str:
    curated = [article for article in articles if article.get("archive_status") == "curated-processed"]
    lines = [
        "# Blog Source Index",
        "",
        "Blog sources add durable written guidance alongside video-derived notes. Prefer topic guides for search; use article notes for provenance.",
        "",
        "## Sources",
        "",
        "- [Stitcher.io](../../data/source/blogs/stitcher-io/README.md) - PHP, Laravel, architecture, event sourcing, type safety, and maintenance guidance.",
        "",
        "## Curated Stitcher.io Articles",
        "",
    ]

    for article in sorted(curated, key=lambda item: item.get("published") or "", reverse=True):
        note = article.get("note_path", "")
        link = "../articles/stitcher-io/" + Path(note).name if note else article["url"]
        lines.append(f"- [{article['title']}]({link}) - {', '.join(article.get('topics') or [])}")

    lines.append("")
    return "\n".join(lines)


def write_stitcher_archive(repo: Path, rss_path: Path) -> list[dict]:
    source_dir = repo / "data/source/blogs/stitcher-io"
    articles_dir = repo / "docs/articles/stitcher-io"
    entries = load_stitcher_rss(rss_path)
    articles = enrich_stitcher_articles(entries)
    metadata_by_slug = {article["slug"]: article for article in articles}

    source_dir.mkdir(parents=True, exist_ok=True)
    articles_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(rss_path, source_dir / "rss.raw.xml")

    write_text(repo / "data/source/blogs/README.md", render_blogs_readme())
    write_text(source_dir / "source.json", json.dumps({**STITCHER_SOURCE, "fetched_at": date.today().isoformat()}, indent=2) + "\n")
    write_text(source_dir / "README.md", render_stitcher_readme(articles))
    write_text(source_dir / "articles.raw.jsonl", "\n".join(json.dumps(entry, ensure_ascii=False) for entry in entries) + "\n")
    write_text(source_dir / "articles.jsonl", "\n".join(json.dumps(article, ensure_ascii=False) for article in articles) + "\n")
    write_text(source_dir / "articles.md", render_articles_index(articles))
    write_text(repo / "docs/indexes/blog-sources.md", render_blog_sources_index(articles))

    for curated in STITCHER_CURATED_ARTICLES:
        metadata = metadata_by_slug.get(curated.slug)
        if not metadata:
            continue
        filename = f"{metadata['published']}-{metadata['slug']}.md"
        write_text(articles_dir / filename, render_curated_article_note(curated, metadata))

    return articles


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|")
