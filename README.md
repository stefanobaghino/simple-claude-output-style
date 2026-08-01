# Simplified Technical English for Claude Code

This plugin adds one output style: **STE**. The style makes Claude write in Simplified Technical English, adapted from ASD-STE100 Issue 9. The output becomes clear, simple, and unambiguous, also for non-native readers.

The style applies to chat answers, code comments, commit messages, PR text, and documentation. It keeps the standard coding instructions of Claude Code.

## Installation

1. Add the marketplace:

   ```
   /plugin marketplace add stefanobaghino/simple-claude-output-style
   ```

2. Install the plugin:

   ```
   /plugin install ste@simple-claude-output-style
   ```

3. Open `/config`, then select **Output style** > **STE**.

## What the style does

- It uses one term per concept and the simplest word that keeps the meaning.
- It permits only the modal verbs "can", "must", and "will".
- It uses the active voice and simple tenses.
- It limits sentences to 20 words for instructions and 25 words for descriptions.
- It removes contractions, Latin abbreviations, and ambiguous pronouns.

See [output-styles/ste.md](output-styles/ste.md) for the full rules.
