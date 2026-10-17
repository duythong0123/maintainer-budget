# Ecosystem demo: `microsoft/vscode`

This page is **not** presented as a current Maintainer Budget candidate cluster. It documents public evidence that repository-specific lifecycle knowledge is important enough to be maintained as agent instructions in a large codebase.

## Explicit repository learning

In [PR #278245](https://github.com/microsoft/vscode/pull/278245), VS Code standardized "Learnings" sections across instruction files. One example added to the disposable guidance was:

> Always register created disposables immediately using `this._register()` to prevent memory leaks.

That is repository memory written down for contributors and coding agents.

## The important nuance

The same codebase also contains a more specific lifecycle constraint. [PR #314636](https://github.com/microsoft/vscode/pull/314636) describes a leak caused by registering a disposable to the containing class **inside a repeatedly called method**, citing the project's own guidance against that pattern.

So a useful rule cannot simply be:

```text
Always use this._register()
```

It needs scope and evidence, for example:

```text
Register lifetime-scoped disposables with this._register(),
but do not attach per-call/per-session disposables to a long-lived
containing class when the method can run repeatedly.
```

That distinction is exactly why Maintainer Budget keeps provenance and requires human approval rather than asking a model to invent a generic "best practice" sentence.

## Repeated maintenance pressure

VS Code has multiple public leak-fix PRs involving disposable scope and repeated registration, including [#312613](https://github.com/microsoft/vscode/pull/312613), [#307958](https://github.com/microsoft/vscode/pull/307958), [#306832](https://github.com/microsoft/vscode/pull/306832), and [#287025](https://github.com/microsoft/vscode/pull/287025).

These are not counted as alpha review-comment candidates here. They are landscape evidence that local lifecycle conventions can become recurring maintenance knowledge and that exporting well-supported rules into repository instructions has practical value.
