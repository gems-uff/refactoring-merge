# Case 1 — Project: ExoPlayer — Merge commit SHA1: fd2ba37b1d67576313aec0512d630331b7c99f4b

---

## Modified file(s):
`library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/RtpPayloadFormat.java`

---

## Class(es) modified in the merge:
`RtpPayloadFormat`

---

## Merge effort lines in the combined diff

**Visibility change on all RTP_MEDIA constants (`private static final` → `public static final`) and rename of one constant:**
```diff
--  private static final String RTP_MEDIA_AC3 = "AC3";
--  private static final String RTP_MEDIA_AMR = "AMR";
--  private static final String RTP_MEDIA_AMR_WB = "AMR-WB";
--  private static final String RTP_MEDIA_MPEG4_GENERIC = "MPEG4-GENERIC";
--  private static final String RTP_MEDIA_MPEG4_VIDEO = "MP4V-ES";
--  private static final String RTP_MEDIA_H263_1998 = "H263-1998";
--  private static final String RTP_MEDIA_H263_2000 = "H263-2000";
--  private static final String RTP_MEDIA_H264 = "H264";
--  private static final String RTP_MEDIA_H265 = "H265";
--  private static final String RTP_MEDIA_OPUS = "OPUS";
--  private static final String RTP_MEDIA_PCM_L8 = "L8";
--  private static final String RTP_MEDIA_PCM_L16 = "L16";
--  private static final String RTP_MEDIA_PCMA = "PCMA";
--  private static final String RTP_MEDIA_PCMU = "PCMU";
--  private static final String RTP_MEDIA_VP8 = "VP8";
--  private static final String RTP_MEDIA_VP9 = "VP9";
++  public static final String RTP_MEDIA_AC3 = "AC3";
++  public static final String RTP_MEDIA_AMR = "AMR";
++  public static final String RTP_MEDIA_AMR_WB = "AMR-WB";
++  public static final String RTP_MEDIA_MPEG4_GENERIC = "MPEG4-GENERIC";
++  public static final String RTP_MEDIA_MPEG4_LATM_AUDIO = "MP4A-LATM";
++  public static final String RTP_MEDIA_MPEG4_VIDEO = "MP4V-ES";
++  public static final String RTP_MEDIA_H263_1998 = "H263-1998";
++  public static final String RTP_MEDIA_H263_2000 = "H263-2000";
++  public static final String RTP_MEDIA_H264 = "H264";
++  public static final String RTP_MEDIA_H265 = "H265";
++  public static final String RTP_MEDIA_OPUS = "OPUS";
++  public static final String RTP_MEDIA_PCM_L8 = "L8";
++  public static final String RTP_MEDIA_PCM_L16 = "L16";
++  public static final String RTP_MEDIA_PCMA = "PCMA";
++  public static final String RTP_MEDIA_PCMU = "PCMU";
++  public static final String RTP_MEDIA_VP8 = "VP8";
++  public static final String RTP_MEDIA_VP9 = "VP9";
```

**Rename of constant at usage sites:**
```diff
--      case RTP_MEDIA_MPEG4_VIDEO:
++      case RTP_MEDIA_MPEG4_LATM_AUDIO:
++      case RTP_MEDIA_MPEG4_VIDEO:

--      case RTP_MEDIA_MPEG4_AUDIO:  (P2 name)
++      case RTP_MEDIA_MPEG4_LATM_AUDIO:
```

**Constructor signature reconciliation:**
```diff
++      Format format,
++      int rtpPayloadType,
++      int clockRate,
++      Map<String, String> fmtpParameters,
++      String mediaEncoding) {
```

---

## Relevant final code in the merge

```java
public static final String RTP_MEDIA_AC3 = "AC3";
public static final String RTP_MEDIA_AMR = "AMR";
// ... (all 17 constants now public static final)
public static final String RTP_MEDIA_MPEG4_LATM_AUDIO = "MP4A-LATM"; // renamed from MPEG4_AUDIO (P2) / new vs MPEG4_GENERIC (P1)
// ...

public RtpPayloadFormat(
    Format format,
    int rtpPayloadType,
    int clockRate,
    Map<String, String> fmtpParameters,
    String mediaEncoding) { ... }
```

---

## Number of merge-effort lines (`++` and `--`) associated with the refactoring types under analysis:
**35 lines**

---

## What each side had

**Parent 1** had all 16 `RTP_MEDIA_*` constants declared as `private static final`. The constant for MP4A-LATM audio did not exist — P1 used `RTP_MEDIA_MPEG4_GENERIC` for that codec path. The `RtpPayloadFormat` constructor had 4 parameters (no `mediaEncoding`).

**Parent 2** had promoted all `RTP_MEDIA_*` constants to `public static final` (a visibility change), added a new constant named `RTP_MEDIA_MPEG4_AUDIO` for MP4A-LATM, and added `String mediaEncoding` as a 5th constructor parameter.

The merge had to reconcile: P1's `private` constants vs P2's `public` constants, and the naming conflict between P1 (no such constant) and P2 (`RTP_MEDIA_MPEG4_AUDIO`) for MP4A-LATM — synthesizing the final name `RTP_MEDIA_MPEG4_LATM_AUDIO`.

---

## Interpretation

P2 performed two refactorings that caused merge conflicts with P1:

### 1. Replace Attribute Modifier — visibility promotion of all `RTP_MEDIA_*` constants

All 16 constants changed from `private static final` to `public static final` in P2. P1 still had `private static final`. The merge produced `--` lines removing all private declarations and `++` lines introducing the public versions — a **Replace Attribute Modifier** (change of modifier/visibility) applied uniformly across the entire constant set.

### 2. Rename_Attribute — `RTP_MEDIA_MPEG4_AUDIO` → `RTP_MEDIA_MPEG4_LATM_AUDIO`

P2 introduced the constant as `RTP_MEDIA_MPEG4_AUDIO`; the merge renamed it to `RTP_MEDIA_MPEG4_LATM_AUDIO` (more specific and accurate name), updating all `case` references. This is a **Rename_Attribute**: the constant's name changes between what P2 had and what the merge finalizes, producing `++` lines at the declaration and all switch cases.

The constructor `++` lines (`mediaEncoding` parameter) reflect the merge applying P2's addition of a new parameter — though this is a parameter addition rather than a type change, it is structurally significant as it accompanies the constant visibility refactoring in the same class.

## Complete diff

```diff
diff --cc library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/RtpPayloadFormat.java
index 0ba52c2bc5,8327c72bfd..5672b7634a
--- a/library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/RtpPayloadFormat.java
+++ b/library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/RtpPayloadFormat.java
@@@ -35,24 -36,26 +35,25 @@@ import java.util.Map
   * <p>This class wraps around the {@link Format} class, in addition to the instance fields that are
   * specific to RTP.
   */
 -@UnstableApi
  public final class RtpPayloadFormat {
  
--  private static final String RTP_MEDIA_AC3 = "AC3";
--  private static final String RTP_MEDIA_AMR = "AMR";
--  private static final String RTP_MEDIA_AMR_WB = "AMR-WB";
--  private static final String RTP_MEDIA_MPEG4_GENERIC = "MPEG4-GENERIC";
--  private static final String RTP_MEDIA_MPEG4_VIDEO = "MP4V-ES";
--  private static final String RTP_MEDIA_H263_1998 = "H263-1998";
--  private static final String RTP_MEDIA_H263_2000 = "H263-2000";
--  private static final String RTP_MEDIA_H264 = "H264";
--  private static final String RTP_MEDIA_H265 = "H265";
--  private static final String RTP_MEDIA_OPUS = "OPUS";
--  private static final String RTP_MEDIA_PCM_L8 = "L8";
--  private static final String RTP_MEDIA_PCM_L16 = "L16";
--  private static final String RTP_MEDIA_PCMA = "PCMA";
--  private static final String RTP_MEDIA_PCMU = "PCMU";
--  private static final String RTP_MEDIA_VP8 = "VP8";
--  private static final String RTP_MEDIA_VP9 = "VP9";
 -  public static final String RTP_MEDIA_MPEG4_AUDIO = "MP4A-LATM";
++  public static final String RTP_MEDIA_AC3 = "AC3";
++  public static final String RTP_MEDIA_AMR = "AMR";
++  public static final String RTP_MEDIA_AMR_WB = "AMR-WB";
++  public static final String RTP_MEDIA_MPEG4_GENERIC = "MPEG4-GENERIC";
++  public static final String RTP_MEDIA_MPEG4_LATM_AUDIO = "MP4A-LATM";
++  public static final String RTP_MEDIA_MPEG4_VIDEO = "MP4V-ES";
++  public static final String RTP_MEDIA_H263_1998 = "H263-1998";
++  public static final String RTP_MEDIA_H263_2000 = "H263-2000";
++  public static final String RTP_MEDIA_H264 = "H264";
++  public static final String RTP_MEDIA_H265 = "H265";
++  public static final String RTP_MEDIA_OPUS = "OPUS";
++  public static final String RTP_MEDIA_PCM_L8 = "L8";
++  public static final String RTP_MEDIA_PCM_L16 = "L16";
++  public static final String RTP_MEDIA_PCMA = "PCMA";
++  public static final String RTP_MEDIA_PCMU = "PCMU";
++  public static final String RTP_MEDIA_VP8 = "VP8";
++  public static final String RTP_MEDIA_VP9 = "VP9";
  
    /** Returns whether the format of a {@link MediaDescription} is supported. */
    public static boolean isFormatSupported(MediaDescription mediaDescription) {
@@@ -64,8 -67,9 +65,9 @@@
        case RTP_MEDIA_H263_2000:
        case RTP_MEDIA_H264:
        case RTP_MEDIA_H265:
 -      case RTP_MEDIA_MPEG4_AUDIO:
--      case RTP_MEDIA_MPEG4_VIDEO:
        case RTP_MEDIA_MPEG4_GENERIC:
++      case RTP_MEDIA_MPEG4_LATM_AUDIO:
++      case RTP_MEDIA_MPEG4_VIDEO:
        case RTP_MEDIA_OPUS:
        case RTP_MEDIA_PCM_L8:
        case RTP_MEDIA_PCM_L16:
@@@ -95,6 -99,7 +97,7 @@@
        case RTP_MEDIA_AMR_WB:
          return MimeTypes.AUDIO_AMR_WB;
        case RTP_MEDIA_MPEG4_GENERIC:
 -      case RTP_MEDIA_MPEG4_AUDIO:
++      case RTP_MEDIA_MPEG4_LATM_AUDIO:
          return MimeTypes.AUDIO_AAC;
        case RTP_MEDIA_OPUS:
          return MimeTypes.AUDIO_OPUS;
@@@ -140,6 -145,7 +143,8 @@@
    public final Format format;
    /** The format parameters, mapped from the SDP FMTP attribute (RFC2327 Page 22). */
    public final ImmutableMap<String, String> fmtpParameters;
++  /** The RTP media encoding. */
+   public final String mediaEncoding;
  
    /**
     * Creates a new instance.
@@@ -151,9 -157,9 +156,14 @@@
     * @param fmtpParameters The format parameters, from the SDP FMTP attribute (RFC2327 Page 22),
     *     empty if unset. The keys and values are specified in the RFCs for specific formats. For
     *     instance, RFC3640 Section 4.1 defines keys like profile-level-id and config.
++   * @param mediaEncoding The RTP media encoding.
     */
 -  public RtpPayloadFormat(Format format, int rtpPayloadType, int clockRate, Map<String,
 -      String> fmtpParameters, String mediaEncoding) {
 +  public RtpPayloadFormat(
-       Format format, int rtpPayloadType, int clockRate, Map<String, String> fmtpParameters) {
++      Format format,
++      int rtpPayloadType,
++      int clockRate,
++      Map<String, String> fmtpParameters,
++      String mediaEncoding) {
      this.rtpPayloadType = rtpPayloadType;
      this.clockRate = clockRate;
      this.format = format;
@@@ -172,7 -179,7 +183,8 @@@
      return rtpPayloadType == that.rtpPayloadType
          && clockRate == that.clockRate
          && format.equals(that.format)
--        && fmtpParameters.equals(that.fmtpParameters);
++        && fmtpParameters.equals(that.fmtpParameters)
++        && mediaEncoding.equals(that.mediaEncoding);
    }
  
    @Override
@@@ -182,6 -189,6 +194,7 @@@
      result = 31 * result + clockRate;
      result = 31 * result + format.hashCode();
      result = 31 * result + fmtpParameters.hashCode();
++    result = 31 * result + mediaEncoding.hashCode();
      return result;
    }
  }
diff --cc library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/RtspMediaTrack.java
index 8f05d30662,a72a84540f..d28d3e20a9
--- a/library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/RtspMediaTrack.java
+++ b/library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/RtspMediaTrack.java
@@@ -28,13 -28,16 +28,15 @@@ import android.util.Base64
  import android.util.Pair;
  import androidx.annotation.Nullable;
  import androidx.annotation.VisibleForTesting;
 -import androidx.media3.common.C;
 -import androidx.media3.common.Format;
 -import androidx.media3.common.MimeTypes;
 -import androidx.media3.common.ParserException;
 -import androidx.media3.common.util.CodecSpecificDataUtil;
 -import androidx.media3.common.util.ParsableBitArray;
 -import androidx.media3.common.util.UnstableApi;
 -import androidx.media3.common.util.Util;
 -import androidx.media3.extractor.AacUtil;
 -import androidx.media3.extractor.NalUnitUtil;
 +import com.google.android.exoplayer2.C;
 +import com.google.android.exoplayer2.Format;
++import com.google.android.exoplayer2.ParserException;
 +import com.google.android.exoplayer2.audio.AacUtil;
 +import com.google.android.exoplayer2.util.CodecSpecificDataUtil;
 +import com.google.android.exoplayer2.util.MimeTypes;
 +import com.google.android.exoplayer2.util.NalUnitUtil;
++import com.google.android.exoplayer2.util.ParsableBitArray;
 +import com.google.android.exoplayer2.util.Util;
  import com.google.common.collect.ImmutableList;
  import com.google.common.collect.ImmutableMap;
  
@@@ -50,7 -54,8 +52,8 @@@
    private static final String PARAMETER_H265_SPROP_PPS = "sprop-pps";
    private static final String PARAMETER_H265_SPROP_VPS = "sprop-vps";
    private static final String PARAMETER_H265_SPROP_MAX_DON_DIFF = "sprop-max-don-diff";
--  private static final String PARAMETER_MP4V_CONFIG = "config";
++  private static final String PARAMETER_MP4A_CONFIG = "config";
+   private static final String PARAMETER_MP4A_C_PRESENT = "cpresent";
  
    /** Prefix for the RFC6381 codecs string for AAC formats. */
    private static final String AAC_CODECS_PREFIX = "mp4a.40.";
@@@ -206,6 -211,21 +209,23 @@@
        case MimeTypes.AUDIO_AAC:
          checkArgument(channelCount != C.INDEX_UNSET);
          checkArgument(!fmtpParameters.isEmpty());
 -        if(mediaEncoding.equals(RtpPayloadFormat.RTP_MEDIA_MPEG4_AUDIO)) {
 -          boolean isConfigPresent  = true;
 -          if (fmtpParameters.get(PARAMETER_MP4A_C_PRESENT) != null && fmtpParameters.get(
 -              PARAMETER_MP4A_C_PRESENT).equals("0")) {
 -            isConfigPresent  = false;
 -          }
 -          checkArgument(!isConfigPresent, "cpresent == 0 means we need to parse config");
 -          @Nullable String configInput = fmtpParameters.get(PARAMETER_MP4V_CONFIG);
 -          if (configInput != null && configInput.length() % 2 == 0) {
 -            Pair<Integer, Integer> configParameters = getSampleRateAndChannelCount(configInput);
 -            channelCount = configParameters.first;
 -            clockRate = configParameters.second;
 -            formatBuilder.setSampleRate(clockRate).setChannelCount(channelCount);
 -          }
++        if (mediaEncoding.equals(RtpPayloadFormat.RTP_MEDIA_MPEG4_LATM_AUDIO)) {
++          // cpresent is defined in RFC3016 Section 5.3. cpresent=0 means the config fmtp parameter
++          // must exist.
++          checkArgument(
++              fmtpParameters.containsKey(PARAMETER_MP4A_C_PRESENT)
++                  && fmtpParameters.get(PARAMETER_MP4A_C_PRESENT).equals("0"),
++              "Only supports cpresent=0 in AAC audio.");
++          @Nullable String config = fmtpParameters.get(PARAMETER_MP4A_CONFIG);
++          checkNotNull(config, "AAC audio stream must include config fmtp parameter");
++          // config is a hex string.
++          checkArgument(config.length() % 2 == 0, "Malformat MPEG4 config: " + config);
++          AacUtil.Config aacConfig = parseAacStreamMuxConfig(config);
++          formatBuilder
++              .setSampleRate(aacConfig.sampleRateHz)
++              .setChannelCount(aacConfig.channelCount)
++              .setCodecs(aacConfig.codecs);
+         }
          processAacFmtpAttribute(formatBuilder, fmtpParameters, channelCount, clockRate);
          break;
        case MimeTypes.AUDIO_AMR_NB:
@@@ -298,9 -319,35 +319,29 @@@
              AacUtil.buildAacLcAudioSpecificConfig(sampleRate, channelCount)));
    }
  
+   /**
 -   * Returns a {@link Pair} of sample rate and channel count, by parsing the
 -   *  MPEG4 Audio Stream Mux configuration.
++   * Returns the {@link AacUtil.Config} by parsing the MPEG4 Audio Stream Mux configuration.
+    *
 -   * <p>fmtp attribute {@code config} includes the MPEG4 Audio Stream Mux
 -   * configuration (ISO/IEC14496-3, Chapter 1.7.3).
++   * <p>fmtp attribute {@code config} includes the MPEG4 Audio Stream Mux configuration
++   * (ISO/IEC14496-3, Chapter 1.7.3).
+    */
 -  private static Pair<Integer, Integer> getSampleRateAndChannelCount(String configInput) {
 -    ParsableBitArray config  = new ParsableBitArray(Util.getBytesFromHexString(configInput));
 -    int audioMuxVersion = config .readBits(1);
 -    if (audioMuxVersion == 0) {
 -      checkArgument(config .readBits(1) == 1, "Only supports one allStreamsSameTimeFraming.");
 -      config .readBits(6);
 -      checkArgument(config .readBits(4) == 0, "Only supports one program.");
 -      checkArgument(config .readBits(3) == 0, "Only supports one numLayer.");
 -      @Nullable AacUtil.Config aacConfig = null;
 -      try {
 -        aacConfig = AacUtil.parseAudioSpecificConfig(config , false);
 -      } catch (ParserException e) {
 -        throw new IllegalArgumentException(e);
 -      }
 -      return Pair.create(aacConfig.channelCount, aacConfig.sampleRateHz);
++  private static AacUtil.Config parseAacStreamMuxConfig(String streamMuxConfig) {
++    ParsableBitArray config = new ParsableBitArray(Util.getBytesFromHexString(streamMuxConfig));
++    checkArgument(config.readBits(1) == 0, "Only supports audio mux version 0.");
++    checkArgument(config.readBits(1) == 1, "Only supports allStreamsSameTimeFraming.");
++    config.skipBits(6);
++    checkArgument(config.readBits(4) == 0, "Only supports one program.");
++    checkArgument(config.readBits(3) == 0, "Only supports one numLayer.");
++    try {
++      return AacUtil.parseAudioSpecificConfig(config, false);
++    } catch (ParserException e) {
++      throw new IllegalArgumentException(e);
+     }
 -    throw new IllegalArgumentException ("Only support audio mux version 0");
+   }
+ 
    private static void processMPEG4FmtpAttribute(
        Format.Builder formatBuilder, ImmutableMap<String, String> fmtpAttributes) {
--    @Nullable String configInput = fmtpAttributes.get(PARAMETER_MP4V_CONFIG);
++    @Nullable String configInput = fmtpAttributes.get(PARAMETER_MP4A_CONFIG);
      if (configInput != null) {
        byte[] configBuffer = Util.getBytesFromHexString(configInput);
        formatBuilder.setInitializationData(ImmutableList.of(configBuffer));
diff --cc library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/reader/DefaultRtpPayloadReaderFactory.java
index 6977b1dc72,7120126561..710eba8cc9
--- a/library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/reader/DefaultRtpPayloadReaderFactory.java
+++ b/library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/reader/DefaultRtpPayloadReaderFactory.java
@@@ -33,7 -35,11 +33,11 @@@ import com.google.android.exoplayer2.ut
        case MimeTypes.AUDIO_AC3:
          return new RtpAc3Reader(payloadFormat);
        case MimeTypes.AUDIO_AAC:
-         return new RtpAacReader(payloadFormat);
 -        if(payloadFormat.mediaEncoding.equals(RtpPayloadFormat.RTP_MEDIA_MPEG4_AUDIO)){
++        if (payloadFormat.mediaEncoding.equals(RtpPayloadFormat.RTP_MEDIA_MPEG4_LATM_AUDIO)) {
+           return new RtpMp4aReader(payloadFormat);
+         } else {
+           return new RtpAacReader(payloadFormat);
+         }
        case MimeTypes.AUDIO_AMR_NB:
        case MimeTypes.AUDIO_AMR_WB:
          return new RtpAmrReader(payloadFormat);
diff --cc library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/reader/RtpMp4aReader.java
index 0000000000,0000000000..d59e506275
new file mode 100644
--- /dev/null
+++ b/library/rtsp/src/main/java/com/google/android/exoplayer2/source/rtsp/reader/RtpMp4aReader.java
@@@ -1,0 -1,0 +1,180 @@@
++/*
++ * Copyright 2022 The Android Open Source Project
++ *
++ * Licensed under the Apache License, Version 2.0 (the "License");
++ * you may not use this file except in compliance with the License.
++ * You may obtain a copy of the License at
++ *
++ *      http://www.apache.org/licenses/LICENSE-2.0
++ *
++ * Unless required by applicable law or agreed to in writing, software
++ * distributed under the License is distributed on an "AS IS" BASIS,
++ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
++ * See the License for the specific language governing permissions and
++ * limitations under the License.
++ */
++package com.google.android.exoplayer2.source.rtsp.reader;
++
++import static com.google.android.exoplayer2.source.rtsp.reader.RtpReaderUtils.toSampleTimeUs;
++import static com.google.android.exoplayer2.util.Assertions.checkArgument;
++import static com.google.android.exoplayer2.util.Assertions.checkNotNull;
++import static com.google.android.exoplayer2.util.Assertions.checkState;
++import static com.google.android.exoplayer2.util.Assertions.checkStateNotNull;
++import static com.google.android.exoplayer2.util.Util.castNonNull;
++
++import androidx.annotation.Nullable;
++import com.google.android.exoplayer2.C;
++import com.google.android.exoplayer2.ParserException;
++import com.google.android.exoplayer2.extractor.ExtractorOutput;
++import com.google.android.exoplayer2.extractor.TrackOutput;
++import com.google.android.exoplayer2.source.rtsp.RtpPacket;
++import com.google.android.exoplayer2.source.rtsp.RtpPayloadFormat;
++import com.google.android.exoplayer2.util.ParsableBitArray;
++import com.google.android.exoplayer2.util.ParsableByteArray;
++import com.google.android.exoplayer2.util.Util;
++import com.google.common.collect.ImmutableMap;
++import org.checkerframework.checker.nullness.qual.MonotonicNonNull;
++
++/**
++ * Parses an MP4A-LATM byte stream carried on RTP packets, and extracts MP4A-LATM Access Units.
++ *
++ * <p>Refer to RFC3016 for more details. The LATM byte stream format is defined in ISO/IEC14496-3.
++ */
++/* package */ final class RtpMp4aReader implements RtpPayloadReader {
++  private static final String TAG = "RtpMp4aReader";
++
++  private static final String PARAMETER_MP4A_CONFIG = "config";
++
++  private final RtpPayloadFormat payloadFormat;
++  private final int numberOfSubframes;
++  private @MonotonicNonNull TrackOutput trackOutput;
++  private long firstReceivedTimestamp;
++  private int previousSequenceNumber;
++  /** The combined size of a sample that is fragmented into multiple subFrames. */
++  private int fragmentedSampleSizeBytes;
++
++  private long startTimeOffsetUs;
++  private long fragmentedSampleTimeUs;
++
++  /**
++   * Creates an instance.
++   *
++   * @throws IllegalArgumentException If {@link RtpPayloadFormat payloadFormat} is malformed.
++   */
++  public RtpMp4aReader(RtpPayloadFormat payloadFormat) {
++    this.payloadFormat = payloadFormat;
++    try {
++      numberOfSubframes = getNumOfSubframesFromMpeg4AudioConfig(payloadFormat.fmtpParameters);
++    } catch (ParserException e) {
++      throw new IllegalArgumentException(e);
++    }
++    firstReceivedTimestamp = C.TIME_UNSET;
++    previousSequenceNumber = C.INDEX_UNSET;
++    fragmentedSampleSizeBytes = 0;
++    // The start time offset must be 0 until the first seek.
++    startTimeOffsetUs = 0;
++    fragmentedSampleTimeUs = C.TIME_UNSET;
++  }
++
++  @Override
++  public void createTracks(ExtractorOutput extractorOutput, int trackId) {
++    trackOutput = extractorOutput.track(trackId, C.TRACK_TYPE_VIDEO);
++    castNonNull(trackOutput).format(payloadFormat.format);
++  }
++
++  @Override
++  public void onReceivingFirstPacket(long timestamp, int sequenceNumber) {
++    checkState(firstReceivedTimestamp == C.TIME_UNSET);
++    firstReceivedTimestamp = timestamp;
++  }
++
++  @Override
++  public void consume(
++      ParsableByteArray data, long timestamp, int sequenceNumber, boolean rtpMarker) {
++    checkStateNotNull(trackOutput);
++
++    int expectedSequenceNumber = RtpPacket.getNextSequenceNumber(previousSequenceNumber);
++    if (fragmentedSampleSizeBytes > 0 && expectedSequenceNumber < sequenceNumber) {
++      outputSampleMetadataForFragmentedPackets();
++    }
++
++    for (int subFrameIndex = 0; subFrameIndex < numberOfSubframes; subFrameIndex++) {
++      int sampleLength = 0;
++      // Implements PayloadLengthInfo() in ISO/IEC14496-3 Chapter 1.7.3.1, it only supports one
++      // program and one layer. Each subframe starts with a variable length encoding.
++      while (data.getPosition() < data.limit()) {
++        int payloadMuxLength = data.readUnsignedByte();
++        sampleLength += payloadMuxLength;
++        if (payloadMuxLength != 0xff) {
++          break;
++        }
++      }
++
++      trackOutput.sampleData(data, sampleLength);
++      fragmentedSampleSizeBytes += sampleLength;
++    }
++    fragmentedSampleTimeUs =
++        toSampleTimeUs(
++            startTimeOffsetUs, timestamp, firstReceivedTimestamp, payloadFormat.clockRate);
++    if (rtpMarker) {
++      outputSampleMetadataForFragmentedPackets();
++    }
++    previousSequenceNumber = sequenceNumber;
++  }
++
++  @Override
++  public void seek(long nextRtpTimestamp, long timeUs) {
++    firstReceivedTimestamp = nextRtpTimestamp;
++    fragmentedSampleSizeBytes = 0;
++    startTimeOffsetUs = timeUs;
++  }
++
++  // Internal methods.
++
++  /**
++   * Parses an MPEG-4 Audio Stream Mux configuration, as defined in ISO/IEC14496-3.
++   *
++   * <p>FMTP attribute {@code config} contains the MPEG-4 Audio Stream Mux configuration.
++   *
++   * @param fmtpAttributes The format parameters, mapped from the SDP FMTP attribute.
++   * @return The number of subframes that is carried in each RTP packet.
++   */
++  private static int getNumOfSubframesFromMpeg4AudioConfig(
++      ImmutableMap<String, String> fmtpAttributes) throws ParserException {
++    @Nullable String configInput = fmtpAttributes.get(PARAMETER_MP4A_CONFIG);
++    int numberOfSubframes = 0;
++    if (configInput != null && configInput.length() % 2 == 0) {
++      byte[] configBuffer = Util.getBytesFromHexString(configInput);
++      ParsableBitArray scratchBits = new ParsableBitArray(configBuffer);
++      int audioMuxVersion = scratchBits.readBits(1);
++      if (audioMuxVersion == 0) {
++        checkArgument(scratchBits.readBits(1) == 1, "Only supports allStreamsSameTimeFraming.");
++        numberOfSubframes = scratchBits.readBits(6);
++        checkArgument(scratchBits.readBits(4) == 0, "Only suppors one program.");
++        checkArgument(scratchBits.readBits(3) == 0, "Only suppors one layer.");
++      } else {
++        throw ParserException.createForMalformedDataOfUnknownType(
++            "unsupported audio mux version: " + audioMuxVersion, null);
++      }
++    }
++    // ISO/IEC14496-3 Chapter 1.7.3.2.3: The minimum value is 0 indicating 1 subframe.
++    return numberOfSubframes + 1;
++  }
++
++  /**
++   * Outputs sample metadata.
++   *
++   * <p>Call this method only after receiving the end of an MPEG4 partition.
++   */
++  private void outputSampleMetadataForFragmentedPackets() {
++    checkNotNull(trackOutput)
++        .sampleMetadata(
++            fragmentedSampleTimeUs,
++            C.BUFFER_FLAG_KEY_FRAME,
++            fragmentedSampleSizeBytes,
++            /* offset= */ 0,
++            /* cryptoData= */ null);
++    fragmentedSampleSizeBytes = 0;
++    fragmentedSampleTimeUs = C.TIME_UNSET;
++  }
++}
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspClientTest.java
index e07e11fd38,4fdc1fc274..6e4c19bb58
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspClientTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspClientTest.java
@@@ -70,8 -70,8 +70,8 @@@ public final class RtspClientTest 
          ImmutableList.of(
              RtspTestUtils.readRtpPacketStreamDump("media/rtsp/h264-dump.json"),
              RtspTestUtils.readRtpPacketStreamDump("media/rtsp/aac-dump.json"),
--            // MP4A-LATM is not supported at the moment.
--            RtspTestUtils.readRtpPacketStreamDump("media/rtsp/mp4a-latm-dump.json"));
++            // MPEG2TS is not supported at the moment.
++            RtspTestUtils.readRtpPacketStreamDump("media/rtsp/mpeg2ts-dump.json"));
    }
  
    @After
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspMediaTrackTest.java
index c2b88db37f,6f5b6fbc02..5e94d8dff0
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspMediaTrackTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspMediaTrackTest.java
@@@ -76,7 -76,7 +76,8 @@@ public class RtspMediaTrackTest 
              /* fmtpParameters= */ ImmutableMap.of(
                  "packetization-mode", "1",
                  "profile-level-id", "64001F",
--                "sprop-parameter-sets", "Z2QAH6zZQPARabIAAAMACAAAAwGcHjBjLA==,aOvjyyLA"));
++                "sprop-parameter-sets", "Z2QAH6zZQPARabIAAAMACAAAAwGcHjBjLA==,aOvjyyLA"),
++            RtpPayloadFormat.RTP_MEDIA_H264);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -101,7 -101,7 +102,8 @@@
                  .build(),
              /* rtpPayloadType= */ 0,
              /* clockRate= */ 8_000,
--            /* fmtpParameters= */ ImmutableMap.of());
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_PCMU);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -134,7 -134,7 +136,8 @@@
                  .build(),
              /* rtpPayloadType= */ pcmaPayloadType,
              /* clockRate= */ pcmaClockRate,
--            /* fmtpParameters= */ ImmutableMap.of());
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_PCMA);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -168,7 -168,7 +171,8 @@@
                  .build(),
              /* rtpPayloadType= */ l16StereoPayloadType,
              /* clockRate= */ l16StereoClockRate,
--            /* fmtpParameters= */ ImmutableMap.of());
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_PCM_L16);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -202,7 -202,7 +206,8 @@@
                  .build(),
              /* rtpPayloadType= */ l16MonoPayloadType,
              /* clockRate= */ l16MonoClockRate,
--            /* fmtpParameters= */ ImmutableMap.of());
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_PCM_L16);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -244,7 -244,7 +249,8 @@@
              /* fmtpParameters= */ ImmutableMap.of(
                  "packetization-mode", "1",
                  "profile-level-id", "64001F",
--                "sprop-parameter-sets", "Z2QAH6zZQPARabIAAAMACAAAAwGcHjBjLA==,aOvjyyLA"));
++                "sprop-parameter-sets", "Z2QAH6zZQPARabIAAAMACAAAAwGcHjBjLA==,aOvjyyLA"),
++            RtpPayloadFormat.RTP_MEDIA_H264);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -288,7 -288,7 +294,8 @@@
                  .put("indexlength", "3")
                  .put("indexdeltalength", "3")
                  .put("config", "1208")
--                .buildOrThrow());
++                .buildOrThrow(),
++            RtpPayloadFormat.RTP_MEDIA_MPEG4_GENERIC);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -315,7 -315,7 +322,8 @@@
                  .build(),
              /* rtpPayloadType= */ 97,
              /* clockRate= */ 48000,
--            /* fmtpParameters= */ ImmutableMap.of());
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_AC3);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
@@@ -342,7 -342,7 +350,8 @@@
                  .build(),
              /* rtpPayloadType= */ 97,
              /* clockRate= */ 48000,
--            /* fmtpParameters= */ ImmutableMap.of());
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_AC3);
  
      assertThat(format).isEqualTo(expectedFormat);
    }
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspPlaybackTest.java
index 1cb87f6e86,0c93acc61f..1ddba06c11
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspPlaybackTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/RtspPlaybackTest.java
@@@ -72,7 -72,7 +72,7 @@@ public final class RtspPlaybackTest 
  
    private RtpPacketStreamDump aacRtpPacketStreamDump;
    // ExoPlayer does not support extracting MP4A-LATM RTP payload at the moment.
--  private RtpPacketStreamDump mp4aLatmRtpPacketStreamDump;
++  private RtpPacketStreamDump mpeg2tsRtpPacketStreamDump;
  
    /** Creates a new instance. */
    public RtspPlaybackTest() {
@@@ -90,8 -90,8 +90,8 @@@
    @Before
    public void setUp() throws Exception {
      aacRtpPacketStreamDump = RtspTestUtils.readRtpPacketStreamDump("media/rtsp/aac-dump.json");
--    mp4aLatmRtpPacketStreamDump =
--        RtspTestUtils.readRtpPacketStreamDump("media/rtsp/mp4a-latm-dump.json");
++    mpeg2tsRtpPacketStreamDump =
++        RtspTestUtils.readRtpPacketStreamDump("media/rtsp/mpeg2ts-dump.json");
    }
  
    @Test
@@@ -99,7 -99,7 +99,7 @@@
      ResponseProvider responseProvider =
          new ResponseProvider(
              clock,
--            ImmutableList.of(aacRtpPacketStreamDump, mp4aLatmRtpPacketStreamDump),
++            ImmutableList.of(aacRtpPacketStreamDump, mpeg2tsRtpPacketStreamDump),
              fakeRtpDataChannel);
  
      try (RtspServer rtspServer = new RtspServer(responseProvider)) {
@@@ -124,7 -124,7 +124,7 @@@
      try (RtspServer rtspServer =
          new RtspServer(
              new ResponseProvider(
--                clock, ImmutableList.of(mp4aLatmRtpPacketStreamDump), fakeRtpDataChannel))) {
++                clock, ImmutableList.of(mpeg2tsRtpPacketStreamDump), fakeRtpDataChannel))) {
        ExoPlayer player = createExoPlayer(rtspServer.startAndGetPortNumber(), rtpDataChannelFactory);
  
        AtomicReference<Throwable> playbackError = new AtomicReference<>();
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpAc3ReaderTest.java
index 14ce7913c6,2404b669b5..7876c2c7a5
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpAc3ReaderTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpAc3ReaderTest.java
@@@ -75,7 -75,7 +75,8 @@@ public final class RtpAc3ReaderTest 
                .build(),
            /* rtpPayloadType= */ 97,
            /* clockRate= */ 48_000,
--          /* fmtpParameters= */ ImmutableMap.of());
++          /* fmtpParameters= */ ImmutableMap.of(),
++          RtpPayloadFormat.RTP_MEDIA_AC3);
  
    @Rule public final MockitoRule mockito = MockitoJUnit.rule();
  
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpAmrReaderTest.java
index c2b7d17ad6,cce1a3db44..df1fe56b7d
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpAmrReaderTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpAmrReaderTest.java
@@@ -215,6 -215,6 +215,9 @@@ public final class RtpAmrReaderTest 
              .build(),
          /* rtpPayloadType= */ 97,
          /* clockRate= */ sampleRate,
--        /* fmtpParameters= */ ImmutableMap.of());
++        /* fmtpParameters= */ ImmutableMap.of(),
++        MimeTypes.AUDIO_AMR.equals(mimeType)
++            ? RtpPayloadFormat.RTP_MEDIA_AMR
++            : RtpPayloadFormat.RTP_MEDIA_AMR_WB);
    }
  }
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpH263ReaderTest.java
index a8a59b9e2a,4c1f4efde0..d2aae8538d
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpH263ReaderTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpH263ReaderTest.java
@@@ -109,7 -109,7 +109,8 @@@ public final class RtpH263ReaderTest 
                .build(),
            /* rtpPayloadType= */ 96,
            /* clockRate= */ (int) MEDIA_CLOCK_FREQUENCY,
--          /* fmtpParameters= */ ImmutableMap.of());
++          /* fmtpParameters= */ ImmutableMap.of(),
++          RtpPayloadFormat.RTP_MEDIA_H263_1998);
  
    private FakeExtractorOutput extractorOutput;
  
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpMp4aReaderTest.java
index 0000000000,0000000000..79509e2647
new file mode 100644
--- /dev/null
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpMp4aReaderTest.java
@@@ -1,0 -1,0 +1,160 @@@
++/*
++ * Copyright 2022 The Android Open Source Project
++ *
++ * Licensed under the Apache License, Version 2.0 (the "License");
++ * you may not use this file except in compliance with the License.
++ * You may obtain a copy of the License at
++ *
++ *      http://www.apache.org/licenses/LICENSE-2.0
++ *
++ * Unless required by applicable law or agreed to in writing, software
++ * distributed under the License is distributed on an "AS IS" BASIS,
++ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
++ * See the License for the specific language governing permissions and
++ * limitations under the License.
++ */
++package com.google.android.exoplayer2.source.rtsp.reader;
++
++import static com.google.android.exoplayer2.util.Util.getBytesFromHexString;
++import static com.google.common.truth.Truth.assertThat;
++
++import androidx.test.ext.junit.runners.AndroidJUnit4;
++import com.google.android.exoplayer2.Format;
++import com.google.android.exoplayer2.ParserException;
++import com.google.android.exoplayer2.source.rtsp.RtpPacket;
++import com.google.android.exoplayer2.source.rtsp.RtpPayloadFormat;
++import com.google.android.exoplayer2.testutil.FakeExtractorOutput;
++import com.google.android.exoplayer2.testutil.FakeTrackOutput;
++import com.google.android.exoplayer2.util.MimeTypes;
++import com.google.android.exoplayer2.util.ParsableByteArray;
++import com.google.common.collect.ImmutableMap;
++import com.google.common.primitives.Bytes;
++import org.junit.Before;
++import org.junit.Test;
++import org.junit.runner.RunWith;
++
++/** Unit test for {@link RtpMp4aReader}. */
++@RunWith(AndroidJUnit4.class)
++public final class RtpMp4aReaderTest {
++  private static final byte[] FRAME_1_FRAGMENT_1_DATA = getBytesFromHexString("0102");
++  private static final RtpPacket FRAME_1_FRAGMENT_1 =
++      new RtpPacket.Builder()
++          .setTimestamp(2599168056L)
++          .setSequenceNumber(40289)
++          .setMarker(false)
++          .setPayloadData(
++              Bytes.concat(/* payload size */ getBytesFromHexString("02"), FRAME_1_FRAGMENT_1_DATA))
++          .build();
++  private static final byte[] FRAME_1_FRAGMENT_2_DATA = getBytesFromHexString("030405");
++  private static final RtpPacket FRAME_1_FRAGMENT_2 =
++      new RtpPacket.Builder()
++          .setTimestamp(2599168056L)
++          .setSequenceNumber(40290)
++          .setMarker(true)
++          .setPayloadData(
++              Bytes.concat(/* payload size */ getBytesFromHexString("03"), FRAME_1_FRAGMENT_2_DATA))
++          .build();
++  private static final byte[] FRAME_1_DATA =
++      Bytes.concat(FRAME_1_FRAGMENT_1_DATA, FRAME_1_FRAGMENT_2_DATA);
++
++  private static final byte[] FRAME_2_FRAGMENT_1_DATA = getBytesFromHexString("0607");
++  private static final RtpPacket FRAME_2_FRAGMENT_1 =
++      new RtpPacket.Builder()
++          .setTimestamp(2599168344L)
++          .setSequenceNumber(40291)
++          .setMarker(false)
++          .setPayloadData(
++              Bytes.concat(/* payload size */ getBytesFromHexString("02"), FRAME_2_FRAGMENT_1_DATA))
++          .build();
++  private static final byte[] FRAME_2_FRAGMENT_2_DATA = getBytesFromHexString("0809");
++  private static final RtpPacket FRAME_2_FRAGMENT_2 =
++      new RtpPacket.Builder()
++          .setTimestamp(2599168344L)
++          .setSequenceNumber(40292)
++          .setMarker(true)
++          .setPayloadData(
++              Bytes.concat(/* payload size */ getBytesFromHexString("02"), FRAME_2_FRAGMENT_2_DATA))
++          .build();
++  private static final byte[] FRAME_2_DATA =
++      Bytes.concat(FRAME_2_FRAGMENT_1_DATA, FRAME_2_FRAGMENT_2_DATA);
++
++  private static final RtpPayloadFormat MP4A_LATM_FORMAT =
++      new RtpPayloadFormat(
++          new Format.Builder().setSampleMimeType(MimeTypes.AUDIO_AAC).setChannelCount(1).build(),
++          /* rtpPayloadType= */ 97,
++          /* clockRate= */ 44_100,
++          /* fmtpParameters= */ ImmutableMap.of(),
++          RtpPayloadFormat.RTP_MEDIA_MPEG4_LATM_AUDIO);
++
++  private FakeExtractorOutput extractorOutput;
++
++  @Before
++  public void setUp() {
++    extractorOutput = new FakeExtractorOutput();
++  }
++
++  @Test
++  public void consume_validPackets() throws ParserException {
++    RtpMp4aReader mp4aLatmReader = new RtpMp4aReader(MP4A_LATM_FORMAT);
++    mp4aLatmReader.createTracks(extractorOutput, /* trackId= */ 0);
++    mp4aLatmReader.onReceivingFirstPacket(
++        FRAME_1_FRAGMENT_1.timestamp, FRAME_1_FRAGMENT_1.sequenceNumber);
++    consume(mp4aLatmReader, FRAME_1_FRAGMENT_1);
++    consume(mp4aLatmReader, FRAME_1_FRAGMENT_2);
++    consume(mp4aLatmReader, FRAME_2_FRAGMENT_1);
++    consume(mp4aLatmReader, FRAME_2_FRAGMENT_2);
++
++    FakeTrackOutput trackOutput = extractorOutput.trackOutputs.get(0);
++    assertThat(trackOutput.getSampleCount()).isEqualTo(2);
++    assertThat(trackOutput.getSampleData(0)).isEqualTo(FRAME_1_DATA);
++    assertThat(trackOutput.getSampleTimeUs(0)).isEqualTo(0);
++    assertThat(trackOutput.getSampleData(1)).isEqualTo(FRAME_2_DATA);
++    assertThat(trackOutput.getSampleTimeUs(1)).isEqualTo(6530);
++  }
++
++  @Test
++  public void consume_fragmentedFrameMissingFirstFragment() throws ParserException {
++    RtpMp4aReader mp4aLatmReader = new RtpMp4aReader(MP4A_LATM_FORMAT);
++    mp4aLatmReader.createTracks(extractorOutput, /* trackId= */ 0);
++    mp4aLatmReader.onReceivingFirstPacket(
++        FRAME_1_FRAGMENT_1.timestamp, FRAME_1_FRAGMENT_1.sequenceNumber);
++    consume(mp4aLatmReader, FRAME_1_FRAGMENT_2);
++    consume(mp4aLatmReader, FRAME_2_FRAGMENT_1);
++    consume(mp4aLatmReader, FRAME_2_FRAGMENT_2);
++
++    FakeTrackOutput trackOutput = extractorOutput.trackOutputs.get(0);
++    assertThat(trackOutput.getSampleCount()).isEqualTo(2);
++    assertThat(trackOutput.getSampleData(0)).isEqualTo(FRAME_1_FRAGMENT_2_DATA);
++    assertThat(trackOutput.getSampleTimeUs(0)).isEqualTo(0);
++    assertThat(trackOutput.getSampleData(1)).isEqualTo(FRAME_2_DATA);
++    assertThat(trackOutput.getSampleTimeUs(1)).isEqualTo(6530);
++  }
++
++  @Test
++  public void consume_fragmentedFrameMissingBoundaryFragment() throws ParserException {
++    RtpMp4aReader mp4aLatmReader = new RtpMp4aReader(MP4A_LATM_FORMAT);
++    mp4aLatmReader.createTracks(extractorOutput, /* trackId= */ 0);
++    mp4aLatmReader.onReceivingFirstPacket(
++        FRAME_1_FRAGMENT_1.timestamp, FRAME_1_FRAGMENT_1.sequenceNumber);
++    consume(mp4aLatmReader, FRAME_1_FRAGMENT_1);
++    consume(mp4aLatmReader, FRAME_2_FRAGMENT_1);
++    consume(mp4aLatmReader, FRAME_2_FRAGMENT_2);
++
++    FakeTrackOutput trackOutput = extractorOutput.trackOutputs.get(0);
++    assertThat(trackOutput.getSampleCount()).isEqualTo(2);
++    assertThat(trackOutput.getSampleData(0)).isEqualTo(FRAME_1_FRAGMENT_1_DATA);
++    assertThat(trackOutput.getSampleTimeUs(0)).isEqualTo(0);
++    assertThat(trackOutput.getSampleData(1)).isEqualTo(FRAME_2_DATA);
++    assertThat(trackOutput.getSampleTimeUs(1)).isEqualTo(6530);
++  }
++
++  private static void consume(RtpMp4aReader mpeg4Reader, RtpPacket rtpPacket) {
++    ParsableByteArray packetData = new ParsableByteArray();
++    packetData.reset(rtpPacket.payloadData);
++    mpeg4Reader.consume(
++        packetData,
++        rtpPacket.timestamp,
++        rtpPacket.sequenceNumber,
++        /* isFrameBoundary= */ rtpPacket.marker);
++  }
++}
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpOpusReaderTest.java
index c01be2fdd2,1b2ed3a50b..b14dde0d76
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpOpusReaderTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpOpusReaderTest.java
@@@ -51,7 -51,7 +51,8 @@@ public final class RtpOpusReaderTest 
                .build(),
            /* rtpPayloadType= */ 97,
            /* clockRate= */ 48_000,
--          /* fmtpParameters= */ ImmutableMap.of());
++          /* fmtpParameters= */ ImmutableMap.of(),
++          RtpPayloadFormat.RTP_MEDIA_OPUS);
  
    private static final RtpPacket OPUS_HEADER =
        createRtpPacket(
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpPcmReaderTest.java
index 393ff5c9c2,bba419e3d6..b6e5d8b7c1
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpPcmReaderTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpPcmReaderTest.java
@@@ -69,7 -69,7 +69,8 @@@ public final class RtpPcmReaderTest 
                      .build(),
                  /* rtpPayloadType= */ RTP_PAYLOAD_TYPE,
                  /* clockRate= */ 48_000,
--                /* fmtpParameters= */ ImmutableMap.of()));
++                /* fmtpParameters= */ ImmutableMap.of(),
++                RtpPayloadFormat.RTP_MEDIA_PCM_L8));
  
      pcmReader.createTracks(extractorOutput, /* trackId= */ 0);
      pcmReader.onReceivingFirstPacket(PACKET_1.timestamp, PACKET_1.sequenceNumber);
@@@ -97,7 -97,7 +98,8 @@@
                      .build(),
                  /* rtpPayloadType= */ RTP_PAYLOAD_TYPE,
                  /* clockRate= */ 60_000,
--                /* fmtpParameters= */ ImmutableMap.of()));
++                /* fmtpParameters= */ ImmutableMap.of(),
++                RtpPayloadFormat.RTP_MEDIA_PCM_L16));
  
      pcmReader.createTracks(extractorOutput, /* trackId= */ 0);
      pcmReader.onReceivingFirstPacket(PACKET_1.timestamp, PACKET_1.sequenceNumber);
@@@ -124,7 -124,7 +126,8 @@@
                      .build(),
                  /* rtpPayloadType= */ RTP_PAYLOAD_TYPE,
                  /* clockRate= */ 16_000,
--                /* fmtpParameters= */ ImmutableMap.of()));
++                /* fmtpParameters= */ ImmutableMap.of(),
++                RtpPayloadFormat.RTP_MEDIA_PCMA));
  
      pcmReader.createTracks(extractorOutput, /* trackId= */ 0);
      pcmReader.onReceivingFirstPacket(PACKET_1.timestamp, PACKET_1.sequenceNumber);
@@@ -151,7 -151,7 +154,8 @@@
                      .build(),
                  /* rtpPayloadType= */ RTP_PAYLOAD_TYPE,
                  /* clockRate= */ 24_000,
--                /* fmtpParameters= */ ImmutableMap.of()));
++                /* fmtpParameters= */ ImmutableMap.of(),
++                RtpPayloadFormat.RTP_MEDIA_PCMU));
  
      pcmReader.createTracks(extractorOutput, /* trackId= */ 0);
      pcmReader.onReceivingFirstPacket(PACKET_1.timestamp, PACKET_1.sequenceNumber);
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpVp8ReaderTest.java
index dde2b265ab,73ffe05fc5..9950248e39
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpVp8ReaderTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpVp8ReaderTest.java
@@@ -190,7 -190,7 +190,8 @@@ public final class RtpVp8ReaderTest 
              new Format.Builder().setSampleMimeType(MimeTypes.VIDEO_VP8).build(),
              /* rtpPayloadType= */ 96,
              /* clockRate= */ (int) MEDIA_CLOCK_FREQUENCY,
--            /* fmtpParameters= */ ImmutableMap.of()));
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_VP8));
    }
  
    private static void consume(RtpVp8Reader vp8Reader, RtpPacket rtpPacket) {
diff --cc library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpVp9ReaderTest.java
index 10250c1dee,22f87ff702..9d174e453b
--- a/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpVp9ReaderTest.java
+++ b/library/rtsp/src/test/java/com/google/android/exoplayer2/source/rtsp/reader/RtpVp9ReaderTest.java
@@@ -185,7 -185,7 +185,8 @@@ public final class RtpVp9ReaderTest 
              new Format.Builder().setSampleMimeType(MimeTypes.VIDEO_VP9).build(),
              /* rtpPayloadType= */ 96,
              /* clockRate= */ (int) MEDIA_CLOCK_FREQUENCY,
--            /* fmtpParameters= */ ImmutableMap.of()));
++            /* fmtpParameters= */ ImmutableMap.of(),
++            RtpPayloadFormat.RTP_MEDIA_VP9));
    }
  
    private static void consume(RtpVp9Reader vp9Reader, RtpPacket rtpPacket) {
diff --cc testdata/src/test/assets/media/rtsp/mpeg2ts-dump.json
index 0000000000,0000000000..6546e52958
new file mode 100644
--- /dev/null
+++ b/testdata/src/test/assets/media/rtsp/mpeg2ts-dump.json
@@@ -1,0 -1,0 +1,9 @@@
++{
++  "trackName": "track3",
++  "firstSequenceNumber": 0,
++  "firstTimestamp": 0,
++  "transmitIntervalMs": 30,
++  "mediaDescription": "m=video 30000 RTP/AVP 32\r\nc=IN IP4 0.0.0.0\r\na=rtpmap:98 MP4/90000\r\na=control:track3\r\n",
++  "packets": [
++  ]
++}
```
