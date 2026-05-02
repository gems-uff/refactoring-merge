# Case 1 — Project: flink — Merge commit SHA1: 5df886ecb32de2da6c6f68b93d0e8edbaab6489a

## Modified file(s):
- `nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/AbstractID.java`
- `nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/channels/DeserializationBuffer.java`
- `nephele/nephele-common/src/main/java/eu/stratosphere/nephele/jobgraph/JobID.java`

## Class(es) modified in the merge:
- `AbstractID` (formerly `ID` in Parent 2)
- `DeserializationBuffer`
- `JobID`

## Merge effort lines in the combined diff

### AbstractID — constructor and `setID` method

```diff
- 	public AbstractID(byte[] bytes) {
 -	public ID(final byte[] bytes) {
++	public AbstractID(final byte[] bytes) {
```

```diff
- 	public void setID(AbstractID src) {
 -	public void setID(final ID src) {
++	public void setID(final AbstractID src) {
```

### JobID — class declaration

```diff
- public class JobID extends AbstractID {
 -public final class JobID extends ID {
++public final class JobID extends AbstractID {
```

### DeserializationBuffer — `readData` method signature and body

```diff
- 	public T readData(T target, ReadableByteChannel readableByteChannel) throws IOException {
 -	public T readData(final ReadableByteChannel readableByteChannel) throws IOException {
++	public T readData(final T target, final ReadableByteChannel readableByteChannel) throws IOException {
```

```diff
- 		deserializationBuffer.reset(tempBuffer.array(), this.recordLength);
- 		final T record = deserializer.deserialize(target, deserializationBuffer);
 -		this.deserializationBuffer.reset(this.tempBuffer.array(), this.recordLength);
 -		final T record = deserializer.deserialize(this.deserializationBuffer);
++		this.deserializationBuffer.reset(tempBuffer.array(), this.recordLength);
++		final T record = deserializer.deserialize(target, this.deserializationBuffer);
```

## Relevant final code in the merge

```java
// AbstractID.java
public AbstractID(final byte[] bytes) {
    if(bytes.length == SIZE) {
        System.arraycopy(bytes, 0, this.bytes, 0, SIZE);
    }
}

public void setID(final AbstractID src) {
    setBytes(src.getBytes());
}

// JobID.java
public final class JobID extends AbstractID {
    ...
}

// DeserializationBuffer.java
public T readData(final T target, final ReadableByteChannel readableByteChannel) throws IOException {
    ...
    this.deserializationBuffer.reset(tempBuffer.array(), this.recordLength);
    final T record = deserializer.deserialize(target, this.deserializationBuffer);
    ...
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
6 lines (++ only; the -- are from the discarded parent lines)

## What each side had

**Parent 1 (P1)** had the class already renamed to `AbstractID`, with the constructor signature `public AbstractID(byte[] bytes)` (non-`final` parameter), and `setID(AbstractID src)` (non-`final` parameter). `JobID` extended `AbstractID`. `readData` took `(T target, ReadableByteChannel ...)` and used `deserializationBuffer` (field reference without `this`).

**Parent 2 (P2)** still used the old class name `ID`, with constructor `public ID(final byte[] bytes)` and `setID(final ID src)`. `JobID` extended `ID`. `readData` had a different, single-parameter signature `readData(final ReadableByteChannel ...)` with `deserializer.deserialize(this.deserializationBuffer)` (no `target` argument).

## Interpretation

**Rename_Class (`ID` → `AbstractID`):** P1 renamed the class from `ID` to `AbstractID` in `AbstractID.java` and updated `JobID` accordingly. P2 still used the old class name `ID` everywhere. The merge had to reconcile both the constructor name and the `setID` parameter type to use `AbstractID`, and fix `JobID`'s superclass declaration to `final class JobID extends AbstractID`. The ++ lines replacing the constructor and method signatures are direct merge effort caused by this rename conflict.

**Change_Parameter_Type / Split_Parameter in `DeserializationBuffer.readData`:** P1 added a `target` parameter to `readData`, making it `readData(T target, ReadableByteChannel ...)`. P2 removed the `target` parameter entirely, keeping only `readData(final ReadableByteChannel ...)`. The merge resolved this conflict by producing the combined signature `readData(final T target, final ReadableByteChannel ...)`, which also required adjusting the body to use `deserializer.deserialize(target, ...)` with `this.deserializationBuffer`. The four ++ body lines are merge effort caused by both sides independently modifying the method signature and the deserialization call.

Both cases are well-supported: the combined-diff notation unambiguously shows both parent contributions (` -` for P2, `- ` for P1) being discarded in favour of the merged `++` lines.

## Complete diff

```diff
diff --cc nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/AbstractID.java
index a83705dfdb5,551641f0bda..9095e2a2fa8
--- a/nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/AbstractID.java
+++ b/nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/AbstractID.java
@@@ -42,9 -42,9 +42,9 @@@ public abstract class AbstractID implem
  	/**
  	 * Constructs a new ID with a specific bytes value.
  	 */
- 	public AbstractID(byte[] bytes) {
 -	public ID(final byte[] bytes) {
 -
 -		if (bytes.length == SIZE) {
++	public AbstractID(final byte[] bytes) {
 +		
 +		if(bytes.length == SIZE) {
  		System.arraycopy(bytes, 0, this.bytes, 0, SIZE);
  		}
  	}
@@@ -93,7 -93,7 +93,7 @@@
  	 * @param src
  	 *        the source ID
  	 */
- 	public void setID(AbstractID src) {
 -	public void setID(final ID src) {
++	public void setID(final AbstractID src) {
  		setBytes(src.getBytes());
  	}

@@@ -101,9 -101,9 +101,9 @@@
  	 * {@inheritDoc}
  	 */
  	@Override
- 	public boolean equals(Object obj) {
+ 	public boolean equals(final Object obj) {

 -		if (!(obj instanceof ID)) {
 +		if (!(obj instanceof AbstractID)) {
  			return false;
  		}

diff --cc nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/channels/DeserializationBuffer.java
index efdfeb9fb1e,f73722da856..ad21366396f
--- a/nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/channels/DeserializationBuffer.java
+++ b/nephele/nephele-common/src/main/java/eu/stratosphere/nephele/io/channels/DeserializationBuffer.java
@@@ -89,7 -89,7 +89,7 @@@ public class DeserializationBuffer<T ex
  	 * @throws IOException
  	 *         thrown if an error occurs while reading the data or deserializing the object
  	 */
- 	public T readData(T target, ReadableByteChannel readableByteChannel) throws IOException {
 -	public T readData(final ReadableByteChannel readableByteChannel) throws IOException {
++	public T readData(final T target, final ReadableByteChannel readableByteChannel) throws IOException {

  		if (this.recordLength < 0) {
  			if (readableByteChannel.read(this.lengthBuf) == -1 && this.propagateEndOfStream) {
@@@ -129,8 -129,8 +129,8 @@@
  			return null;
  		}

- 		deserializationBuffer.reset(tempBuffer.array(), this.recordLength);
- 		final T record = deserializer.deserialize(target, deserializationBuffer);
 -		this.deserializationBuffer.reset(this.tempBuffer.array(), this.recordLength);
 -		final T record = deserializer.deserialize(this.deserializationBuffer);
++		this.deserializationBuffer.reset(tempBuffer.array(), this.recordLength);
++		final T record = deserializer.deserialize(target, this.deserializationBuffer);

  		this.recordLength = -1;
  		this.lengthBuf.clear();

diff --cc nephele/nephele-common/src/main/java/eu/stratosphere/nephele/jobgraph/JobID.java
index df1377557ad,2682cfb201b..1a17fe66d43
--- a/nephele/nephele-common/src/main/java/eu/stratosphere/nephele/jobgraph/JobID.java
+++ b/nephele/nephele-common/src/main/java/eu/stratosphere/nephele/jobgraph/JobID.java
@@@ -23,7 -23,7 +23,7 @@@ import eu.stratosphere.nephele.io.Abstr
   * 
   * @author warneke
   */
- public class JobID extends AbstractID {
 -public final class JobID extends ID {
++public final class JobID extends AbstractID {
  	/**
  	 * Constructs a new random ID from a uniform distribution.
  	 */
```
