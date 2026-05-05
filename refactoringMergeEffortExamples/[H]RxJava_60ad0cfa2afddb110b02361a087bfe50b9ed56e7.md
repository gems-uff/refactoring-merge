# Project: RxJava — Merge commit SHA1: 60ad0cfa2afddb110b02361a087bfe50b9ed56e7

## Modified file(s):
- `rxjava-core/src/main/java/rx/operators/OperationRefCount.java`

## Class(es) modified in the merge:
- `OperationRefCount<T>`
- `RefCount<T>` (inner class)

## Merge effort lines in the combined diff

```diff
// OperationRefCount.java

// Return type of factory method:
-     public static <T> Func1<Observer<T>, Subscription> refCount(ConnectableObservable<T> connectableObservable) {
++    public static <T> Observable.OnSubscribeFunc<T> refCount(ConnectableObservable<T> connectableObservable) {
         return new RefCount<T>(connectableObservable);
     }

// Inner class implements clause:
-     private static class RefCount<T> implements Func1<Observer<T>, Subscription> {
++    private static class RefCount<T> implements Observable.OnSubscribeFunc<T> {

// Override method name and observer type:
-         public Subscription call(Observer<T> observer) {
++        public Subscription onSubscribe(Observer<? super T> observer) {

// Structural indentation of inner UnitTest (closing brace relocation):
-     }
-
-     @RunWith(JUnit4.class)
-     public static class UnitTest {
-         @Before
-         public void setUp() { ... }
-         @Test public void subscriptionToUnderlyingOnFirstSubscription() { ... }
-         @Test public void noSubscriptionToUnderlyingOnSecondSubscription() { ... }
-         @Test public void unsubscriptionFromUnderlyingOnLastUnsubscription() { ... }
-         @Test public void noUnsubscriptionFromUnderlyingOnFirstUnsubscription() { ... }
-     }
- }
++        @RunWith(JUnit4.class)
++        public static class UnitTest {
++            @Before
++            public void setUp() { ... }
++            @Test public void subscriptionToUnderlyingOnFirstSubscription() { ... }
++            [all test methods re-indented as ++]
++        }
++    }
++}
```

## Relevant final code in the merge

```java
public final class OperationRefCount<T> {

    public static <T> Observable.OnSubscribeFunc<T> refCount(
            ConnectableObservable<T> connectableObservable) {
        return new RefCount<T>(connectableObservable);
    }

    private static class RefCount<T> implements Observable.OnSubscribeFunc<T> {
        private final ConnectableObservable<T> innerConnectableObservable;
        private final Object gate = new Object();
        private int count = 0;
        private Subscription connection = null;

        public RefCount(ConnectableObservable<T> innerConnectableObservable) {
            this.innerConnectableObservable = innerConnectableObservable;
        }

        @Override
        public Subscription onSubscribe(Observer<? super T> observer) {
            final Subscription subscription = innerConnectableObservable.subscribe(observer);
            synchronized (gate) {
                if (count++ == 0) {
                    connection = innerConnectableObservable.connect();
                }
            }
            return Subscriptions.create(new Action0() { ... });
        }

        @RunWith(JUnit4.class)
        public static class UnitTest { ... }
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
~70 lines (`++`), covering the 3 direct refactoring-driven changes plus the structural re-indentation of the `UnitTest` inner class that was forced by the structural change.

## What each side had

**Parent 1** had `OperationRefCount.RefCount<T>` implementing `Func1<Observer<T>, Subscription>` with an override method named `call(Observer<T> observer)`. The `UnitTest` was a sibling class of `RefCount` (at the same nesting level inside `OperationRefCount`).

**Parent 2** introduced the new `Observable.OnSubscribeFunc<T>` interface to replace the raw `Func1<Observer<T>, Subscription>` pattern across all operators, renaming the method from `call` to `onSubscribe` and widening the observer to `Observer<? super T>`. It also nested `UnitTest` inside `RefCount`.

## Interpretation

Three refactoring types are evidenced, all from **Parent 2**:

1. **Change_Return_Type** (`Func1<Observer<T>, Subscription>` → `Observable.OnSubscribeFunc<T>`): The factory method `refCount(...)` and the `implements` clause of `RefCount<T>` were changed to use the new dedicated interface. The `++` lines at both locations confirm the merge had to adopt this type.

2. **Rename_Method** (`call` → `onSubscribe`): The sole method of the `OnSubscribeFunc` interface is `onSubscribe`, replacing the previous `Func1.call`. The `++` line for `public Subscription onSubscribe(Observer<? super T> observer)` directly confirms this, with the ` -` line showing `call(Observer<T> observer)` being discarded.

3. **Change_Parameter_Type** (`Observer<T>` → `Observer<? super T>`): Combined with the rename, the observer parameter was widened to use the covariant bound. This appears on the `++` method signature line.

The ~70 `++` lines for the `UnitTest` re-indentation are a structural consequence of nesting the test class inside `RefCount` (as P2 had it), confirming that the class-level structural refactoring from P2 also required merge effort to reconcile with the file layout from P1.

## Complete diff

```diff
diff --cc rxjava-core/src/main/java/rx/operators/OperationRefCount.java
index 3c64397094,0000000000..b814512a11
mode 100644,000000..100644
--- a/rxjava-core/src/main/java/rx/operators/OperationRefCount.java
+++ b/rxjava-core/src/main/java/rx/operators/OperationRefCount.java
@@@ -1,148 -1,0 +1,147 @@@
 +public final class OperationRefCount<T> {
-     public static <T> Func1<Observer<T>, Subscription> refCount(ConnectableObservable<T> connectableObservable) {
++    public static <T> Observable.OnSubscribeFunc<T> refCount(ConnectableObservable<T> connectableObservable) {
 +        return new RefCount<T>(connectableObservable);
 +    }
 +
-     private static class RefCount<T> implements Func1<Observer<T>, Subscription> {
++    private static class RefCount<T> implements Observable.OnSubscribeFunc<T> {
 +        [fields...]
 +
 +        @Override
-         public Subscription call(Observer<T> observer) {
++        public Subscription onSubscribe(Observer<? super T> observer) {
 +            [body unchanged...]
 +        }
-     }
 +
-     @RunWith(JUnit4.class)
-     public static class UnitTest {
-         @Before
-         public void setUp() { MockitoAnnotations.initMocks(this); }
-         @Test public void subscriptionToUnderlyingOnFirstSubscription() { ... }
-         @Test public void noSubscriptionToUnderlyingOnSecondSubscription() { ... }
-         @Test public void unsubscriptionFromUnderlyingOnLastUnsubscription() { ... }
-         @Test public void noUnsubscriptionFromUnderlyingOnFirstUnsubscription() { ... }
-     }
- }
++        @RunWith(JUnit4.class)
++        public static class UnitTest {
++            @Before
++            public void setUp() { MockitoAnnotations.initMocks(this); }
++            @Test public void subscriptionToUnderlyingOnFirstSubscription() { ... }
++            @Test public void noSubscriptionToUnderlyingOnSecondSubscription() { ... }
++            @Test public void unsubscriptionFromUnderlyingOnLastUnsubscription() { ... }
++            @Test public void noUnsubscriptionFromUnderlyingOnFirstUnsubscription() { ... }
++        }
++    }
++}
```
