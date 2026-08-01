# Make Claude write clearly, for everyone

*Output styles for Claude Code.*

This plugin adds two output styles:

- **technical-simplified** — strict writing rules from ASD-STE100 Issue 9. The output becomes clear, simple, and unambiguous, also for non-native readers.
- **plain-language** — reader-first writing rules from the Federal Plain Language Guidelines. The output becomes clear at the first read, with a natural tone.

Each style applies to chat answers, code comments, commit messages, PR text, and documentation. Each style keeps the default coding instructions of Claude Code.

## How to install the plugin

1. Add the marketplace:

   ```
   /plugin marketplace add stefanobaghino/claude-plugins
   ```

2. Install the plugin:

   ```
   /plugin install simple-output-styles
   ```

3. Open `/config`, then select **Output style** > **technical-simplified** or **plain-language**.

## What the styles do

**technical-simplified** is the strict style:

- The style uses one term per concept and the simplest word that keeps the meaning.
- It permits only the modal verbs "can", "must", and "will".
- It uses the active voice and simple tenses.
- It limits sentences to 20 words for instructions and 25 words for descriptions.
- It removes contractions, Latin abbreviations, and ambiguous pronouns.

**plain-language** is the natural style:

- The style puts the answer first and one idea in each sentence.
- It addresses the reader as "you" and uses the active voice and the present tense.
- It picks familiar words, removes hidden verbs, and limits abbreviations.
- It reserves "must" for obligations and never uses "shall".
- It permits contractions where they sound natural.

See [plugin/output-styles/technical-simplified.md](plugin/output-styles/technical-simplified.md) and [plugin/output-styles/plain-language.md](plugin/output-styles/plain-language.md) for the full rules.

## Attribution and disclaimer

This project is an independent adaptation of the writing rules of ASD-STE100 Issue 9. It restates the rules in its own words. It does not reproduce the text, the examples, or the dictionary of the specification.

The plain-language style adapts the [Federal Plain Language Guidelines](https://digital.gov/guides/plain-language), a work of the United States government in the public domain. This project is not affiliated with the US government.

"ASD-STE100 Simplified Technical English" is a registered trademark of the Aerospace, Security and Defence Industries Association of Europe (ASD). This project uses the name only to refer to the specification. ASD and the STEMG are not affiliated with this project, and they do not endorse or certify this project.

This plugin does not make the output of Claude compliant with ASD-STE100. Download the full specification free of charge from [asd-ste100.org](https://www.asd-ste100.org/).

## License

The Zero-Clause BSD license (0BSD) covers this project. See [LICENSE](LICENSE).

The license covers only the content of this project: the adapted rules, the examples, and the packaging. The license does not give rights to the ASD-STE100 specification or to the trademarks of ASD.
