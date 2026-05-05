# Project: byte-buddy — Merge commit SHA1: 5db8c3cc386e85cd1da28d4f7fe714f2c0d51879

## Modified file(s):
- `byte-buddy-dep/src/main/java/net/bytebuddy/description/method/ParameterDescription.java`
- `byte-buddy-dep/src/main/java/net/bytebuddy/description/method/ParameterList.java`

## Class(es) modified in the merge:
`ParameterDescription.ForLoadedParameter.OfMethod`, `ParameterDescription.ForLoadedParameter.OfConstructor`, `ParameterDescription.ForLoadedParameter.OfLegacyVmMethod`, `ParameterDescription.ForLoadedParameter.OfLegacyVmConstructor`

## Merge effort lines in the combined diff

```diff
@@@ ParameterDescription.java — OfMethod (modern VM) @@@

 +            @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfMethodParameter(executable, index, executable.getParameterTypes()[index]);
++            public TypeDescription.Generic getType() {
++                return new TypeDescription.Generic.LazyProjection.OfMethodParameter(executable, index, executable.getParameterTypes()[index]);
             }

@@@ ParameterDescription.java — OfConstructor (modern VM) @@@

 +            @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfConstructorParameter(executable, index, executable.getParameterTypes()[index]);
++            public TypeDescription.Generic getType() {
++                return new TypeDescription.Generic.LazyProjection.OfConstructorParameter(executable, index, executable.getParameterTypes()[index]);
             }

@@@ ParameterDescription.java — OfLegacyVmMethod (legacy VM) @@@

             @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfMethodParameter(method, index, parameterType);
 +            public TypeDescription.Generic getType() {
-                 return new TypeDescription.Generic.LazyProjection.ForLoadedParameter.OfLegacyVmMethod(method, index, parameterType);
++                return new TypeDescription.Generic.LazyProjection.OfMethodParameter(method, index, parameterType);
             }

@@@ ParameterDescription.java — OfLegacyVmConstructor (legacy VM) @@@

             @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfConstructorParameter(constructor, index, parameterType);
 +            public TypeDescription.Generic getType() {
-                 return new TypeDescription.Generic.LazyProjection.ForLoadedParameter.OfLegacyVmConstructor(constructor, index, parameterType);
++                return new TypeDescription.Generic.LazyProjection.OfConstructorParameter(constructor, index, parameterType);
             }
```

```diff
@@@ ParameterList.java — Dispatcher interface and ForModernVm @@@

 +            /**
 -             * Describes a {@link Method}'s parameters of the given VM.
 +             * Describes a {@link Constructor}'s parameters of the given VM.
              ...
 -            ParameterList<ParameterDescription.InDefinedShape> describe(Method method);
 +            ParameterList<ParameterDescription.InDefinedShape> describe(Constructor<?> constructor);

 +            /**
++             * Describes a {@link Method}'s parameters of the given VM.
              ...
++            ParameterList<ParameterDescription.InDefinedShape> describe(Method method);

                 @Override
 -                public ParameterList<ParameterDescription.InDefinedShape> describe(Constructor<?> constructor) {
 -                    return new OfLegacyVmConstructor(constructor);
++                public ParameterList<ParameterDescription.InDefinedShape> describe(Constructor<?> constructor) {
++                    return new OfLegacyVmConstructor(constructor);

                 @Override
 -                public ParameterList<ParameterDescription.InDefinedShape> describe(Method method) {
 -                    return new OfLegacyVmMethod(method);
++                public ParameterList<ParameterDescription.InDefinedShape> describe(Method method) {
++                    return new OfLegacyVmMethod(method);
```

## Relevant final code in the merge

```java
// ParameterDescription.ForLoadedParameter.OfMethod (modern VM)
@Override
public TypeDescription.Generic getType() {
    return new TypeDescription.Generic.LazyProjection.OfMethodParameter(
        executable, index, executable.getParameterTypes()[index]);
}

// ParameterDescription.ForLoadedParameter.OfLegacyVmMethod (legacy VM)
@Override
public TypeDescription.Generic getType() {
    return new TypeDescription.Generic.LazyProjection.OfMethodParameter(
        method, index, parameterType);
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
25 lines (19 `++` + 6 `--`)

## What each side had

**Parent 1 (generic type system refactoring branch):**
Renamed the type system from a flat `GenericTypeDescription` hierarchy to a nested `TypeDescription.Generic` hierarchy. The `getType()` method in all `ParameterDescription` implementations was changed to return `TypeDescription.Generic` instead of `GenericTypeDescription`. The inner class `TypeDescription.LazyProjection.OfMethodParameter` was moved/renamed to `TypeDescription.Generic.LazyProjection.OfMethodParameter`. P1 had:
```
- public GenericTypeDescription getType() {
- return new TypeDescription.LazyProjection.OfMethodParameter(...)
```

**Parent 2 (parameter API refactoring branch):**
Added `OfMethod` and `OfConstructor` inner classes to `ForLoadedParameter` for modern VMs and reorganized `ForLoadedExecutable`. P2 still used `GenericTypeDescription` as the return type and introduced a different path `TypeDescription.Generic.LazyProjection.ForLoadedParameter.OfLegacyVmMethod`. P2 had:
```
+ public TypeDescription.Generic getType() {
+     return new TypeDescription.Generic.LazyProjection.ForLoadedParameter.OfLegacyVmMethod(...)
```

## Interpretation

This case evidences a **Change_Return_Type** refactoring on the `getType()` method across all `ParameterDescription` implementations. Parent 1 renamed the return type from `GenericTypeDescription` to `TypeDescription.Generic` as part of a systematic restructuring of the generic type hierarchy. Parent 2 independently restructured the `ForLoadedParameter` class hierarchy (introducing `OfMethod`/`OfConstructor`) and used an intermediate inner class path `TypeDescription.Generic.LazyProjection.ForLoadedParameter.OfLegacyVmMethod` for the legacy VM case.

The merge had to reconcile both: for the modern VM cases (`OfMethod`, `OfConstructor`), the `++` lines adopt P1's return type (`TypeDescription.Generic`) with the new inner class path. For the legacy VM cases, the `++` lines resolve the conflict between P2's deeper inner path (`ForLoadedParameter.OfLegacyVmMethod`) and P1's flatter structure (`OfMethodParameter`), landing on P1's path. The `--` lines discard P1's old `GenericTypeDescription` return type declarations that conflicted with P2's new overriding implementations. The conflict is surgical and specific to the return type of `getType()` across exactly these four inner classes.

## Complete diff

```diff
diff --cc byte-buddy-dep/src/main/java/net/bytebuddy/description/method/ParameterDescription.java
index 433481026e7,62783df3bec..cbe3c050916
@@@ -521,6 -449,68 +455,68 @@@

             @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfMethodParameter(executable, index, executable.getParameterTypes()[index]);
++            public TypeDescription.Generic getType() {
++                return new TypeDescription.Generic.LazyProjection.OfMethodParameter(executable, index, executable.getParameterTypes()[index]);
             }

             @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfConstructorParameter(executable, index, executable.getParameterTypes()[index]);
++            public TypeDescription.Generic getType() {
++                return new TypeDescription.Generic.LazyProjection.OfConstructorParameter(executable, index, executable.getParameterTypes()[index]);
             }

@@@ -563,8 -553,8 +559,8 @@@
             @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfMethodParameter(method, index, parameterType);
 +            public TypeDescription.Generic getType() {
-                 return new TypeDescription.Generic.LazyProjection.ForLoadedParameter.OfLegacyVmMethod(method, index, parameterType);
++                return new TypeDescription.Generic.LazyProjection.OfMethodParameter(method, index, parameterType);

@@@ -635,8 -625,8 +631,8 @@@
             @Override
 -            public GenericTypeDescription getType() {
 -                return new TypeDescription.LazyProjection.OfConstructorParameter(constructor, index, parameterType);
 +            public TypeDescription.Generic getType() {
-                 return new TypeDescription.Generic.LazyProjection.ForLoadedParameter.OfLegacyVmConstructor(constructor, index, parameterType);
++                return new TypeDescription.Generic.LazyProjection.OfConstructorParameter(constructor, index, parameterType);
```
