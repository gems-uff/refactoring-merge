# Project: byte-buddy — Merge commit SHA1: d2ca5cf77202d709c337a430a347940a678e66a3

## Modified file(s):
- `byte-buddy-dep/src/main/java/net/bytebuddy/dynamic/loading/MultipleParentClassLoader.java`

## Class(es) modified in the merge:
`MultipleParentClassLoader.Builder`

## Merge effort lines in the combined diff

```diff
@@@ MultipleParentClassLoader.java @@@

- import static net.bytebuddy.utility.ByteBuddyCommons.joinUnique;
++import static net.bytebuddy.utility.ByteBuddyCommons.filterUnique;

         /**
          * @param classLoaders The class loaders to collected.
          * @return A new builder instance with the additional class loaders.
          */
         public Builder append(List<? extends ClassLoader> classLoaders) {
-             return new Builder(joinUnique(this.classLoaders, classLoaders));
++            return new Builder(filterUnique(this.classLoaders, classLoaders));
         }
```

## Relevant final code in the merge

```java
import static net.bytebuddy.utility.ByteBuddyCommons.filterUnique;

// ...

public class MultipleParentClassLoader extends ClassLoader {

    // ...

    public static class Builder {

        private final List<? extends ClassLoader> classLoaders;

        private Builder(List<? extends ClassLoader> classLoaders) {
            this.classLoaders = classLoaders;
        }

        public Builder append(List<? extends ClassLoader> classLoaders) {
            return new Builder(filterUnique(this.classLoaders, classLoaders));
        }
        // ...
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
2 lines (2 `++`, 0 `--`)

## What each side had

**Parent 1 (utility method rename branch):**
Renamed `joinUnique` to `filterUnique` in `ByteBuddyCommons` to better reflect the method's semantics (it filters duplicates, not just joins). The import and all call sites were updated. P1 had:
```
- import static net.bytebuddy.utility.ByteBuddyCommons.joinUnique;
- return new Builder(joinUnique(this.classLoaders, classLoaders));
```

**Parent 2 (MultipleParentClassLoader addition branch):**
Added the `MultipleParentClassLoader` class as a new file, including its `Builder` inner class. P2 was independently developed and still used the old name `joinUnique`. P2 had:
```
+ import static net.bytebuddy.utility.ByteBuddyCommons.joinUnique;
+ return new Builder(joinUnique(this.classLoaders, classLoaders));
```

## Interpretation

This case evidences a **Rename_Method** refactoring: `joinUnique` was renamed to `filterUnique` in Parent 1. Parent 2 introduced the `MultipleParentClassLoader` class (new file) and independently used the old method name `joinUnique`. The merge conflict arose because both parents modified the same import and call site: P2 added the file using `joinUnique`, and P1 renamed the utility method to `filterUnique`. The merge resolution produced two `++` lines — the updated import and the updated call site — that directly reflect the propagation of the rename into the newly added class. The case is surgical and specific: exactly the import statement and the single call site within `Builder.append()` are affected.

## Complete diff

```diff
diff --cc byte-buddy-dep/src/main/java/net/bytebuddy/dynamic/loading/MultipleParentClassLoader.java
index 6a571f3545c,00000000000..994d8afb89e
mode 100644,000000..100644
@@@ -1,274 -1,0 +1,274 @@@
- import static net.bytebuddy.utility.ByteBuddyCommons.joinUnique;
++import static net.bytebuddy.utility.ByteBuddyCommons.filterUnique;

         public Builder append(List<? extends ClassLoader> classLoaders) {
-             return new Builder(joinUnique(this.classLoaders, classLoaders));
++            return new Builder(filterUnique(this.classLoaders, classLoaders));
         }
```
