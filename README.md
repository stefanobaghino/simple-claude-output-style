# Make Claude write clearly, for everyone

*Output styles for Claude Code.*

This plugin adds a collection of output styles.

| Style | Original source | Implementation |
|---|---|---|
| **technical-simplified** | [ASD-STE100 Issue 9](https://www.asd-ste100.org/) | [technical-simplified.md](plugin/output-styles/technical-simplified.md) |
| **plain-language** | [Federal Plain Language Guidelines](https://digital.gov/guides/plain-language) | [plain-language.md](plugin/output-styles/plain-language.md) |

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

## Attribution and disclaimer

### technical-simplified

The technical-simplified style is an independent adaptation of the writing rules of ASD-STE100 Issue 9. It restates the rules in its own words. It does not reproduce the text, the examples, or the dictionary of the specification.

"ASD-STE100 Simplified Technical English" is a registered trademark of the Aerospace, Security and Defence Industries Association of Europe (ASD). This project uses the name only to refer to the specification. ASD and the STEMG are not affiliated with this project, and they do not endorse or certify this project.

This plugin does not make the output of Claude compliant with ASD-STE100. Download the full specification free of charge from [asd-ste100.org](https://www.asd-ste100.org/).

### plain-language

The plain-language style adapts the [Federal Plain Language Guidelines](https://digital.gov/guides/plain-language), a work of the United States government in the public domain. This project is not affiliated with the US government.

## License

The Zero-Clause BSD license (0BSD) covers this project. See [LICENSE](LICENSE).

The license covers only the content of this project: the adapted rules, the examples, and the packaging. The license does not give rights to the ASD-STE100 specification or to the trademarks of ASD.
