# Case 1 — Project: dropwizard — Merge commit SHA1: 2d67da4cade8ee71be720a65efe4a03c5bff868d

## Modified file(s):
- `dropwizard-example/src/test/java/com/example/helloworld/resources/PersonResourceTest.java`

## Class(es) modified in the merge:
- `PersonResourceTest`

## Merge effort lines in the combined diff

```diff
@@@ -1,0 -1,56 +1,60 @@@
+ package com.example.helloworld.resources;
+ ...
-    private static final PersonDAO dao = mock(PersonDAO.class);
-
++    private static final PersonDAO DAO = mock(PersonDAO.class);
+     @ClassRule
-    public static final ResourceTestRule resources = ResourceTestRule.builder()
-            .addResource(new PersonResource(dao))
++    public static final ResourceTestRule RULE = ResourceTestRule.builder()
++            .addResource(new PersonResource(DAO))
+             .build();
...
+     @After
+     public void tearDown() {
-        reset(dao);
++        reset(DAO);
+     }
+
+     @Test
-    public void getPerson_success() {
-        when(dao.findById(1L)).thenReturn(Optional.of(person));
++    public void getPersonSuccess() {
++        when(DAO.findById(1L)).thenReturn(Optional.of(person));

-        Person found = resources.client().resource("/people/1").get(Person.class);
-        assertThat(found.getId()).isEqualTo(person.getId());
++        Person found = RULE.client().target("/people/1").request().get(Person.class);

-        verify(dao).findById(1L);
++        assertThat(found.getId()).isEqualTo(person.getId());
++        verify(DAO).findById(1L);
+     }

-    @Test(expected = UniformInterfaceException.class)
-    public void getPerson_404() {
-        when(dao.findById(2L)).thenReturn(Optional.<Person>absent());
-        resources.client().resource("/people/2").get(Person.class);
++    @Test
++    public void getPersonNotFound() {
++        when(DAO.findById(2L)).thenReturn(Optional.<Person>absent());
++        final Response response = RULE.client().target("/people/2").request().get();

-        verify(dao).findById(2L);
++        assertThat(response.getStatusInfo()).isEqualTo(Response.Status.NOT_FOUND);
++        verify(DAO).findById(2L);
+     }
```

## Relevant final code in the merge

```java
public class PersonResourceTest {
    private static final PersonDAO DAO = mock(PersonDAO.class);

    @ClassRule
    public static final ResourceTestRule RULE = ResourceTestRule.builder()
            .addResource(new PersonResource(DAO))
            .build();

    private Person person;

    @Before
    public void setup() {
        person = new Person();
        person.setId(1L);
    }

    @After
    public void tearDown() {
        reset(DAO);
    }

    @Test
    public void getPersonSuccess() {
        when(DAO.findById(1L)).thenReturn(Optional.of(person));

        Person found = RULE.client().target("/people/1").request().get(Person.class);

        assertThat(found.getId()).isEqualTo(person.getId());
        verify(DAO).findById(1L);
    }

    @Test
    public void getPersonNotFound() {
        when(DAO.findById(2L)).thenReturn(Optional.<Person>absent());
        final Response response = RULE.client().target("/people/2").request().get();

        assertThat(response.getStatusInfo()).isEqualTo(Response.Status.NOT_FOUND);
        verify(DAO).findById(2L);
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
14 lines

## What each side had

**Parent 1 (P1)** had the original version of `PersonResourceTest`, which used:
- `private static final PersonDAO dao = mock(PersonDAO.class);` (lowercase `dao`)
- `public static final ResourceTestRule resources = ResourceTestRule.builder()` (named `resources`)
- Test methods named `getPerson_success()` and `getPerson_404()`
- References to `dao` and `resources` throughout
- Used the old Jersey 1.x client API (`resources.client().resource(...)`)

**Parent 2 (P2)** had a rewritten version of `PersonResourceTest` that introduced:
- `private static final PersonDAO DAO = mock(PersonDAO.class);` (uppercase `DAO`)
- `public static final ResourceTestRule RULE = ResourceTestRule.builder()` (renamed to `RULE`)
- Test methods renamed to `getPersonSuccess()` and `getPersonNotFound()`
- References updated from `dao`/`resources` to `DAO`/`RULE`
- Used the new Jersey 2.x client API (`RULE.client().target(...)`)

## Interpretation

**Refactoring types evidenced:** `Rename_Attribute`, `Rename_Method`

Two distinct refactorings occurred in Parent 2 prior to the merge:

1. **`Rename_Attribute`**: The static field `dao` was renamed to `DAO` (following Java constant naming conventions for `static final` fields), and `resources` was renamed to `RULE`. These renames propagated to all usage sites within the class, causing conflicts at every reference point. The merge effort (`++` lines) shows the resolution: adopting the P2 naming (`DAO`, `RULE`) while integrating the new client API code from P2.

2. **`Rename_Method`**: The test methods `getPerson_success()` and `getPerson_404()` were renamed in P2 to `getPersonSuccess()` and `getPersonNotFound()` respectively (switching from underscore to camelCase convention). The merge had to reconcile these renamed methods while preserving and integrating the new assertion logic.

The `++` lines confirm the merge effort: the final merged code adopts the new names (`DAO`, `RULE`, `getPersonSuccess`, `getPersonNotFound`) while also integrating the new assertions and the Jersey 2.x client invocations. These conflicts were directly triggered by the systematic renaming performed in P2 before the merge.

## Complete diff

```diff
diff --cc dropwizard-example/src/test/java/com/example/helloworld/resources/PersonResourceTest.java
index 0000000000,e975041aae..a23f2f94d1
mode 000000,100644..100644
--- a/dropwizard-example/src/test/java/com/example/helloworld/resources/PersonResourceTest.java
+++ b/dropwizard-example/src/test/java/com/example/helloworld/resources/PersonResourceTest.java
@@@ -1,0 -1,56 +1,60 @@@
+ package com.example.helloworld.resources;
+ 
+ import com.example.helloworld.core.Person;
+ import com.example.helloworld.db.PersonDAO;
+ import com.google.common.base.Optional;
-import com.sun.jersey.api.client.UniformInterfaceException;
+ import io.dropwizard.testing.junit.ResourceTestRule;
+ import org.junit.After;
+ import org.junit.Before;
+ import org.junit.ClassRule;
+ import org.junit.Test;
+ 
-import static org.fest.assertions.api.Assertions.assertThat;
-import static org.mockito.Mockito.*;
++import javax.ws.rs.core.Response;
++
++import static org.assertj.core.api.Assertions.assertThat;
++import static org.mockito.Mockito.mock;
++import static org.mockito.Mockito.reset;
++import static org.mockito.Mockito.verify;
++import static org.mockito.Mockito.when;
+ 
+ /**
+  * Unit tests for {@link PersonResource}.
+  */
+ public class PersonResourceTest {
-    private static final PersonDAO dao = mock(PersonDAO.class);
-
++    private static final PersonDAO DAO = mock(PersonDAO.class);
+     @ClassRule
-    public static final ResourceTestRule resources = ResourceTestRule.builder()
-            .addResource(new PersonResource(dao))
++    public static final ResourceTestRule RULE = ResourceTestRule.builder()
++            .addResource(new PersonResource(DAO))
+             .build();
+     private Person person;
+ 
+     @Before
+     public void setup() {
+         person = new Person();
+         person.setId(1L);
+     }
+ 
+     @After
+     public void tearDown() {
-        reset(dao);
++        reset(DAO);
+     }
+ 
+     @Test
-    public void getPerson_success() {
-        when(dao.findById(1L)).thenReturn(Optional.of(person));
++    public void getPersonSuccess() {
++        when(DAO.findById(1L)).thenReturn(Optional.of(person));
+ 
-        Person found = resources.client().resource("/people/1").get(Person.class);
-        assertThat(found.getId()).isEqualTo(person.getId());
++        Person found = RULE.client().target("/people/1").request().get(Person.class);
+ 
-        verify(dao).findById(1L);
++        assertThat(found.getId()).isEqualTo(person.getId());
++        verify(DAO).findById(1L);
+     }
+ 
-    @Test(expected = UniformInterfaceException.class)
-    public void getPerson_404() {
-        when(dao.findById(2L)).thenReturn(Optional.<Person>absent());
-        resources.client().resource("/people/2").get(Person.class);
++    @Test
++    public void getPersonNotFound() {
++        when(DAO.findById(2L)).thenReturn(Optional.<Person>absent());
++        final Response response = RULE.client().target("/people/2").request().get();
+ 
-        verify(dao).findById(2L);
++        assertThat(response.getStatusInfo()).isEqualTo(Response.Status.NOT_FOUND);
++        verify(DAO).findById(2L);
+     }
+ }
```
