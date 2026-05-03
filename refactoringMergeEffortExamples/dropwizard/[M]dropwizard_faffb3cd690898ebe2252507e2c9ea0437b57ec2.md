# Case 3 — Project: dropwizard — Merge commit SHA1: faffb3cd690898ebe2252507e2c9ea0437b57ec2

## Modified file(s):
- `dropwizard-testing/src/main/java/com/codahale/dropwizard/testing/junit/ConfigOverride.java`
- `dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleConfigOverrideTest.java`
- `dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleTest.java`
- `dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/TestConfiguration.java`

## Class(es) modified in the merge:
- `ConfigOverride`
- `DropwizardServiceRuleConfigOverrideTest`
- `DropwizardServiceRuleTest`
- `TestConfiguration`

## Merge effort lines in the combined diff

```diff
diff --cc dropwizard-testing/src/main/java/com/codahale/dropwizard/testing/junit/ConfigOverride.java
@@@ -1,20 -1,0 +1,20 @@@
- package com.yammer.dropwizard.testing.junit;
++package com.codahale.dropwizard.testing.junit;
+
+ public class ConfigOverride { ... }

diff --cc dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleConfigOverrideTest.java
@@@ -1,28 -1,0 +1,27 @@@
- package com.yammer.dropwizard.testing.tests.junit;
++package com.codahale.dropwizard.testing.junit;
...
- import static com.yammer.dropwizard.testing.junit.ConfigOverride.config;
- import static com.yammer.dropwizard.testing.tests.junit.DropwizardServiceRuleTest.resourceFilePath;
++import static com.codahale.dropwizard.testing.junit.ConfigOverride.config;
++import static com.codahale.dropwizard.testing.junit.DropwizardServiceRuleTest.resourceFilePath;

diff --cc dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleTest.java
@@@ -1,9 -1,15 +1,8 @@@
- package com.yammer.dropwizard.testing.tests.junit;
+ package com.codahale.dropwizard.testing.junit;
...
@@@ -22,8 -30,8 +21,8 @@@
      @Test
      public void canGetExpectedResourceOverHttp() {
          final String content = new Client().resource("http://localhost:" +
-                 RULE.getLocalPort()
-                 + "/test").get(String.class);
 -                                                             RULE.getLocalPort()
 -                                                             +"/test").get(String.class);
++                                                     RULE.getLocalPort()
++                                                     +"/test").get(String.class);

diff --cc dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/TestConfiguration.java
@@@ -1,16 -1,0 +1,16 @@@
- package com.yammer.dropwizard.testing.tests.junit;
++package com.codahale.dropwizard.testing.junit;
+
++import com.codahale.dropwizard.Configuration;
+ import com.fasterxml.jackson.annotation.JsonProperty;
- import com.yammer.dropwizard.config.Configuration;
+ import org.hibernate.validator.constraints.NotEmpty;
+
+ public class TestConfiguration extends Configuration { ... }
```

## Relevant final code in the merge

```java
// ConfigOverride.java
package com.codahale.dropwizard.testing.junit;

public class ConfigOverride {
    private final String key;
    private final String value;

    private ConfigOverride(String key, String value) {
        this.key = key;
        this.value = value;
    }

    public static ConfigOverride config(String key, String value) {
        return new ConfigOverride(key, value);
    }

    public void addToSystemProperties() {
        System.setProperty("dw." + key, value);
    }
}

// TestConfiguration.java
package com.codahale.dropwizard.testing.junit;

import com.codahale.dropwizard.Configuration;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.hibernate.validator.constraints.NotEmpty;

public class TestConfiguration extends Configuration {
    @JsonProperty
    @NotEmpty
    private String message;

    public String getMessage() {
        return message;
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
8 lines

## What each side had

**Parent 1 (P1)** had the test classes located under the package `com.yammer.dropwizard.testing.junit` (or `com.yammer.dropwizard.testing.tests.junit`), with:
- `package com.yammer.dropwizard.testing.junit;` in `ConfigOverride.java`
- `package com.yammer.dropwizard.testing.tests.junit;` in test classes
- `import com.yammer.dropwizard.config.Configuration;` in `TestConfiguration`
- Static import `com.yammer.dropwizard.testing.junit.ConfigOverride.config`
- Static import `com.yammer.dropwizard.testing.tests.junit.DropwizardServiceRuleTest.resourceFilePath`

**Parent 2 (P2)** had moved all classes to the new `com.codahale.dropwizard.testing.junit` package, introducing:
- `package com.codahale.dropwizard.testing.junit;` across all affected files
- `import com.codahale.dropwizard.Configuration;`
- Updated static imports pointing to the new package

## Interpretation

**Refactoring type evidenced:** `Move_Class`

Parent 2 performed a surgical move of the `dropwizard-testing` JUnit helper classes from the `com.yammer.dropwizard` namespace to the `com.codahale.dropwizard` namespace. This is distinct from the broad `javax` → `jakarta` uniform migration seen in other commits, because:

1. It affects only a small, specific set of classes within a single module (`dropwizard-testing`)
2. The package move is from `com.yammer.*` to `com.codahale.*` — reflecting a specific project-level organisational refactoring (rebranding), not a dependency upgrade
3. The conflict is structural: P1 kept the old package declarations and import references, while P2 had moved them, creating direct conflicts on the `package` statement, import statements, and static import references in each file
4. The `++` lines confirm the merge chose P2's new package (`com.codahale.dropwizard.testing.junit`) and updated all cross-references accordingly (e.g., the static imports in `DropwizardServiceRuleConfigOverrideTest`)

The merge effort resolves these conflicts by adopting P2's new package declarations and updating all dependent references within each file.

## Complete diff

```diff
diff --cc dropwizard-testing/src/main/java/com/codahale/dropwizard/testing/junit/ConfigOverride.java
index 17c6d87dd7,0000000000..fda1fe252e
mode 100644,000000..100644
--- a/dropwizard-testing/src/main/java/com/codahale/dropwizard/testing/junit/ConfigOverride.java
+++ b/dropwizard-testing/src/main/java/com/codahale/dropwizard/testing/junit/ConfigOverride.java
@@@ -1,20 -1,0 +1,20 @@@
- package com.yammer.dropwizard.testing.junit;
++package com.codahale.dropwizard.testing.junit;
+
+public class ConfigOverride {
+
+    private final String key;
+    private final String value;
+
+    private ConfigOverride(String key, String value) {
+        this.key = key;
+        this.value = value;
+    }
+
+    public static ConfigOverride config(String key, String value) {
+        return new ConfigOverride(key, value);
+    }
+
+    public void addToSystemProperties() {
+        System.setProperty("dw." + key, value);
+    }
+}

diff --cc dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleConfigOverrideTest.java
index b5e13f9662,0000000000..626d120554
mode 100644,000000..100644
--- a/dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleConfigOverrideTest.java
+++ b/dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleConfigOverrideTest.java
@@@ -1,28 -1,0 +1,27 @@@
- package com.yammer.dropwizard.testing.tests.junit;
++package com.codahale.dropwizard.testing.junit;
+
+import com.sun.jersey.api.client.Client;
- import com.yammer.dropwizard.testing.junit.DropwizardServiceRule;
+import org.junit.ClassRule;
+import org.junit.Test;
+
- import static com.yammer.dropwizard.testing.junit.ConfigOverride.config;
- import static com.yammer.dropwizard.testing.tests.junit.DropwizardServiceRuleTest.resourceFilePath;
++import static com.codahale.dropwizard.testing.junit.ConfigOverride.config;
++import static com.codahale.dropwizard.testing.junit.DropwizardServiceRuleTest.resourceFilePath;
+import static org.hamcrest.core.Is.is;
+import static org.junit.Assert.assertThat;
+
+public class DropwizardServiceRuleConfigOverrideTest {
+
+    @ClassRule
+    public static final DropwizardServiceRule<TestConfiguration> RULE =
+            new DropwizardServiceRule<TestConfiguration>(TestService.class,
+                                                         resourceFilePath("test-config.yaml"),
+                                                         config("message", "A new way to say Hooray!"));
+
+    @Test
+    public void supportsConfigAttributeOverrides() {
+        final String content = new Client().resource("http://localhost:" + RULE.getLocalPort() + "/test")
+                                           .get(String.class);
+
+        assertThat(content, is("A new way to say Hooray!"));
+    }
+}

diff --cc dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleTest.java
index 98094bddc1,27f7d3a89c..77825bee72
--- a/dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleTest.java
+++ b/dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/DropwizardServiceRuleTest.java
@@@ -1,9 -1,15 +1,8 @@@
- package com.yammer.dropwizard.testing.tests.junit;
+ package com.codahale.dropwizard.testing.junit;
...
@@@ -22,8 -30,8 +21,8 @@@
     @Test
     public void canGetExpectedResourceOverHttp() {
         final String content = new Client().resource("http://localhost:" +
-                 RULE.getLocalPort()
-                 + "/test").get(String.class);
 -                                                             RULE.getLocalPort()
 -                                                             +"/test").get(String.class);
++                                                     RULE.getLocalPort()
++                                                     +"/test").get(String.class);
 
         assertThat(content, is("Yes, it's here"));
     }

diff --cc dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/TestConfiguration.java
index 76bdabe6eb,0000000000..507bece1d3
mode 100644,000000..100644
--- a/dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/TestConfiguration.java
+++ b/dropwizard-testing/src/test/java/com/codahale/dropwizard/testing/junit/TestConfiguration.java
@@@ -1,16 -1,0 +1,16 @@@
- package com.yammer.dropwizard.testing.tests.junit;
++package com.codahale.dropwizard.testing.junit;
+
++import com.codahale.dropwizard.Configuration;
+import com.fasterxml.jackson.annotation.JsonProperty;
- import com.yammer.dropwizard.config.Configuration;
+import org.hibernate.validator.constraints.NotEmpty;
+
+public class TestConfiguration extends Configuration {
+
+    @JsonProperty
+    @NotEmpty
+    private String message;
+
+    public String getMessage() {
+        return message;
+    }
+}
```
