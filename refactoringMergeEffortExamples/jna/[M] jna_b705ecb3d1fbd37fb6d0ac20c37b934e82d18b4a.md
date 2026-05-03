# Case 1 — Project: jna — Merge commit SHA1: b705ecb3d1fbd37fb6d0ac20c37b934e82d18b4a

## Modified file(s):
- `contrib/platform/src/com/sun/jna/platform/win32/Advapi32.java`
- `contrib/platform/src/com/sun/jna/platform/win32/Winsvc.java`

## Class(es) modified in the merge:
- `ChangeServiceConfig2Info` (moved from `Advapi32` to `Winsvc`)

## Merge effort lines in the combined diff

### Winsvc.java — `Move_Class`: `ChangeServiceConfig2Info` now declared inside `Winsvc`

```diff
 // Winsvc.java — import removed since class now lives here
 -import com.sun.jna.platform.win32.Advapi32.ChangeServiceConfig2Info;
  import com.sun.jna.Memory;
+ import com.sun.jna.Pointer;
  import com.sun.jna.Structure;

 ...

@@@ -199,6 -204,123 +201,128 @@@
++    public abstract class ChangeServiceConfig2Info extends Structure {
++        public ChangeServiceConfig2Info() {
++            super();
++        }
++
++        public ChangeServiceConfig2Info(Pointer p) {
++            super(p);
++        }
++    }

+     public class SERVICE_FAILURE_ACTIONS extends ChangeServiceConfig2Info {
          ...
+     }

+     public class SERVICE_FAILURE_ACTIONS_FLAG extends ChangeServiceConfig2Info {
          ...
+     }
```

### Advapi32.java — `Move_Class`: `ChangeServiceConfig2Info` definition removed from `Advapi32`

```diff
 // Advapi32.java — class definition removed
 -    public static abstract class ChangeServiceConfig2Info extends Structure {
 -        public ChangeServiceConfig2Info() {
 -            super();
 -        }
 -
 -        public ChangeServiceConfig2Info(Pointer p) {
 -            super(p);
 -        }
 -
 -        public ChangeServiceConfig2Info(TypeMapper mapper) {
 -            super(mapper);
 -        }
 -
 -        public ChangeServiceConfig2Info(Pointer p, int alignType, TypeMapper mapper) {
 -            super(p, alignType, mapper);
 -        }
 -    }
```

### Advapi32.java — `ChangeServiceConfig2` method now references `Winsvc.ChangeServiceConfig2Info` (via `++`)

```diff
++    public boolean ChangeServiceConfig2(SC_HANDLE hService, int dwInfoLevel,
++                                        ChangeServiceConfig2Info lpInfo);
```

*(The merged `Advapi32.java` still uses the unqualified `ChangeServiceConfig2Info` since `Winsvc` is imported; the call site now refers to the class in its new home.)*

## Relevant final code in the merge

```java
// Winsvc.java — ChangeServiceConfig2Info now lives here
public interface Winsvc {
    ...
    public abstract class ChangeServiceConfig2Info extends Structure {
        public ChangeServiceConfig2Info() {
            super();
        }

        public ChangeServiceConfig2Info(Pointer p) {
            super(p);
        }
    }

    // Subclasses that were already in Winsvc now extend it directly:
    public class SERVICE_FAILURE_ACTIONS extends ChangeServiceConfig2Info {
        public int dwResetPeriod;
        public String lpRebootMsg;
        public String lpCommand;
        public int cActions;
        public SC_ACTION.ByReference lpsaActions;

        public SERVICE_FAILURE_ACTIONS() {}
        public SERVICE_FAILURE_ACTIONS(Pointer p) { super(p); read(); }

        protected List getFieldOrder() {
            return Arrays.asList(new String[] {
                "dwResetPeriod", "lpRebootMsg", "lpCommand", "cActions", "lpsaActions"
            });
        }
    }
}

// Advapi32.java — method still uses ChangeServiceConfig2Info (now from Winsvc)
public interface Advapi32 extends StdCallLibrary {
    ...
    public boolean ChangeServiceConfig2(SC_HANDLE hService, int dwInfoLevel,
                                        ChangeServiceConfig2Info lpInfo);
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**~18 lines** (++ for the new `ChangeServiceConfig2Info` declaration in `Winsvc`, removal of old constructors with `TypeMapper` parameter, and the `--` for its complete definition in `Advapi32`, plus the removed import in `Winsvc`)

## What each side had

**Parent 1 (P1)** had `ChangeServiceConfig2Info` declared as `public static abstract class ChangeServiceConfig2Info extends Structure` inside `Advapi32`. It had four constructors: a no-arg, a `Pointer` constructor, a `TypeMapper` constructor, and a `Pointer + int + TypeMapper` constructor. `Winsvc.java` imported it via `import com.sun.jna.platform.win32.Advapi32.ChangeServiceConfig2Info;` and contained `SERVICE_FAILURE_ACTIONS` and `SERVICE_FAILURE_ACTIONS_FLAG` as its subclasses.

**Parent 2 (P2)** had already moved `ChangeServiceConfig2Info` into `Winsvc` as a non-static `public abstract class`, retaining only the no-arg and `Pointer` constructors (dropping the `TypeMapper` and `Pointer+int+TypeMapper` constructors). The import `Advapi32.ChangeServiceConfig2Info` in `Winsvc` was removed. The `Advapi32` interface lost its `ChangeServiceConfig2Info` inner class definition entirely.

## Interpretation

This is a clear **Move_Class** refactoring. `ChangeServiceConfig2Info` was moved from `Advapi32` to `Winsvc`, where it logically belongs since its only subclasses (`SERVICE_FAILURE_ACTIONS`, `SERVICE_FAILURE_ACTIONS_FLAG`, `SC_ACTION`) are all declared inside `Winsvc`.

The evidence is strong:
- The `--` lines confirm P2 had `ChangeServiceConfig2Info` fully defined in `Advapi32` as a `static` inner class with 4 constructors.
- The `++` lines show the class redeclared in `Winsvc` as a non-static inner abstract class with only 2 constructors (the `TypeMapper`-based constructors were dropped, consistent with the move and the related `Rename_Method` refactoring in `Structure` that changed how type mappers are provided).
- The import statement `import com.sun.jna.platform.win32.Advapi32.ChangeServiceConfig2Info;` in `Winsvc` is removed (`--` in `Winsvc.java`), because the class is now locally defined.
- The `ChangeServiceConfig2` method call in `Advapi32` still references `ChangeServiceConfig2Info` unqualified, now resolving to `Winsvc.ChangeServiceConfig2Info` through the interface inheritance chain.

The also-changed `static` modifier (`public static abstract` → `public abstract`) is consistent with the Move_Class: as an inner class of a top-level `interface`, `static` is implicit and not required.

## Complete diff

```diff
diff --cc contrib/platform/src/com/sun/jna/platform/win32/Advapi32.java
index 7820917a7,ae436d3e2..d4c243aa6
--- a/contrib/platform/src/com/sun/jna/platform/win32/Advapi32.java
+++ b/contrib/platform/src/com/sun/jna/platform/win32/Advapi32.java
@@@ -48,1718 -47,1737 +49,1773 @@@
-- public interface Advapi32 extends StdCallLibrary {
--     Advapi32 INSTANCE = (Advapi32) Native.loadLibrary("Advapi32",
--             Advapi32.class, W32APIOptions.DEFAULT_OPTIONS);
--     ...
 -    public static abstract class ChangeServiceConfig2Info extends Structure {
 -        public ChangeServiceConfig2Info() {
 -            super();
 -        }
 -        public ChangeServiceConfig2Info(Pointer p) {
 -            super(p);
 -        }
 -        public ChangeServiceConfig2Info(TypeMapper mapper) {
 -            super(mapper);
 -        }
--
 -        public ChangeServiceConfig2Info(Pointer p, int alignType, TypeMapper mapper) {
 -            super(p, alignType, mapper);
 -        }
 -    }
++    /**
++     * Encrypts a file or directory. ...
++     */
++    public boolean EncryptFile(String lpFileName);
...
++    public boolean ChangeServiceConfig2(SC_HANDLE hService, int dwInfoLevel,
++                                        ChangeServiceConfig2Info lpInfo);

diff --cc contrib/platform/src/com/sun/jna/platform/win32/Winsvc.java
index cc3407793,b730a66c1..ebc89df1e
--- a/contrib/platform/src/com/sun/jna/platform/win32/Winsvc.java
+++ b/contrib/platform/src/com/sun/jna/platform/win32/Winsvc.java
@@@ -16,9 -16,14 +16,11 @@@
  import java.util.Arrays;
  import java.util.List;

 -import com.sun.jna.platform.win32.Advapi32.ChangeServiceConfig2Info;
  import com.sun.jna.Memory;
+ import com.sun.jna.Pointer;
  import com.sun.jna.Structure;
+ import com.sun.jna.TypeMapper;
  import com.sun.jna.platform.win32.WinNT.HANDLE;
 -import com.sun.jna.win32.StdCallLibrary;
 -import com.sun.jna.win32.W32APITypeMapper;

@@@ -199,6 -204,123 +201,128 @@@ public interface Winsvc
         }
     }

++    public abstract class ChangeServiceConfig2Info extends Structure {
++        public ChangeServiceConfig2Info() {
++            super();
++        }
++
++        public ChangeServiceConfig2Info(Pointer p) {
++            super(p);
++        }
++    }

+     public class SERVICE_FAILURE_ACTIONS extends ChangeServiceConfig2Info {
+         public static class ByReference extends SERVICE_FAILURE_ACTIONS implements Structure.ByReference {}
+         public int dwResetPeriod;
+         public String lpRebootMsg;
+         public String lpCommand;
+         public int cActions;
+         public SC_ACTION.ByReference lpsaActions;

+         public SERVICE_FAILURE_ACTIONS() {}
+         public SERVICE_FAILURE_ACTIONS(Pointer p) {
 -            super(p, Structure.ALIGN_DEFAULT, getTypeMapper());
++            super(p);
+             read();
+         }

+         protected List getFieldOrder() {
+             return Arrays.asList(new String[] {
+                 "dwResetPeriod", "lpRebootMsg", "lpCommand", "cActions", "lpsaActions"
+             });
+         }
+     }

+     public class SERVICE_FAILURE_ACTIONS_FLAG extends ChangeServiceConfig2Info {
          ...
+     }
```
