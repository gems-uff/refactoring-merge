# Case 2 — Project: antlr4 — Merge commit SHA1: c2b49bd94eb0d186584765294ed87f91cf9e8daf

## Modified file(s):
`runtime/Java/src/org/antlr/v4/runtime/atn/LexerATNSimulator.java`

## Class(es) modified in the merge:
`LexerATNSimulator`

## Merge effort lines in the combined diff

```diff
@@@ -474,52 -595,67 +614,55 @@@

 -	public void deleteWildcardConfigsForAlt(@NotNull ATNConfigSet closure, int ci, int alt) {
 +	/** Delete configs for alt following ci. Closure is unmodified; copy returned. */
 +	public ATNConfigSet deleteWildcardConfigsForAlt(@NotNull ATNConfigSet closure, int ci, int alt) {
 +		ATNConfigSet dup = new ATNConfigSet(closure);
  		int j=ci+1;
 -		while ( j<closure.size() ) {
 -			ATNConfig c = closure.get(j);
 -			boolean isWildcard = c.state.getClass() == ATNState.class &&
 -				c.state.transition(0).getClass() == WildcardTransition.class;
 +		while ( j < dup.size() ) {
 +			ATNConfig c = dup.get(j);
 +			boolean isWildcard = c.state.getClass() == ATNState.class && // plain state only, not rulestop etc..
 +				c.state.transition(0) instanceof WildcardTransition;
```

```diff
 		ATNState p = config.state;
 -		ATNConfig c;
 
 +		LexerATNConfig c = null;
-		if ( t.getClass() == RuleTransition.class ) {
-			PredictionContext newContext =
-				new SingletonPredictionContext(config.context, p.stateNumber);
-			c = new LexerATNConfig(config, t.target, newContext);
+		switch (t.getSerializationType()) {
-		case Transition.RULE:
-			RuleContext newContext =
-				new RuleContext(config.context, p.stateNumber);
-			c = new ATNConfig(config, t.target, newContext);
-			break;
		...
++		case Transition.RULE:
++			PredictionContext newContext =
++				new SingletonPredictionContext(config.context, p.stateNumber);
++			c = new LexerATNConfig(config, t.target, newContext);
++			break;
++		case Transition.PREDICATE:
++			...
++			c = new LexerATNConfig(config, t.target, pt.getPredicate());
++			break;
++		case Transition.ACTION:
++			c = new LexerATNConfig(config, t.target, ((ActionTransition)t).actionIndex);
++			break;
++		case Transition.EPSILON:
++			c = new LexerATNConfig(config, t.target);
++			break;
```

## Relevant final code in the merge

```java
/** Delete configs for alt following ci. Closure is unmodified; copy returned. */
public ATNConfigSet deleteWildcardConfigsForAlt(@NotNull ATNConfigSet closure, int ci, int alt) {
    ATNConfigSet dup = new ATNConfigSet(closure);
    int j = ci + 1;
    while ( j < dup.size() ) {
        ATNConfig c = dup.get(j);
        boolean isWildcard = c.state.getClass() == ATNState.class &&
            c.state.transition(0) instanceof WildcardTransition;
        if ( c.alt == alt && isWildcard ) { ... }
        else j++;
    }
    ...
}

// getEpsilonTarget:
LexerATNConfig c = null;
switch (t.getSerializationType()) {
    case Transition.RULE:
        PredictionContext newContext =
            new SingletonPredictionContext(config.context, p.stateNumber);
        c = new LexerATNConfig(config, t.target, newContext);
        break;
    case Transition.PREDICATE:
        ...
        c = new LexerATNConfig(config, t.target, pt.getPredicate());
        break;
    case Transition.ACTION:
        c = new LexerATNConfig(config, t.target, ((ActionTransition)t).actionIndex);
        break;
    case Transition.EPSILON:
        c = new LexerATNConfig(config, t.target);
        break;
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
More than 20 lines (++ and --)

## What each side had

**Parent 1 (lexer specialization branch):**
Introduced a specialized `LexerATNConfig` class and adapted `getEpsilonTarget` to use it, with a switch-based dispatch (`switch (t.getSerializationType())`). The method `deleteWildcardConfigsForAlt` operated on a local `dup` copy and returned `ATNConfigSet`. P1 had:
```
+ public ATNConfigSet deleteWildcardConfigsForAlt(...) {
+     ATNConfigSet dup = new ATNConfigSet(closure);
+     ...
+     LexerATNConfig c = null;
+     switch (t.getSerializationType()) { ... }
```

**Parent 2 (base/general branch):**
Kept the original `void` return type and the older `if-else` chain based on `instanceof` checks, using generic `ATNConfig` and `RuleContext`. P2 had:
```
- public void deleteWildcardConfigsForAlt(...) {
-     while ( j<closure.size() ) { ... }
-     ATNConfig c;
-     if ( t.getClass() == RuleTransition.class ) {
-         RuleContext newContext = new RuleContext(...);
-         c = new ATNConfig(config, t.target, newContext);
-     } else if ( t.getClass() == PredicateTransition.class ) { ... }
```

## Interpretation

This case evidences two related refactoring types in one merge conflict:

**Change_Return_Type** on `deleteWildcardConfigsForAlt`: Parent 1 changed the return type from `void` to `ATNConfigSet` (returning a modified copy rather than mutating in place). Parent 2 still had `void`. The merge resolved the conflict by adopting the new signature from P1, generating `--` on the `void` line and `++` on the `ATNConfigSet` line, plus `++` for the `ATNConfigSet dup = new ATNConfigSet(closure)` initialization.

**Rename_Attribute / Replace_Attribute** on the local variable `c` in `getEpsilonTarget`: Parent 1 replaced the generic `ATNConfig c` with the more specific `LexerATNConfig c = null`, and simultaneously replaced the `if-else instanceof` chain with a `switch` on `t.getSerializationType()`, replacing `new ATNConfig(...)` and `new RuleContext(...)` with `new LexerATNConfig(...)` and `new SingletonPredictionContext(...)`. The merge preserved the P1 version, producing many `++` lines for the new switch cases and `--` for the old if-else chain.

Both refactorings were introduced in P1 as part of a systematic specialization of `LexerATNSimulator` to use `LexerATNConfig` throughout. The conflict arose because P2 independently modified the same method region. The case is well-supported by the volume and specificity of the `++`/`--` lines.

## Complete diff

```diff
diff --cc runtime/Java/src/org/antlr/v4/runtime/atn/LexerATNSimulator.java
@@@ -481,34 -474,52 +484,54 @@@

   		case SET:
   			...
   		}
   	}

 -	public void deleteWildcardConfigsForAlt(@NotNull ATNConfigSet closure, int ci, int alt) {
 +	/** Delete configs for alt following ci. Closure is unmodified; copy returned. */
 +	public ATNConfigSet deleteWildcardConfigsForAlt(@NotNull ATNConfigSet closure, int ci, int alt) {
 +		ATNConfigSet dup = new ATNConfigSet(closure);
  		int j=ci+1;
 -		while ( j<closure.size() ) {
 -			ATNConfig c = closure.get(j);
 -			boolean isWildcard = c.state.getClass() == ATNState.class &&
 -				c.state.transition(0).getClass() == WildcardTransition.class;
 +		while ( j < dup.size() ) {
 +			ATNConfig c = dup.get(j);
 +			boolean isWildcard = c.state.getClass() == ATNState.class &&
 +				c.state.transition(0) instanceof WildcardTransition;
  			if ( c.alt == alt && isWildcard ) {
  				...
  			}
  		}
  	}

@@@ -591,52 -595,67 +614,55 @@@
  	{
  		ATNState p = config.state;
 -		ATNConfig c;

 +		LexerATNConfig c = null;
-		if ( t.getClass() == RuleTransition.class ) {
-			PredictionContext newContext =
-				new SingletonPredictionContext(config.context, p.stateNumber);
-			c = new LexerATNConfig(config, t.target, newContext);
+		switch (t.getSerializationType()) {
-		case Transition.RULE:
-			RuleContext newContext =
-				new RuleContext(config.context, p.stateNumber);
-			c = new ATNConfig(config, t.target, newContext);
-			break;
-		case Transition.PREDICATE:
-			...
-			c = new ATNConfig(config, t.target, pt.getPredicate());
-			break;
-		case Transition.ACTION:
-			c = new ATNConfig(config, t.target);
-			c.lexerActionIndex = ((ActionTransition)t).actionIndex;
-			break;
-		case Transition.EPSILON:
-			c = new ATNConfig(config, t.target);
-			break;
++		case Transition.RULE:
++			PredictionContext newContext =
++				new SingletonPredictionContext(config.context, p.stateNumber);
++			c = new LexerATNConfig(config, t.target, newContext);
++			break;
++		case Transition.PREDICATE:
++			...
++			c = new LexerATNConfig(config, t.target, pt.getPredicate());
++			break;
++		case Transition.ACTION:
++			c = new LexerATNConfig(config, t.target, ((ActionTransition)t).actionIndex);
++			break;
++		case Transition.EPSILON:
++			c = new LexerATNConfig(config, t.target);
++			break;
  		}
-		else if ( t.getClass() == PredicateTransition.class ) { ... }
  	}
```
