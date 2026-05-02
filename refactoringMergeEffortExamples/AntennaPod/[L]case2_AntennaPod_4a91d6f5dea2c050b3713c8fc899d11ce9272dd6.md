# Case 2 — Project: AntennaPod — Merge commit SHA1: 4a91d6f5dea2c050b3713c8fc899d11ce9272dd6

## Modified file(s):
- `core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedParserTask.java`
- `core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedSyncTask.java`
- `app/src/main/java/de/danoeh/antennapod/activity/OnlineFeedViewActivity.java`

## Class(es) modified in the merge:
- `FeedParserTask`
- `FeedSyncTask`
- `OnlineFeedViewActivity`

## Merge effort lines in the combined diff

```diff
// FeedParserTask.java — DownloadStatus constructor call change
++import java.util.Date;

      public FeedParserTask(DownloadRequest request) {
          this.request = request;
 -        downloadStatus = new DownloadStatus(request, DownloadError.ERROR_REQUEST_ERROR,
 -                false, false, "Unknown error: Status not set");
++        downloadStatus = new DownloadStatus(
++        0, request.getTitle(), 0, request.getFeedfileType(), false,
++                false, true, DownloadError.ERROR_REQUEST_ERROR, new Date(),
++                "Unknown error: Status not set", request.isInitiatedByUser());
      }

// FeedSyncTask.java — Move_Class of DownloadStatus
 -import de.danoeh.antennapod.core.service.download.DownloadStatus;
 +import de.danoeh.antennapod.model.download.DownloadStatus;

// OnlineFeedViewActivity.java — Move_Class of DownloadError
 -import de.danoeh.antennapod.core.util.DownloadError;
 +import de.danoeh.antennapod.model.download.DownloadError;
```

## Relevant final code in the merge

```java
// FeedParserTask.java
import java.util.Date;
// ...
downloadStatus = new DownloadStatus(
    0, request.getTitle(), 0, request.getFeedfileType(), false,
    false, true, DownloadError.ERROR_REQUEST_ERROR, new Date(),
    "Unknown error: Status not set", request.isInitiatedByUser());

// FeedSyncTask.java
import de.danoeh.antennapod.model.download.DownloadStatus;

// OnlineFeedViewActivity.java
import de.danoeh.antennapod.model.download.DownloadError;
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
5 lines

## What each side had

**Parent 1 (P1)** changed the `DownloadStatus` constructor signature from a short form accepting a `DownloadRequest` object plus a few fields, to an expanded explicit form requiring individual fields including `id`, `title`, `feedfileId`, `feedfileType`, `successful`, `cancelled`, `initiatedByUser`, `reason`, `completionDate`, `reasonDetailed`. This is a **Change_Parameter_Type** / constructor signature expansion. P1 also moved `DownloadStatus` and `DownloadError` from `de.danoeh.antennapod.core.*` to `de.danoeh.antennapod.model.download.*` (**Move_Class**).

**Parent 2 (P2)** introduced the new `FeedParserTask` class using the old short-form `DownloadStatus` constructor:
```java
// P2 (old constructor call, discarded):
 -  downloadStatus = new DownloadStatus(request, DownloadError.ERROR_REQUEST_ERROR,
 -          false, false, "Unknown error: Status not set");
```

P2 also still imported `DownloadStatus` and `DownloadError` from the old packages.

## Interpretation

This is a **Change_Parameter_Type** conflict combined with a **Move_Class** refactoring. P1 redesigned the `DownloadStatus` constructor to accept individual typed fields rather than a composite `DownloadRequest` object, breaking the old call that P2 had written. Additionally, P1 moved both `DownloadStatus` and `DownloadError` to a new `model.download` package.

The merge had to:
1. Write the new expanded constructor call with all required arguments (`++` lines including `Date`, `feedfileType`, `isInitiatedByUser`)
2. Add the `import java.util.Date` that the new constructor requires (`++` line)
3. Update the import path for `DownloadStatus` in `FeedSyncTask` (` -` old / ` +` new)
4. Update the import path for `DownloadError` in `OnlineFeedViewActivity` (` -` old / ` +` new)

The `++` lines on the constructor arguments are directly traceable to the `Change_Parameter_Type` refactoring in P1. The  constructor signature mismatch is unambiguous, the parent attribution is clear, and the move of class packages is confirmed by the import changes.

## Complete diff

```diff
diff --cc app/src/main/java/de/danoeh/antennapod/activity/OnlineFeedViewActivity.java
index 3dfe661d1,3f01a2b2d..7a26759cc
--- a/app/src/main/java/de/danoeh/antennapod/activity/OnlineFeedViewActivity.java
+++ b/app/src/main/java/de/danoeh/antennapod/activity/OnlineFeedViewActivity.java
@@@ -51,10 -50,9 +51,9 @@@
  import de.danoeh.antennapod.core.service.playback.PlaybackService;
  import de.danoeh.antennapod.core.storage.DBReader;
  import de.danoeh.antennapod.core.storage.DBWriter;
- import de.danoeh.antennapod.core.util.FileNameGenerator;
  import de.danoeh.antennapod.parser.feed.FeedHandler;
  import de.danoeh.antennapod.parser.feed.FeedHandlerResult;
 -import de.danoeh.antennapod.core.util.DownloadError;
 +import de.danoeh.antennapod.model.download.DownloadError;
  import de.danoeh.antennapod.core.util.IntentUtils;
  import de.danoeh.antennapod.core.util.StorageUtils;
  import de.danoeh.antennapod.core.util.URLChecker;

diff --cc core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedParserTask.java
index 22981dcda,125804669..dc5893b23
--- a/core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedParserTask.java
+++ b/core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedParserTask.java
@@@ -18,6 -18,6 +19,7 @@@
  import javax.xml.parsers.ParserConfigurationException;
  import java.io.File;
  import java.io.IOException;
++import java.util.Date;
  import java.util.concurrent.Callable;

@@@ -28,6 -28,8 +30,10 @@@

    public FeedParserTask(DownloadRequest request) {
        this.request = request;
 -      downloadStatus = new DownloadStatus(request, DownloadError.ERROR_REQUEST_ERROR,
 -              false, false, "Unknown error: Status not set");
++      downloadStatus = new DownloadStatus(
++      0, request.getTitle(), 0, request.getFeedfileType(), false,
++              false, true, DownloadError.ERROR_REQUEST_ERROR, new Date(),
++              "Unknown error: Status not set", request.isInitiatedByUser());
    }

diff --cc core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedSyncTask.java
index 042a903d3,57bcecf2e..5e97c233f
--- a/core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedSyncTask.java
+++ b/core/src/main/java/de/danoeh/antennapod/core/service/download/handler/FeedSyncTask.java
@@@ -2,9 -2,10 +2,10 @@@

  import android.content.Context;

+ import androidx.annotation.NonNull;
  import de.danoeh.antennapod.model.feed.Feed;
  import de.danoeh.antennapod.core.service.download.DownloadRequest;
 -import de.danoeh.antennapod.core.service.download.DownloadStatus;
 +import de.danoeh.antennapod.model.download.DownloadStatus;
  import de.danoeh.antennapod.core.storage.DBTasks;
  import de.danoeh.antennapod.parser.feed.FeedHandlerResult;
```
