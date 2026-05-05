# Project: languagetool — Merge commit SHA1: c7f12513db90c922230311acc08dbab2ec677885

## Modified file(s):
`languagetool-core/src/main/java/org/languagetool/rules/spelling/morfologik/MorfologikSpellerRule.java`

## Class(es) modified in the merge:
`MorfologikSpellerRule`

## Merge effort lines in the combined diff

```diff
       if (tokenizingPattern() == null) {
-        ruleMatches.addAll(getRuleMatches(word, token.getStartPos(), sentence));
 -       ruleMatches.addAll(getRuleMatches(word, token.getStartPos(), sentence, ruleMatches));
++        ruleMatches.addAll(getRuleMatches(word, token.getStartPos(), sentence, ruleMatches));
       } else {
         int index = 0;
         Matcher m = tokenizingPattern().matcher(word);
         while (m.find()) {
           String match = word.subSequence(index, m.start()).toString();
-          ruleMatches.addAll(getRuleMatches(match, token.getStartPos() + index, sentence));
 -         ruleMatches.addAll(getRuleMatches(match, token.getStartPos() + index, sentence, ruleMatches));
++          ruleMatches.addAll(getRuleMatches(match, token.getStartPos() + index, sentence, ruleMatches));
           index = m.end();
         }
         if (index == 0) { // tokenizing char not found
-          ruleMatches.addAll(getRuleMatches(word, token.getStartPos(), sentence));
 -         ruleMatches.addAll(getRuleMatches(word, token.getStartPos(), sentence, ruleMatches));
++          ruleMatches.addAll(getRuleMatches(word, token.getStartPos(), sentence, ruleMatches));
         } else {
           ruleMatches.addAll(getRuleMatches(word.subSequence(
-              index, word.length()).toString(), token.getStartPos() + index, sentence));
 -             index, word.length()).toString(), token.getStartPos() + index, sentence, ruleMatches));
++              index, word.length()).toString(), token.getStartPos() + index, sentence, ruleMatches));
         }
       }
```

And the method signature:
```diff
-  protected List<RuleMatch> getRuleMatches(String word, int startPos, AnalyzedSentence sentence) throws IOException {
 - protected List<RuleMatch> getRuleMatches(String word, int startPos, AnalyzedSentence sentence, List<RuleMatch> ruleMatchesSoFar) throws IOException {
++  protected List<RuleMatch> getRuleMatches(String word, int startPos, AnalyzedSentence sentence, List<RuleMatch> ruleMatchesSoFar) throws IOException {
```

Also in `initSpeller`:
```diff
-      speller1 = new MorfologikMultiSpeller(binaryDict, plainTextDict, userConfig, 1);
-      speller2 = new MorfologikMultiSpeller(binaryDict, plainTextDict, userConfig, 2);
-      speller3 = new MorfologikMultiSpeller(binaryDict, plainTextDict, userConfig, 3);
 -     speller1 = new MorfologikMultiSpeller(binaryDict, plainTextDict, languageVariantPlainTextDict, userConfig, 1);
 -     speller2 = new MorfologikMultiSpeller(binaryDict, plainTextDict, languageVariantPlainTextDict, userConfig, 2);
 -     speller3 = new MorfologikMultiSpeller(binaryDict, plainTextDict, languageVariantPlainTextDict, userConfig, 3);
++      speller1 = new MorfologikMultiSpeller(binaryDict, plainTextDict, languageVariantPlainTextDict, userConfig, 1);
++      speller2 = new MorfologikMultiSpeller(binaryDict, plainTextDict, languageVariantPlainTextDict, userConfig, 2);
++      speller3 = new MorfologikMultiSpeller(binaryDict, plainTextDict, languageVariantPlainTextDict, userConfig, 3);
```

## Relevant final code in the merge

```java
protected List<RuleMatch> getRuleMatches(String word, int startPos, AnalyzedSentence sentence,
        List<RuleMatch> ruleMatchesSoFar) throws IOException {
    ...
    if (userConfig == null || userConfig.getMaxSpellingSuggestions() == 0
            || ruleMatchesSoFar.size() <= userConfig.getMaxSpellingSuggestions()) {
        ...
    } else {
        ruleMatch.setSuggestedReplacement(messages.getString("too_many_errors"));
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
8 lines (`++` for the 4 call sites updated to pass `ruleMatches` as the 4th argument, the method signature with the new parameter, and 3 constructor calls for `MorfologikMultiSpeller` with the additional `languageVariantPlainTextDict` argument).

## What each side had

- **Parent 1 (P1):** `getRuleMatches(String word, int startPos, AnalyzedSentence sentence)` — 3-parameter signature. `MorfologikMultiSpeller` constructor took 4 arguments (no `languageVariantPlainTextDict`).
- **Parent 2 (P2):** Added a 4th parameter `List<RuleMatch> ruleMatchesSoFar` to `getRuleMatches` to limit suggestions when too many errors exist (**Parameterize_Variable** → **Change_Parameter_Type** by adding a parameter). Also added `languageVariantPlainTextDict` to `MorfologikMultiSpeller` constructor (**Split_Parameter**).

## Interpretation

This case evidences a **Change_Parameter_Type** / parameter addition refactoring on `getRuleMatches`: P2 added a `List<RuleMatch> ruleMatchesSoFar` parameter to allow the method to short-circuit suggestion generation when many errors are found. This conflicts with P1's 3-parameter call sites. The `++` merge effort lines resolve the conflict at every call site by adopting P2's 4-argument signature. Similarly, the `MorfologikMultiSpeller` constructor conflict is resolved by adopting P2's version with `languageVariantPlainTextDict`. Both are well-supported by the diff evidence.

## Complete diff

*(See full diff in `languagetool_c7f12513db90c922230311acc08dbab2ec677885.diff`)*
