English · [Chinese](errors.zh.md)

# Errors and what they mean

Look up the sentence you see on screen. Each entry says where it appears, what
it means, and what to do; the [manual](manual.md) covers the screens themselves.

Messages are grouped by when they appear. Anything the app prints verbatim is in
`backticks`.

---

## 1. Installing

### `There was a problem parsing the package`
**Where** the system installer, straight after you tap the APK.
**Means** the file is incomplete or corrupted — not that the app is broken.
**Do** compare the size with the release page (about 18 MB) and the SHA-256 next
to it, then download again over a stable connection, or push it with
`adb install`. Chinese systems say There was a problem parsing the package.

### Nothing installs, and the phone is Android 13 or older
**Means** the app needs **Android 14+ / arm64**.
**Do** there is no 32-bit or older-Android build.

---

## 2. Before the first task — pairing

### `[CH]YesPair Wireless Debugging，先Done[CH]Pairing。`
### `[CH]Yes[CH]Pairing[CH]，[CH]Pair Wireless Debugging。`
**Where** the chat, right after the app opens.
**Means** the app has no pairing identity yet, so it never starts the agent.
**Do** turn on **wireless debugging**, then in the app press **Pair Wireless Debugging**
(Settings) or reopen it. The code is read from the system dialog, so the
accessibility service has to be on first.

### `Wireless Debugging[CH]YesClose，PhoneGo [CH] adbd。`
**Means** `adb_wifi_enabled` is 0. Android switches it off on reboot and when the
Wi-Fi changes.
**Do** Settings → Developer options → Wireless debugging → on, then come back.
The app reconnects by itself.

### `没Yes[CH]PairingPopup（[CH]Wireless Debugging里Open「Pair with pairing code」）`
**Means** the pairing watcher never saw the system dialog with the six-digit
code.
**Do** open **Pair device with pairing code** in Wireless debugging, leave the
dialog up, and press **Pair Wireless Debugging** within two minutes.

### `Tip：Accessibility Service[CH]。没Yes它，PhoneGo None[CH]Pairing码，agent [CH]…`
**Means** exactly that. Pairing cannot read the code, and later the agent can
only tap coordinates, not labels.
**Do** long-press the Settings chip → Accessibility service, or Settings →
Accessibility → PhoneGo.

### `StartPairingFailed：…`
**Means** the pairing service could not start.
**Do** check wireless debugging is on and the accessibility service is enabled;
reopen the app and try once more.

---

## 3. Sending a task

### `Local agent 没Yes[CH]：java.net.ConnectException: Failed to connect to /127.0.0.1:8765`
**Where** the chat, after you press send.
**Means** `127.0.0.1:8765` is the app's **own** local agent. This is not your
network and not the model: the agent is not answering. Since 0.4.4 the
connection to the phone's own adbd is rebuilt once when it dies, so a dropped
socket no longer fails the task.
**Do** since 0.4.2 the app waits longer and restarts the agent once by itself;
if the message still appears, it says so in the same line. Then: make sure
wireless debugging is on, restart the app from Recents, and if it persists,
re-pair (see §2).

### `WaitingLocal agent [CH]…`
**Means** normal for the first 20–30 seconds after a start: the display is being
created.
**Do** nothing. It only becomes a problem if it stays for a minute or more.

### `[CH]：[CH]Yes[CH]ModelAPI Key，click「Settings」[CH] API Key。`
**Means** no key stored, so the task is refused rather than run without a model.
**Do** Settings → paste a key → **Save** (saving runs the connection test).

### `[CH] 20 [CH]，[CH]StopWaiting。`
**Means** the app stopped *waiting*, not the task. Using a model that streams
slowly or a long chain of apps can take that long.
**Do** the result still appears under Usage later; or re-run with a shorter
instruction.

---

## 4. While a task runs

### `PhoneGo [CH]Lag[CH]（N [CH]Yes[CH]）。`
**Means** the heartbeat file is older than two minutes — the interpreter froze or
was killed. Since 0.4.1 the app restarts it once automatically; if you see this,
that restart already failed.
**Do** swipe the app away from Recents and open it again.

### `[CH]Failed：…`
**Means** the app lost its connection to its own agent while watching a task.
**Do** reopen the app; if the task had already finished, its answer is under
**Usage**.

### A step line reads `no_ui: nothing readable on the agent's display`
**Means** the agent's screen was empty when a subtask started — usually the app
closed itself. 0.4.2 waits six seconds before believing it.
**Do** nothing on a current build; on older ones, re-run the task.

### A step ends with `— max_rounds`
**Means** the subtask used its whole step budget (default 35 per task, shared
between subtasks).
**Do** Settings → Advanced → raise **max steps per task** (5–80), or split the
instruction in two.

### A step ends with `— partial`, `— planner`, or `— handover`
**Means** the model stopped part-way, the planner could not map the instruction
to apps, or the task was handed back to you on purpose.
**Do** read the answer text: it names the step that failed. Re-running with a
simpler wording often gets through.

### `[CH] App N [CH]SecurityVerify（第 N 次）`
**Means** an app answered automation with a captcha, so **replay is skipped for
that app for seven days** — it will be driven by the vision loop instead, which
is slower and uses more tokens. Nothing is broken.
**Do** let it run in vision mode, or use another app. The mark expires on its
own.

### `[CH]「X」：[CH]Main Screen[CH] singleTask，[CH]Screen…`
**Means** that app cannot start on the agent's display at all.
**Do** pick another app, or use hands-off mode (Settings → "Drive your own
screen") so it runs on your display.

### `AdbError: not connected`
**Means** the app's connection to the phone's own `adbd` broke mid-task.
**Do** the app rebuilds the display by itself; if tasks keep failing, turn
wireless debugging off and on, then restart the app.

### `[CH]：` / `PhoneGo [CH]`
**Means** the task is paused on purpose — a captcha, a login, a choice, or a
question about spending money.
**Do** handle it on the phone and reply in the chat. Silence is treated as "no".

---

## 5. Model and key

### `❌ …` under **Test connection**
**Means** the provider refused the call.
**Do** read the detail: `401` is a wrong or expired key, `403` is a key without
access to that model, `404` is a wrong base URL or model id, and a timeout is the
network. The base URL decides the protocol: `…/v1` is OpenAI-style, `…/anthropic`
is Anthropic-style.

### `Local agent 没Yes[CH]，[CH]Restart；[CH]「TestConnection」。`
**Means** the test could not even reach the app's own agent — the model was
never asked.
**Do** wait ~15 s and test again; the agent is restarting.

### `[CH]API Key，agent [CH]Mode[CH]。`
**Means** you saved an empty key. Tasks cannot run without a model.
**Do** paste a key again.

---

## 6. Maps and crawling

### `[CH] App [CH]` / the app list shows ⛔
**Means** the app cannot start on the agent's display (see the singleTask entry
above); a crawl would record nothing.
**Do** choose another app, or run it hands-off.

### `[CH]：…`
**Means** the agent did not answer while the map library was opening.
**Do** reopen the Map chip; if it repeats, restart the app.

### The map is there but steps show 👁 instead of replay
**Means** this app has no usable map on this phone yet, or its map is marked for
the risk cooldown (§4).
**Do** build a map under Maps, or accept the slower vision path.

---

## 7. Where to look next

| If you want | Read |
|---|---|
| what a screen does | [manual.md](manual.md) |
| how to install and start | [getting-started.md](getting-started.md) |
| what changed between versions | [../CHANGELOG.md](../CHANGELOG.md) |

If the answer is not here, open an issue with the exact sentence from the screen
and what you had just done:
<https://github.com/HKUDS/PhoneGo/issues>
