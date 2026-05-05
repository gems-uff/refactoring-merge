# Project: RxJava — Merge commit SHA1: f189a985fb955a79bed03b927e6b46934cdaa8df

## Modified file(s):
- `rxjava-core/src/main/java/rx/operators/OperationRepeat.java`
- `rxjava-core/src/test/java/rx/ObservableTests.java`

## Class(es) modified in the merge:
- `OperationRepeat<T>`

## Merge effort lines in the combined diff

```diff
// OperationRepeat.java — onSubscribe method body

 +    @Override
 +    public Subscription onSubscribe(final Observer<? super T> observer) {
 -        final MultipleAssignmentSubscription subscription = new MultipleAssignmentSubscription();
 -        subscription.setSubscription(scheduler.schedule(new Action1<Action0>() {
++        final CompositeSubscription compositeSubscription = new CompositeSubscription();
++        final MultipleAssignmentSubscription innerSubscription = new MultipleAssignmentSubscription();
++        compositeSubscription.add(innerSubscription);
++        compositeSubscription.add(scheduler.schedule(new Action1<Action0>() {
 +             @Override
 +             public void call(final Action0 self) {
 -                subscription.setSubscription(source.subscribe(new Observer<T>() {
++                innerSubscription.set(source.subscribe(new Observer<T>() {
 +                     [...]
 +                 }));
 +             }
 +         }));
 -        return subscription;
++        return compositeSubscription;
 +    }

// factory method — raw type fix:
 -        return new OperationRepeat(source, scheduler);
++        return new OperationRepeat<T>(source, scheduler);

// ObservableTests.java — Move_Class for schedulers:
 -import rx.concurrency.Schedulers;
 -import rx.concurrency.TestScheduler;
++import rx.schedulers.Schedulers;
++import rx.schedulers.TestScheduler;
```

## Relevant final code in the merge

```java
// OperationRepeat.java
@Override
public Subscription onSubscribe(final Observer<? super T> observer) {
    final CompositeSubscription compositeSubscription = new CompositeSubscription();
    final MultipleAssignmentSubscription innerSubscription = new MultipleAssignmentSubscription();
    compositeSubscription.add(innerSubscription);
    compositeSubscription.add(scheduler.schedule(new Action1<Action0>() {
        @Override
        public void call(final Action0 self) {
            innerSubscription.set(source.subscribe(new Observer<T>() {
                @Override
                public void onCompleted() { self.call(); }
                @Override
                public void onError(Throwable error) { observer.onError(error); }
                @Override
                public void onNext(T value) { observer.onNext(value); }
            }));
        }
    }));
    return compositeSubscription;
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
10 lines (`++`), covering: 3 new variable declarations/usages, 2 changed method calls, 1 return statement change, 1 generic-type fix in factory method, and 2 import changes.

## What each side had

**Parent 1** had `OperationRepeat.onSubscribe(...)` using a single `MultipleAssignmentSubscription subscription` variable that tracked both the scheduler subscription and the inner source subscription via repeated `setSubscription(...)` calls. The factory method had a raw type `new OperationRepeat(...)`.

**Parent 2** split the single subscription variable into two: a `CompositeSubscription compositeSubscription` (the return value, holding both) and a `MultipleAssignmentSubscription innerSubscription` (tracking only the source subscription). It also moved the scheduler package from `rx.concurrency` to `rx.schedulers`.

## Interpretation

### Split_Variable

This is a textbook **Split_Variable** case: the single variable `subscription` (of type `MultipleAssignmentSubscription`) in Parent 1 was split in Parent 2 into two semantically distinct variables:
- `compositeSubscription` — the outer composite returned to the caller
- `innerSubscription` — the inner handle to the source subscription

The `++` lines confirm the merge introduced all three declarations (`compositeSubscription`, `innerSubscription`, and `compositeSubscription.add(innerSubscription)`) plus the updated call site (`innerSubscription.set(...)`) and return statement (`return compositeSubscription`), while the ` -` lines show the discarded single-variable pattern. This is merge effort directly caused by P2's split-variable refactoring conflicting with P1's single-variable version of the same method.

### Move_Class (Schedulers)

The `++` import lines in `ObservableTests.java` (`rx.schedulers.Schedulers`, `rx.schedulers.TestScheduler`) replacing the ` -` imports (`rx.concurrency.Schedulers`, `rx.concurrency.TestScheduler`) confirm a **Move_Class** refactoring applied in Parent 2, moving scheduler classes from the `rx.concurrency` package to `rx.schedulers`. These are surgical, file-specific changes (not a bulk migration pattern), indicating a genuine package rename/move that required merge effort.

## Complete diff

```diff
diff --cc rxjava-core/src/main/java/rx/operators/OperationRepeat.java
index 0000000000,6bf34efa78..8bdff97776
mode 000000,100644..100644
--- a/rxjava-core/src/main/java/rx/operators/OperationRepeat.java
+++ b/rxjava-core/src/main/java/rx/operators/OperationRepeat.java
@@@ -1,0 -1,68 +1,71 @@@
+ public class OperationRepeat<T> implements Observable.OnSubscribeFunc<T> {
+
+     public static <T> Observable.OnSubscribeFunc<T> repeat(Observable<T> source, Scheduler scheduler) {
 -        return new OperationRepeat(source, scheduler);
++        return new OperationRepeat<T>(source, scheduler);
+     }
+
+     @Override
+     public Subscription onSubscribe(final Observer<? super T> observer) {
 -        final MultipleAssignmentSubscription subscription = new MultipleAssignmentSubscription();
 -        subscription.setSubscription(scheduler.schedule(new Action1<Action0>() {
++        final CompositeSubscription compositeSubscription = new CompositeSubscription();
++        final MultipleAssignmentSubscription innerSubscription = new MultipleAssignmentSubscription();
++        compositeSubscription.add(innerSubscription);
++        compositeSubscription.add(scheduler.schedule(new Action1<Action0>() {
+             @Override
+             public void call(final Action0 self) {
 -                subscription.setSubscription(source.subscribe(new Observer<T>() {
++                innerSubscription.set(source.subscribe(new Observer<T>() {
+                     [...]
+                 }));
+             }
+         }));
 -        return subscription;
++        return compositeSubscription;
+     }
+ }

diff --cc rxjava-core/src/test/java/rx/ObservableTests.java
index b02afea164,dcf0fe678b..cd5a985104
--- a/rxjava-core/src/test/java/rx/ObservableTests.java
+++ b/rxjava-core/src/test/java/rx/ObservableTests.java
@@@ -33,17 -20,13 +33,17 @@@
  import rx.Observable.OnSubscribeFunc;
- import rx.schedulers.TestScheduler;
 -import rx.concurrency.Schedulers;
 -import rx.concurrency.TestScheduler;
  import rx.observables.ConnectableObservable;
++import rx.schedulers.Schedulers;
++import rx.schedulers.TestScheduler;
```
