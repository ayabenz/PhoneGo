English · [Chinese](getting-started.zh.md)

# Getting started

Ten minutes from a downloaded APK to a finished task. You need the phone itself
and a model API key — no computer, no cable.

> The interface follows the phone's language (English or Chinese); Settings →
> Language overrides it. Labels are quoted here in both.

## 1. Install

Download [`PhoneGo-0.4.4-arm64.apk`](https://github.com/HKUDS/PhoneGo/releases/download/phonego-v0.4.4/PhoneGo-0.4.4-arm64.apk)
and open it on the phone.

- **Android 14 or newer, arm64.** The Python runtime and the display helper are
  built for `arm64-v8a` only.
- Allow installation from this source. MIUI asks once — tap ContinueInstall (continue).
- Later releases install in place: every one is signed with the same key.

## 2. Turn on two switches

PhoneGo talks to the phone's own `adbd` over loopback, and it has to read the
pairing code out of the system dialog to do that. So the order matters:

1. **Developer options → Wireless debugging → on.**
2. **PhoneGo's accessibility service → on.** Long-press the 「Settings」 chip in the app
   to jump straight to the system page, or find it under
   Settings → Accessibility → PhoneGo.

Open the app. It pairs itself and starts the agent service; the chat says so when
the connection is up. If it says there is no pairing identity yet, turn on
wireless debugging and reopen the app — or press 「Pair Wireless Debugging」 in Settings.

> Why accessibility first: without it the app cannot read the six-digit pairing
> code, so it cannot pair; the agent can then only see screenshots, not the
> labels on screen.

## 3. Give it a model

Tap 「Settings」 → ModelSettings:

| Field | What to put |
|---|---|
| **Provider** | twelve to choose from — DeepSeek official, DeepSeek, OpenRouter, Zhipu, Alibaba Bailian, SiliconFlow, Moonshot Kimi, OpenAI, Gemini, Anthropic, local, custom. Picking one fills the base URL and model id |
| **API Key** | your own key. It is encrypted with a key in the Android Keystore and stays on the phone |
| **model / api base** | editable; any OpenAI- or Anthropic-compatible endpoint works. The base URL decides which protocol is spoken |
| **[CH]Model** | optional; leave empty to use the same model for screenshots |
| **[CH]** | default 35 — the budget for one task |

Saving runs the connection test for you; 「TestConnection」 re-runs it. Nothing is bundled: without a key
the agent refuses to run, and the chat says so.

## 4. First task

Start with something that needs no login, so you can watch the whole loop:

```
OpenSettings，[CH]Yes[CH] Wi-Fi
```

```
[CH]，[CH]，[CH]
```

The first takes seconds. The second is the cross-app example from the README:
two apps, a value carried from one to the other, and a price at the end.

What you should see: the step list growing in the chat, a thumbnail of the
agent's own screen in the corner, and finally an answer — plus one question,
whether to move the page it ended on over to your screen.

## 5. When something is off

| Symptom | What it is | Fix |
|---|---|---|
| 「[CH]YesPair Wireless Debugging，先Done[CH]Pairing」 | the app has no pairing identity yet | turn on wireless debugging, then reopen the app or press 「Pair Wireless Debugging」 |
| works, then stops after a reboot | Android turns wireless debugging off at boot | turn it back on; the app reconnects by itself |
| tasks die in the background | the system's cleaner reclaimed the app | allow background running and set battery saving to unrestricted (long-press 「Settings」) |
| the step list says [CH] instead of [CH] | this app has no map on this phone yet | expected — the map is built per app by crawling it; the vision fallback handles it meanwhile |
| an app only ever appears on your own screen | it refuses to run on the agent's display | expected: PhoneGo follows it there, then puts it back |

## 6. What it will not do

- **Spend money.** Paying, ordering and submitting stop and ask you first.
- **Type your passwords.** Password and verification-code screens are handed to
  you.
- **Work on every app out of the box.** Apps with a map replay fast; the rest go
  through the vision model, which is slower and costs tokens. Maps are built per
  app, on your phone, and can be rebuilt any time.

Next: [what the app is, layer by layer](product-app.md) ·
[how a map is compiled](map-building.md) ·
[recordings](showcase/)
