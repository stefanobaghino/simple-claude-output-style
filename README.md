# Make Claude write clearly, for everyone

This plugin adds a collection of [output styles](https://code.claude.com/docs/en/output-styles) for Claude Code. An output style replaces part of the system prompt of Claude Code, and thus shapes how Claude writes in every turn. This covers both the chat replies of Claude and the material that Claude writes, such as documentation and commit messages. The styles in this plugin aim at output that is clear, simple, and unambiguous, also for non-native readers.

| Style | Original source | Implementation |
|---|---|---|
| **classic-concise** | [The Elements of Style, 1918](https://www.gutenberg.org/ebooks/37134) | [classic-concise.md](plugin/output-styles/classic-concise.md) |
| **clarity-flow** | Style: Toward Clarity and Grace | [clarity-flow.md](plugin/output-styles/clarity-flow.md) |
| **developer-docs** | [Google developer documentation style guide](https://developers.google.com/style) | [developer-docs.md](plugin/output-styles/developer-docs.md) |
| **plain-language** | [Federal Plain Language Guidelines](https://digital.gov/guides/plain-language) | [plain-language.md](plugin/output-styles/plain-language.md) |
| **technical-simplified** | [ASD-STE100 Issue 9](https://www.asd-ste100.org/) | [technical-simplified.md](plugin/output-styles/technical-simplified.md) |

Each style keeps the default coding instructions of Claude Code.

## How to install the plugin

1. Add the marketplace:

   ```
   /plugin marketplace add stefanobaghino/claude-plugins
   ```

2. Install the plugin:

   ```
   /plugin install simple-output-styles
   ```

3. Open `/config`, then select **Output style** and pick a style.

## Sources and disclaimers

### classic-concise

The classic-concise style adapts the composition principles of The Elements of Style (William Strunk Jr., 1918), a work in the public domain. The style restates the principles in its own words and covers only the 1918 text, not the later editions. The style joins the collection for its philosophy: classic prescriptive concision, the archetypal "omit needless words" doctrine.

### clarity-flow

The clarity-flow style is an independent adaptation of the clarity principles taught in Style: Toward Clarity and Grace by Joseph M. Williams. It restates the principles in its own words. It does not reproduce the text, the examples, or the exercises of the book. The author and the publisher are not affiliated with this project, and they do not endorse it. The style joins the collection for its philosophy: reader-centered clarity grounded in reading psychology, with actors as subjects, actions as verbs, and old information before new.

### developer-docs

The developer-docs style adapts the [Google developer documentation style guide](https://developers.google.com/style), whose text is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/). This project is not affiliated with Google, and Google does not endorse it; the name refers only to the source guide. The style joins the collection for its philosophy: the modern industry documentation voice, direct and conversational, written for a global audience.

### plain-language

The plain-language style adapts the [Federal Plain Language Guidelines](https://digital.gov/guides/plain-language), a work of the United States government in the public domain. This project is not affiliated with the US government.

### technical-simplified

The technical-simplified style is an independent adaptation of the writing rules of ASD-STE100 Issue 9. It restates the rules in its own words. It does not reproduce the text, the examples, or the dictionary of the specification.

"ASD-STE100 Simplified Technical English" is a registered trademark of the Aerospace, Security and Defence Industries Association of Europe (ASD). This project uses the name only to refer to the specification. ASD and the STEMG are not affiliated with this project, and they do not endorse or certify this project.

This plugin does not make the output of Claude compliant with ASD-STE100. Download the full specification free of charge from [asd-ste100.org](https://www.asd-ste100.org/).

## License

Two licenses cover this project:

- The Zero-Clause BSD license (0BSD) covers the plugin, the rule files in `evals/rules/`, and every other file outside `evals/`. See [LICENSE](LICENSE). 0BSD requires no attribution notice, so you can copy a style text into your own setup without a license notice.
- The Apache License 2.0 covers the evaluation harness in `evals/`, except the rule files in `evals/rules/`. See [evals/LICENSE](evals/LICENSE).

The rule files stay under 0BSD because a rule file pairs with a style text. A fork of a style needs the matched rule file to measure the fork.

GitHub reads only the root license file, so the repository page shows 0BSD. This section states the full split.

The licenses cover only the content of this project: the adapted rules, the examples, and the packaging. The licenses do not give rights to the ASD-STE100 specification or to the trademarks of ASD.
