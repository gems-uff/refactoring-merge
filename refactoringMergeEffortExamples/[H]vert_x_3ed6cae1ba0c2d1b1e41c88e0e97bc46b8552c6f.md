# Project: vert_x — Merge commit SHA1: 3ed6cae1ba0c2d1b1e41c88e0e97bc46b8552c6f

## Modified file(s):
- `src/main/java/io/vertx/core/http/HttpClientOptions.java`
- `src/main/java/io/vertx/core/http/HttpServerOptions.java`
- `src/main/generated/io/vertx/core/http/HttpClientOptionsConverter.java`
- `src/main/generated/io/vertx/core/http/HttpServerOptionsConverter.java`
- `src/main/java/io/vertx/core/http/impl/ConnectionManager.java`
- `src/main/java/io/vertx/core/http/impl/HttpServerImpl.java`
- `src/test/java/io/vertx/test/core/Http1xTest.java`
- `src/main/asciidoc/dataobjects.adoc`

## Class(es) modified in the merge:
- `HttpClientOptions`
- `HttpServerOptions`
- `HttpClientOptionsConverter`
- `HttpServerOptionsConverter`

## Merge effort lines in the combined diff

### `HttpClientOptions.java` — Rename_Attribute and Rename_Method

P1 introduced the feature with attribute name `initialBufferSizeHttpDecoder` and getter/setter `getInitialBufferSizeHttpDecoder()` / `setInitialBufferSizeHttpDecoder()`.  
P2 renamed the attribute and constant to `decoderInitialBufferSize` / `DEFAULT_DECODER_INITIAL_BUFFER_SIZE` and the methods to `getDecoderInitialBufferSize()` / `setDecoderInitialBufferSize()`.  
The merge had to reconcile: it applied the P2 naming while keeping the full implementation:

```diff
 +  public static final boolean DEFAULT_FORCE_SNI = false;
 +
+   /**
+    * Default initial buffer size for HttpObjectDecoder = 128 bytes
+    */
-  public static final int DEFAULT_INITIAL_BUFFER_SIZE_HTTP_DECODER = 128;
-
++  public static final int DEFAULT_DECODER_INITIAL_BUFFER_SIZE = 128;
```

```diff
 +  private boolean forceSni;
++  private int decoderInitialBufferSize;
```

```diff
 +    this.forceSni = other.forceSni;
++    this.decoderInitialBufferSize = other.getDecoderInitialBufferSize();
```

```diff
 +    forceSni = DEFAULT_FORCE_SNI;
++    decoderInitialBufferSize = DEFAULT_DECODER_INITIAL_BUFFER_SIZE;
```

```diff
-  public int getInitialBufferSizeHttpDecoder() { return initialBufferSizeHttpDecoder; }
++  public int getDecoderInitialBufferSize() { return decoderInitialBufferSize; }
```

```diff
-  public HttpClientOptions setInitialBufferSizeHttpDecoder(int initialBufferSizeHttpDecoder) {
-    Arguments.require(initialBufferSizeHttpDecoder > 0, "initialBufferSizeHttpDecoder must be > 0");
-    this.initialBufferSizeHttpDecoder = initialBufferSizeHttpDecoder;
++  public HttpClientOptions setDecoderInitialBufferSize(int decoderInitialBufferSize) {
++    Arguments.require(decoderInitialBufferSize > 0, "initialBufferSizeHttpDecoder must be > 0");
++    this.decoderInitialBufferSize = decoderInitialBufferSize;
```

```diff
-    if (initialBufferSizeHttpDecoder != that.initialBufferSizeHttpDecoder) return false;
++    if (decoderInitialBufferSize != that.decoderInitialBufferSize) return false;
```

```diff
-    result = 31 * result + initialBufferSizeHttpDecoder;
++    result = 31 * result + decoderInitialBufferSize;
```

### `HttpServerOptions.java` — same Rename_Attribute / Rename_Method pattern

```diff
-  public static final int DEFAULT_INITIAL_BUFFER_SIZE_HTTP_DECODER = 128;
++  public static final int DEFAULT_DECODER_INITIAL_BUFFER_SIZE = 128;

 -  private int initialBufferSizeHttpDecoder;
++  private int decoderInitialBufferSize;

 -    this.initialBufferSizeHttpDecoder = other.getInitialBufferSizeHttpDecoder();
++    this.decoderInitialBufferSize = other.getDecoderInitialBufferSize();

 -    initialBufferSizeHttpDecoder = DEFAULT_INITIAL_BUFFER_SIZE_HTTP_DECODER;
++    decoderInitialBufferSize = DEFAULT_DECODER_INITIAL_BUFFER_SIZE;

 -  public int getInitialBufferSizeHttpDecoder() { return initialBufferSizeHttpDecoder; }
++  public int getDecoderInitialBufferSize() { return decoderInitialBufferSize; }

 -  public HttpServerOptions setInitialBufferSizeHttpDecoder(int initialBufferSizeHttpDecoder) {
 -    Arguments.require(initialBufferSizeHttpDecoder > 0, ...);
 -    this.initialBufferSizeHttpDecoder = initialBufferSizeHttpDecoder;
++  public HttpServerOptions setDecoderInitialBufferSize(int decoderInitialBufferSize) {
++    Arguments.require(decoderInitialBufferSize > 0, ...);
++    this.decoderInitialBufferSize = decoderInitialBufferSize;

 -    if (initialBufferSizeHttpDecoder != that.initialBufferSizeHttpDecoder) return false;
++    if (decoderInitialBufferSize != that.decoderInitialBufferSize) return false;

 -    result = 31 * result + initialBufferSizeHttpDecoder;
++    result = 31 * result + decoderInitialBufferSize;
```

### `ConnectionManager.java` — call site update

```diff
-              options.getMaxChunkSize(), false, false, options.getInitialBufferSizeHttpDecoder()));
++              options.getMaxChunkSize(), false, false, options.getDecoderInitialBufferSize()));
```

### `HttpServerImpl.java` — call site update

```diff
-        , options.getMaxHeaderSize(), options.getMaxChunkSize(), false, options.getInitialBufferSizeHttpDecoder()));
++        , options.getMaxHeaderSize(), options.getMaxChunkSize(), false, options.getDecoderInitialBufferSize()));
```

### `Http1xTest.java` — test references updated

```diff
-    assertEquals(HttpClientOptions.DEFAULT_INITIAL_BUFFER_SIZE_HTTP_DECODER, options.getInitialBufferSizeHttpDecoder());
-    assertEquals(options, options.setInitialBufferSizeHttpDecoder(256));
-    assertEquals(256, options.getInitialBufferSizeHttpDecoder());
-    assertIllegalArgumentException(() -> options.setInitialBufferSizeHttpDecoder(-1));
++    assertEquals(HttpClientOptions.DEFAULT_DECODER_INITIAL_BUFFER_SIZE, options.getDecoderInitialBufferSize());
++    assertEquals(options, options.setDecoderInitialBufferSize(256));
++    assertEquals(256, options.getDecoderInitialBufferSize());
++    assertIllegalArgumentException(() -> options.setDecoderInitialBufferSize(-1));

...

-    assertEquals(HttpServerOptions.DEFAULT_INITIAL_BUFFER_SIZE_HTTP_DECODER, options.getInitialBufferSizeHttpDecoder());
-    assertEquals(options, options.setInitialBufferSizeHttpDecoder(256));
++    assertEquals(HttpServerOptions.DEFAULT_DECODER_INITIAL_BUFFER_SIZE, options.getDecoderInitialBufferSize());
++    assertEquals(options, options.setDecoderInitialBufferSize(256));

 -    int initialSizeBufferHttpDecoder = TestUtils.randomPositiveInt();
++    int decoderInitialBufferSize = TestUtils.randomPositiveInt();

 -    options.setInitialBufferSizeHttpDecoder(initialSizeBufferHttpDecoder);
++    options.setDecoderInitialBufferSize(decoderInitialBufferSize);

 -    assertEquals(def.getInitialBufferSizeHttpDecoder(), json.getInitialBufferSizeHttpDecoder());
++    assertEquals(def.getDecoderInitialBufferSize(), json.getDecoderInitialBufferSize());

 -      .put("initialBufferSizeHttpDecoder", initialBufferSizeHttpDecoder);
++      .put("decoderInitialBufferSize", decoderInitialBufferSize);

 -    assertEquals(initialBufferSizeHttpDecoder, options.getInitialBufferSizeHttpDecoder());
++    assertEquals(decoderInitialBufferSize, options.getDecoderInitialBufferSize());
```

### `HttpClientOptionsConverter.java` / `HttpServerOptionsConverter.java` — generated converters updated

```diff
++    if (json.getValue("decoderInitialBufferSize") instanceof Number) {
++      obj.setDecoderInitialBufferSize(((Number)json.getValue("decoderInitialBufferSize")).intValue());
++    }
...
++    json.put("decoderInitialBufferSize", obj.getDecoderInitialBufferSize());
```

## Relevant final code in the merge

```java
// HttpClientOptions.java
public static final int DEFAULT_DECODER_INITIAL_BUFFER_SIZE = 128;
private int decoderInitialBufferSize;

public int getDecoderInitialBufferSize() { return decoderInitialBufferSize; }

public HttpClientOptions setDecoderInitialBufferSize(int decoderInitialBufferSize) {
  Arguments.require(decoderInitialBufferSize > 0, "initialBufferSizeHttpDecoder must be > 0");
  this.decoderInitialBufferSize = decoderInitialBufferSize;
  return this;
}

// HttpServerOptions.java — identical pattern
public static final int DEFAULT_DECODER_INITIAL_BUFFER_SIZE = 128;
private int decoderInitialBufferSize;
// ... same getter/setter
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**~40 lines** (`++` and `--` across `HttpClientOptions`, `HttpServerOptions`, their converters, `ConnectionManager`, `HttpServerImpl`, and `Http1xTest`)

## What each side had

**Parent 1 (P1):** Introduced the feature using the name `initialBufferSizeHttpDecoder` for both the field (`private int initialBufferSizeHttpDecoder`) and the API (`getInitialBufferSizeHttpDecoder()` / `setInitialBufferSizeHttpDecoder()`), and `DEFAULT_INITIAL_BUFFER_SIZE_HTTP_DECODER` for the constant.

**Parent 2 (P2):** Renamed the attribute to `decoderInitialBufferSize`, the constant to `DEFAULT_DECODER_INITIAL_BUFFER_SIZE`, and the getter/setter to `getDecoderInitialBufferSize()` / `setDecoderInitialBufferSize()`. P2 also added `forceSni` and `DEFAULT_FORCE_SNI` as an independent feature in `HttpClientOptions`.

## Interpretation

This is a clear **Rename_Attribute** + **Rename_Method** case. P1 introduced the feature under one naming convention (`initialBufferSizeHttpDecoder`), while P2 renamed it to follow a different convention (`decoderInitialBufferSize`). The conflict arose because both parents modified the same files and the same fields/methods.

The merge effort (`++` and `--` lines) is the direct reconciliation of those two naming schemes: the `--` lines eliminate the P1 naming from definition, call sites, tests, and generated converters, while the `++` lines establish the P2 naming everywhere. The consistent pattern across `HttpClientOptions`, `HttpServerOptions`, both converter files, `ConnectionManager`, `HttpServerImpl`, and test files confirms this is a genuine, surgical rename — not a broad namespace migration — making it a strong and defensible case.

## Complete diff

```diff
diff --cc src/main/asciidoc/dataobjects.adoc
[... full raw diff content as provided in the input file ...]
```
