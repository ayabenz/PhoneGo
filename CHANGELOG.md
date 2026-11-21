# Changelog

The PhoneGo Android app, one section per release. Newest first. Each release is a
`phonego-vX.Y.Z` tag with an APK on the [releases page](https://github.com/HKUDS/PhoneGo/releases);
every build is signed with the same key, so a newer one installs over an older one.

PhoneGo App VersionChanged[CH]，[CH]。[CH]Version[CH] `phonego-vX.Y.Z` Tab[CH] APK
（See [releases Page](https://github.com/HKUDS/PhoneGo/releases)）；[CH]Version[CH]，
NewVersion[CH]Install。

The format follows [Keep a Changelog](https://keepachangelog.com/), and the
versions are the app's own — the CLI in this repository has its own history.

---

## 0.4.4 — 2026-11-21

`PhoneGo-0.4.4-arm64.apk` · SHA-256 `fd639ff3694c4d895fa166fc060ff56e11ba405f8daa905534e151ed613d774b`

**English**

- **Changed**: a page that jumps to the phone's screen is pulled back to the
  virtual display, and only followed after two attempts. Measured on
  [CH] → [CH]: four pulls, one follow, task done in 3m31s.
- **Fixed**: the chat could hang on [CH] forever — a `finish`-only step batch
  returned before the terminal-state handling ran.
- **Fixed**: the transcript and session index are written atomically (temp file,
  fsync, rename, `.bak` fallback); a kill mid-write could leave an empty chat.
- **Fixed**: the connection to adbd heals itself after `ssl.SSLEOFError`; a read
  timeout retries five times instead of ending the poll.
- **Fixed**: `returnToChat` no longer creates a second MainActivity instance; the
  wake lock is renewed while a task is watched.
- **Fixed**: `task_on` reads a task's own display from `am stack list` (a moved
  task used to appear under both displays and trigger pointless follows).

**Chinese**

- **Changed**：[CH]PhoneScreenPage[CH]VirtualScreen，[CH]。[CH] → [CH]：
  4 [CH]、1 [CH]，3 minute 31 secondDone。
- **Fix**：[CH]「[CH]…」——[CH] `finish` [CH]Back，Skip[CH]。
- **Fix**：[CH]File[CH]（[CH]File + fsync + [CH]，[CH] `.bak`），
  [CH]。
- **Fix**：and adbd Connectionat `ssl.SSLEOFError` [CH]Rebuild；readTimeout[CH]Retry 5 [CH]。
- **Fix**：`returnToChat` [CH] MainActivity [CH]；Wake[CH]。
- **Fix**：`task_on` [CH] `am stack list` [CH]（[CH]，
  [CH]）。

---

## 0.4.3 — 2026-11-20

`PhoneGo-0.4.3-arm64.apk` · SHA-256 `e0cef8e8d3a858eb1bd8ef0b263b82d8e43ee957e747eb648243e1ad80950f9c`

**English**

- **Fixed**: `Failed to connect to /127.0.0.1:8765` could still appear after
  0.4.2. The restart was gated on `AgentService.isReady()`, a flag that is set
  once and never cleared, so an agent that hung after starting looked healthy.
  The submission loop now restarts on ten refusals regardless of the flag, and
  `restart()` clears it before rebuilding.
- **Changed**: the failure message says the app already tried a restart.
- **Known gap**: if the agent hangs during a task, polling stops and the task is
  not resumed.

**Chinese**

- **Fix**：0.4.2 [CH] `Failed to connect to /127.0.0.1:8765`。Restart[CH]
  `AgentService.isReady()` above，[CH]、[CH]，Service[CH]。[CH]
  [CH] 10 [CH]Restart，`restart()` [CH]。
- **Changed**：FailedTipwillInstruction"[CH]AutoRestart[CH]"。
- **Known[CH]**：[CH]Service[CH]，[CH]Stop，[CH]Auto[CH]。

---

## 0.4.2 — 2026-11-19

`PhoneGo-0.4.2-arm64.apk` · SHA-256 `81be9339552c1757453b6f1733f2e1961894f2ac55832d8b6404ff4144ad0d54`

**English**

- **Fixed**: a finished task could leave an empty chat. The agent brings the chat
  forward when a task ends, and the window had no launch mode, so that start
  opened a second window which read the transcript before the first had saved it.
  The window is `singleTop` now and the transcript is flushed at once.
- **Fixed**: the session list dropped every conversation listed after the current
  one (their files stayed on disk). Talking in an older chat lost the newer ones.
- **Changed**: model settings is one provider row instead of five fields. Twelve
  providers plus **Custom**; base URL, model, vision model and step budget hide
  under Advanced; a pasted `sk-or-v1-…` / `sk-ant-…` key picks its provider; saving
  runs the connection test.
- **Changed**: [CH]Mode is now [CH] / "Never ask me about money". It only
  ever skipped the confirmation before money steps and destructive shell commands.
  It asks once before switching on, defaults to off, and a stored old value is
  reset once.

**Chinese**

- **Fix**：[CH]。[CH] agent [CH]，而Window[CH]Settings
  launchMode，[CH]Window——NewWindow[CH]，[CH]File。[CH]
  Windowis `singleTop`，[CH]。
- **Fix**：[CH]（File[CH]）。[CH]Message[CH]
  让Update[CH]。
- **Changed**：ModelSettings[CH]「[CH]」[CH]。12 [CH] + **Custom**；base URL、
  Model、[CH]Model、[CH]「AdvancedSettings」；Paste `sk-or-v1-…` / `sk-ant-…` willAuto[CH]；
  Save时AutoTestConnection。
- **Changed**：「[CH]Mode」[CH]「[CH]」。[CH]Skip[CH] shell [CH]Confirm。
  [CH]Open[CH]Confirm[CH]、DefaultClose，[CH]Reset[CH]。

---

## 0.4.1 — 2026-11-19

`PhoneGo-0.4.1-arm64.apk` · SHA-256 `0adc9c56162e54e4ea76ef0e8b3eb4009c5614ed0337be6092a2e49adf4811de`

**English**

- **Fixed**: a stalled agent now restarts itself. A heartbeat older than two
  minutes used to end with "swipe PhoneGo away from Recents"; the app stops and
  starts the local agent once and only asks you if that fails. `Failed to connect
  to 127.0.0.1:8765` means the app's own server is not up, and gets the same
  treatment.
- **Fixed**: the first message waits up to 100 s (it was 60) and restarts the
  agent once if it is still silent at 25 s.
- **Fixed**: "Test connection" no longer prints a raw Java exception; it restarts
  the agent and says to try again in ten seconds.
- **Added**: a `.sha256` file next to the APK. "There was a problem parsing the
  package" is almost always an incomplete download.

**Chinese**

- **Fix**：Lag[CH] agent [CH]Restart。[CH]，[CH]Tip"[CH]"；
  [CH]，[CH]Failed[CH]Manual[CH]。`Failed to connect to
  127.0.0.1:8765` Instruction App [CH]Service[CH]，[CH]。
- **Fix**：[CH]MessagewillRetry 100 second（[CH] 60），25 [CH]Restart[CH] agent。
- **Fix**：「TestConnection」[CH]Print Java [CH]，[CH]Restart并Tip[CH]。
- **Added**：APK [CH] `.sha256` File——「[CH]Issue」[CH]Download[CH]。

---

## 0.4.0 — 2026-11-17

`PhoneGo-0.4.0-arm64.apk` · SHA-256 `ca8d8d1fc2060d4a7b9a8fd07638eb9080a4fae31622e378c5efa91ab80bf6c5`

**English**

- **Added**: an English interface. Every label goes through one translation table
  (300 literals in the chat screen alone); resource strings are translated by a
  pass over the view tree.
- **Added**: Settings → Language — Follow system · Chinese · English. The app follows
  the phone's language by default.
- Notes: the agent's answers follow the language you type, and old chat history
  keeps the language it was written in.

**Chinese**

- **Added**：EnglishInterface。[CH]（[CH]Interface[CH] 300 处）；[CH]
  [CH]。
- **Added**：Settings → Language——[CH] · Chinese · English，Default[CH]PhoneLanguage。
- Instruction：agent [CH]Language[CH]InputLanguage；[CH]Message[CH]Language。

---

## 0.3.0 — 2026-11-17

`PhoneGo-0.3.0-arm64.apk` · SHA-256 `3003dbe08cfc8e5e2bf56cb2335a84977dffcd8d99b1ca67a43ffdc6b593cbee`

**English**

- **Added**: cross-app hand-over. What a subtask reads is carried into the next
  one; the search box prefers the name quoted in that report; each subtask opens
  its own app first; a step that must produce a name has to open an item and read
  its body. Measured: [CH] → note → 「[CH]」 → [CH], 49 steps, 200 s.
- **Added**: the phone comes back at the end of a task — the app returns to its own
  screen, a full-screen viewer is closed, the chat comes forward with the answer
  and one question about moving that page over.
- **Fixed**: false endings. Waiting stops at 20 minutes instead of six, a subtask's
  failure reason reaches the step list, a cold app gets six seconds to draw.
- **Fixed**: the start-up warm-up no longer opens other apps on the agent's display
  (it looked like the agent wandering off in a demo).
- **Fixed**: crawl leaks and crashes — the replaced display is released, shell
  calls have timeouts, the partial save no longer crashes.

**Chinese**

- **Added**：跨 App [CH]。[CH]Next；Search[CH]；
  [CH]Open[CH] App；[CH]Open[CH]。[CH]：[CH] → [CH]
  →「[CH]」→ [CH]，49 步 / 200 second。
- **Added**：[CH]Phone[CH]——[CH] App [CH]、[CH]View器、[CH]
  [CH]，[CH]Page[CH]。
- **Fix**：假Failed。Waiting[CH] 6 [CH] 20 [CH]，[CH]Failed[CH]，[CH] App
  Yes 6 [CH]。
- **Fix**：[CH]Virtual[CH]Open[CH] App（[CH] agent [CH]）。
- **Fix**：[CH]——[CH]Virtual[CH]、shell [CH]Timeout、[CH]Save[CH]。

---

## 0.2.0 — 2026-11-15

`PhoneGo-0.2.0-arm64.apk` · SHA-256 `ff842d55f5932e32d5ecd3cce6e666c9dac60c8ba7f52f976c3ee786e89c8453`

**English**

- First public build: the agent runs **inside** the phone and drives the target app
  on a virtual display, so the phone's own screen stays usable.
- Requirements: Android 14+, arm64, wireless debugging, the accessibility service
  (it reads the pairing code), and your own model API key.
- Added after the first upload: export/import a backup zip (pairing identity,
  maps, chats, model settings) so a reinstall does not start from zero.

**Chinese**

- [CH]Version：agent [CH]**Phone[CH]**，[CH]Virtual[CH] App，Phone[CH]Screen[CH]。
- [CH]：Android 14+、arm64、[CH]Debugging、[CH]Service（[CH]Pairing码），[CH]Model API Key。
- [CH]Upload[CH]：BackupExport/Import（Pairing[CH]、[CH]、[CH]、ModelSettings），[CH]Start。

---

## Where the details live / [CH]

Each release's full notes are on its release page — install steps, signing, the
measured numbers behind a change. [CH]Version[CH]Instruction[CH] release Page：Install[CH]、[CH]、
[CH]。

- Releases: <https://github.com/HKUDS/PhoneGo/releases>
- Manual for the current version: [docs/manual.md](docs/manual.md) · [Chinese](docs/manual.zh.md)
- First-run walkthrough: [docs/getting-started.md](docs/getting-started.md) · [Chinese](docs/getting-started.zh.md)
