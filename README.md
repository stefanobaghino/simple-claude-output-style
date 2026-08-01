# Make Claude write clearly, for everyone

*An output style for Claude Code.*

This plugin adds one output style: **simple**. The style makes Claude write in Simplified Technical English. The rules come from ASD-STE100 Issue 9, with changes for chat and code work. The output becomes clear, simple, and unambiguous, also for non-native readers.

The style applies to chat answers, code comments, commit messages, PR text, and documentation. The style keeps the default coding instructions of Claude Code.

## How to install the plugin

1. Add the marketplace:

   ```
   /plugin marketplace add stefanobaghino/simple-claude-output-style
   ```

2. Install the plugin:

   ```
   /plugin install simple-claude-output-style
   ```

3. Open `/config`, then select **Output style** > **simple**.

## What the style does

- The style uses one term per concept and the simplest word that keeps the meaning.
- It permits only the modal verbs "can", "must", and "will".
- It uses the active voice and simple tenses.
- It limits sentences to 20 words for instructions and 25 words for descriptions.
- It removes contractions, Latin abbreviations, and ambiguous pronouns.

See [output-styles/simple.md](output-styles/simple.md) for the full rules.

## Attribution and disclaimer

This project is an independent adaptation of the writing rules of ASD-STE100 Issue 9. It restates the rules in its own words. It does not reproduce the text, the examples, or the dictionary of the specification.

"ASD-STE100 Simplified Technical English" is a registered trademark of the Aerospace, Security and Defence Industries Association of Europe (ASD). This project uses the name only to refer to the specification. ASD and the STEMG are not affiliated with this project, and they do not endorse or certify this project.

This plugin does not make the output of Claude compliant with ASD-STE100. Download the full specification free of charge from [asd-ste100.org](https://www.asd-ste100.org/).

## License

The Zero-Clause BSD license (0BSD) covers this project. See [LICENSE](LICENSE).

The license covers only the content of this project: the adapted rules, the examples, and the packaging. The license does not give rights to the ASD-STE100 specification or to the trademarks of ASD.
