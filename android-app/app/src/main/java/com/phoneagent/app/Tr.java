package com.phoneagent.app;

import android.content.Context;
import android.content.SharedPreferences;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

/**
 * Chinese-to-English for the app's own text.
 *
 * The Chinese literal is the key, so the English UI cannot drift from what was
 * measured in Chinese: if a label changes, its translation disappears instead of
 * lying. Set in Settings → Language / Language, or follow the system locale.
 */
final class Tr {

    private static final Map<String, String> EN = new HashMap<>();

    private static SharedPreferences prefs;

    private Tr() {
    }

    static void attach(Context context) {
        prefs = context.getSharedPreferences("agent", Context.MODE_PRIVATE);
    }

    static boolean english() {
        String mode = prefs == null ? "system" : prefs.getString("lang", "system");
        if ("en".equals(mode)) {
            return true;
        }
        if ("zh".equals(mode)) {
            return false;
        }
        return !Locale.getDefault().getLanguage().startsWith("zh");
    }

    /** The app's text in the current language; unknown strings pass through. */
    static String t(String zh) {
        String en = EN.get(zh);
        return en == null || !english() ? zh : en;
    }

    static {
        put("Cancel", "Cancel");
        put("[CH]", "Build map");
        put("[CH]…", "Working…");
        put("你", "You");
        put("[CH]", "Maps");
        put("[CH]", "New chat");
        put("Delete", "Delete");
        put("Close", "Close");
        put("[CH]", "missing");
        put("[CH]", "Chats");
        put("Start", "Start");
        put(" · [CH] ", " · and ");
        put(" Home[CH] singleTask，", "'s home screen is declared singleTask, ");
        put("[CH]", "Got it");
        put("CancelFailed：", "Could not cancel: ");
        put("[CH]Phone", "Driving the phone");
        put("Input[CH]", "Type something");
        put("[CH]：[CH]「", "Map replay: go to \"");
        put(" 步）", " steps)");
        put("PhoneGo [CH]", "PhoneGo is starting");
        put("[CH]Debugging[CH]：adbd [CH]。[CH]「Settings → [CH] → [CH]Debugging」Open", "Wireless debugging is off: adbd is not listening. Open Settings → Developer options → Wireless debugging");
        put("PhoneGo [CH]Device[CH]", "PhoneGo cannot run on this device");
        put("PhoneGo [CH]", "PhoneGo is running");
        put("[CH]Cancel[CH]", "Cancelling the task");
        put("[CH]", "Floating view is showing");
        put("Stop[CH]", "Stop the task");
        put("Open PhoneAgent", "Open PhoneAgent");
        put("[CH] PhoneAgent", "Tap here to return to PhoneAgent");
        put("[CH]Open App", "The system does not let a floating view open the app");
        put("clickNotification[CH] PhoneAgent", "Tap the notification to return to PhoneAgent");
        put("[CH]Pairing[CH]Debugging，先Done[CH]Pairing。", "Wireless debugging is not paired yet. Pair it once first.");
        put("Pairing ", "Pairing ");
        put("[CH]PhonePairing（", "Pairing with the phone (");
        put("Python [CH]：", "Python is ready: ");
        put("\napp_map [CH]：", "\napp_map module: ");
        put("[CH]", "loaded");
        put("[CH]", "ok");
        put("Python [CH]Failed：", "Python failed to start: ");
        put("[CH]", "time unknown");
        put(" [CH]", " min ago");
        put(" [CH]", " h ago");
        put(" [CH]", " d ago");
        put("＋ [CH]", "+ New chat");
        put("[CH] · [CH]「[CH]」里", "New chat · what you had stays under Chats");
        put("[CH]，[CH]。", "A task is still running. Switch chats when it finishes.");
        put("Delete[CH]", "Delete this chat");
        put("Delete[CH]？", "Delete this chat?");
        put("[CH]，Phone[CH]。", "Only the chat log goes; maps and task results on the phone are untouched.");
        put("[CH]Screen数", "Max screens to crawl");
        put("[CH]（[CH]）", "Time budget (minutes)");
        put("[CH] · fromHome[CH]", "Max depth · taps from the home screen");
        put("[CH] ", "Re-crawl ");
        put("Delete[CH]？", "Delete this map?");
        put("\n\n[CH]Phone[CH]，[CH]。", "\n\nOnly the copy on this phone goes, and there is no undo.");
        put("[CH]Update", "Map updated");
        put("[CH]Failed：", "Map action failed: ");
        put("[CH]：", "Could not read the map list: ");
        put("[CH]。[CH]，[CH] App [CH]，[CH]Path。", "No maps yet. Once one is built, the same app's steps are recorded and replayed next time.");
        put("[CH]：[CH]Path[CH]，[CH]Page。", "Landings grade the map against itself: a few paths are replayed at random to see if they end where they were recorded.");
        put("＋ [CH]", "+ Build a new map");
        put("[CH]", "In use");
        put("[CH]", "Re-measure landings");
        put("Delete[CH]", "Delete map");
        put("Delete「", "Delete \"");
        put("」[CH]？\n", "\"'s map?\n");
        put("[CH] App [CH]。", "This app goes back to having no map.");
        put("Cancel[CH]", "Unpin");
        put("[CH]", "Pin");
        put(" Screen · ", " screens · ");
        put(" [CH]", " actions");
        put(" [CH]", " not reached");
        put(" [CH]", " maps for this package");
        put("[CH] 4/4", "landings 4/4");
        put("[CH]", "landings not measured");
        put("[CH]", "no navigation to measure");
        put("[CH] ", "Landings ");
        put("（[CH]）", " (older data)");
        put("[CH]「", "Re-measuring \"");
        put("」[CH]…", "\" landings…");
        put("[CH]Start[CH]：", "Could not start measuring: ");
        put("[CH]Failed：", "Measurement failed: ");
        put("」[CH] ", "\" landings ");
        put("[CH]Failed：", "Action failed: ");
        put("[CH] App…", "Reading the apps that can be crawled…");
        put("Local agent [CH] App，[CH]。", "The local agent has not listed any apps yet; try again shortly.");
        put("[CH] App [CH]：", "Could not read the app list: ");
        put("[CH]Screen数 · [CH]", "Max screens · the most this map may record");
        put("[CH]（[CH]）· [CH]", "Time budget (minutes) · stops when it runs out");
        put("[CH] · fromHome[CH]（1 = [CH]Home[CH]Page）", "Max depth · taps from the home screen (1 = only what the home screen lists)");
        put("[CH]", "Try once first");
        put("[CH]。[CH]：[CH]，", "It may not launch. One crawl tells you: it stops at once and remembers, ");
        put("[CH] ⛔。", "and marks it ⛔ next time.");
        put("试", "Try");
        put("[CH]", "Never mind");
        put("[CH] App [CH]", "This app cannot be crawled");
        put("[CH]Screen，Virtual[CH]。\n\n", "The system only puts it back on its own display; it will not start on the virtual one.\n\n");
        put("[CH] ✅  App。", "Pick an app marked ✅ instead.");
        put("Startfor「", "Starting a map for \"");
        put("」[CH]：[CH] ", "\": up to ");
        put(" Screen、", " screens, ");
        put(" [CH]。", " minutes.");
        put("[CH]，Done[CH]「[CH]」[CH]。", "Progress shows up here line by line; when it is done the map appears under Maps.");
        put("\n[CH]（[CH]Cancel）", "\nCrawling (tap to cancel)");
        put("[CH]Start：", "Could not start: ");
        put("[CH]Stop[CH]…（[CH]）", "Stopping the crawl… (what it reached is kept)");
        put("[CH] App", "This app");
        put("」Done：", "\" finished: ");
        put(" Screen", " screens");
        put("[CH]Save", "Map saved");
        put("，[CH] ", ", took ");
        put("。\n已Save，[CH]「[CH]」里View[CH]。", ".\nSaved — see it under Maps, or pin it for use.");
        put("」[CH]Done：", "\" did not finish: ");
        put("[CH]", "Needs you");
        put("PhoneGo [CH]", "PhoneGo needs a moment from you");
        put("[CH]…", "Resuming the last task…");
        put("[CH]", "Usage");
        put("[CH]：", "Could not read usage: ");
        put("[CH]", "Today");
        put("近 ", "Last ");
        put(" 天", " days");
        put("[CH]", "By day");
        put("[CH]", "By task");
        put("pressModel", "By model");
        put("Token [CH]", "Token usage");
        put("[CH]", "Collapse");
        put("api base（[CH] https://api.deepseek.com/v1）", "api base (e.g. https://api.deepseek.com/v1)");
        put("[CH]Model（[CH]）", "Vision model (empty = same as above)");
        put("[CH]（Default 35）", "Max steps per task (default 35)");
        put("DeepSeek [CH]", "DeepSeek (official)");
        put("[CH]", "Zhipu");
        put("[CH]", "Alibaba Bailian");
        put("[CH]", "SiliconFlow");
        put("Local", "Local");
        put("[CH]Connection", "Test connection");
        put("[CH]…", "Testing…");
        put("✅ [CH]：", "✅ Works: ");
        put("[CH]Mode：[CH]", "Autonomous: does not even ask before paying");
        put("[CH]：View[CH]", "Diagnostics: inspect the runtime");
        put("[CH]", "Runtime");
        put("[CH]", "not started");
        put("\n\n[CH]：", "\n\nheartbeat: ");
        put("[CH]Reconnect", "Reconnect now");
        put("[CH]Connection…", "Checking the connection…");
        put("ModelSettings", "Model settings");
        put("Save", "Save");
        put("Pairing[CH]Debugging", "Pair wireless debugging");
        put("[CH]", "no heartbeat yet");
        put(" [CH]（[CH]）", " s ago (ok)");
        put(" [CH]（[CH]Lag住）", " s ago (may be stuck)");
        put("[CH]API Key，agent [CH]Mode[CH]。", "Key cleared; the agent can only run in screenshot mode.");
        put("已Save，[CH]RestartLocal agent…", "Saved, restarting the local agent…");
        put("SaveFailed：", "Could not save: ");
        put("[CH]ModelAPI Key。click「Settings」[CH] API Key，[CH]。", "No model key yet. Open Settings and paste an API key, or tasks cannot run.");
        put("✅ [CH]Service[CH]（[CH] App AutoRestore）。", "✅ Accessibility service is ready (the app restores it at launch).");
        put("Tip：[CH]Service[CH]。[CH]，PhoneGo [CH]Pairing码，", "Note: the accessibility service is off. Without it PhoneGo cannot read the pairing code, ");
        put("agent [CH]（[CH]Tab[CH]）。", "and the agent can only use screenshots (no tapping by label).");
        put("\n[CH]「Settings」[CH]Open[CH]Settings页。", "\nLong-press Settings to open that page directly.");
        put("[CH]Pairing[CH]，[CH]Pairing[CH]Debugging。", "No pairing identity yet. Pair wireless debugging first.");
        put("[CH]Debugging[CH]Close，PhoneGo [CH] adbd。", "Wireless debugging is off, so PhoneGo cannot reach its own adbd.");
        put("\n[CH]「Settings → [CH] → [CH]Debugging」Open[CH]，[CH]。", "\nOpen Settings → Developer options → Wireless debugging, turn it on, then come back.");
        put("[CH]Local agent（[CH] adbd、[CH]VirtualScreen）…", "Starting the local agent (finding adbd, creating the display)…");
        put("[CH]Local agent Failed：\n", "Could not start the local agent:\n");
        put("[CH]Settings", "System settings");
        put("[CH]Service", "Accessibility service");
        put("BatteryOptimize（[CH]）", "Battery optimisation (background)");
        put("ExportBackup（含 API Key）", "Export backup (includes the API key)");
        put("ImportBackup", "Import backup");
        put("ExportBackup", "Export backup");
        put("[CH]Pairing[CH]、[CH]、[CH]ModelSettings[CH] zip，", "Packs the pairing identity, the maps, the chats and the model settings into one zip, ");
        put("[CH]「Download」Directory。\n\n", "saved to Downloads.\n\n");
        put("File[CH] API Key [CH]（[CH]，[CH]），", "The API key inside is plain text (on this phone it is encrypted and cannot be decrypted elsewhere), ");
        put("[CH]Share[CH]。", "so do not hand the file to anyone.");
        put("Export", "Export");
        put("[CH]ExportBackup…", "Exporting…");
        put("Backup已Saveto「Download」：", "Backup saved to Downloads: ");
        put("ExportFailed：", "Export failed: ");
        put("[CH]FileSelect器：", "Could not open the file picker: ");
        put("[CH]ImportBackup…", "Importing…");
        put("已Restore ", "Restored ");
        put(" File。[CH]Restart agent…", " files. Restarting the agent…");
        put("ImportFailed：", "Import failed: ");
        put("[CH]BatteryOptimize[CH]，[CH]。", "Battery optimisation is already off for PhoneGo; it can stay in the background.");
        put("[CH]BatterySettings，请Manualto「Settings → App → PhoneGo → [CH] → [CH]」。", "Could not open battery settings; set Settings → Apps → PhoneGo → Battery saver → Unrestricted.");
        put("Tip：[CH]DebuggingisClose，adbd [CH]。", "Note: wireless debugging is off and adbd is not listening.");
        put("\n[CH]「Settings → [CH] → [CH]Debugging」Open[CH]。", "\nOpen Settings → Developer options → Wireless debugging and turn it on.");
        put("Tip：BatteryOptimize[CH] PhoneGo。", "Note: battery optimisation may kill PhoneGo in the background.");
        put("\n[CH]「Settings」→「BatteryOptimize」[CH]。", "\nLong-press Settings → Battery optimisation to set it unrestricted.");
        put("[CH]Service", "Turn on the accessibility service first");
        put("Pairing[CH]PairingPopup里，[CH]Popup[CH]PairingService[CH]，", "The pairing code only exists in the system dialog, and closing it stops the pairing service, ");
        put("[CH] PhoneGo [CH]。\n\n", "so only PhoneGo itself can read it.\n\n");
        put("[CH]「Settings → [CH]」[CH] PhoneGo，[CH]Pairing。", "Open Settings → Accessibility, enable PhoneGo, then pair again.");
        put("Open[CH]Settings", "Open accessibility settings");
        put("请Open Settings → [CH] → [CH]Debugging → [CH]Pairing码PairingDevice。", "Turn on Settings → Developer options → Wireless debugging → Pair device with pairing code.");
        put("\nPairing[CH] PhoneGo [CH]，[CH]；Pop up[CH]Done。", "\nPhoneGo reads the code itself; you do not type it. Finish within two minutes of the dialog appearing.");
        put("[CH]PairingFailed：\n", "Could not start pairing:\n");
        put("WaitingLocal agent [CH]…", "Waiting for the local agent…");
        put("[CH]：[CH]ModelAPI Key，click「Settings」[CH] API Key。\n", "The task was not submitted: no model key yet. Open Settings and paste one.\n");
        put("Local agent [CH]：\n", "The local agent did not start:\n");
        put("agent [CH]，[CH]。", "The agent is still starting; give it ten seconds and try again.");
        put("PhoneGo [CH]Lag[CH]（", "PhoneGo's background process is stuck (");
        put(" [CH]）。", " s without a heartbeat).");
        put("\n[CH]，[CH]Open[CH]。", "\nSwipe it away from Recents and open it again.");
        put("Connection[CH]，[CH]Reconnect。", "The connection is fine; nothing to reconnect.");
        put("已Reconnect，[CH]Continue[CH]。", "Reconnected — carry on.");
        put("已AutoReconnect，[CH]Continue[CH]。", "Reconnected automatically — carry on.");
        put("ReconnectFailed：", "Reconnect failed: ");
        put("[CH] 20 [CH]，[CH]StopWaiting。", "This task has been running over 20 minutes, so I stopped waiting.");
        put("[CH]，[CH]「[CH]/[CH]」[CH]。", "It may still be running; the result shows up under Maps / Usage later.");
        put("[CH]：", "Needs your answer: ");
        put("Waiting[CH]…", "Waiting for your answer…");
        put("[CH] PhoneGo", "Reply to PhoneGo");
        put("已Cancel", "Cancelled");
        put("Done：", "Done: ");
        put("[CH]Done：", "Partly done: ");
        put("Failed：", "Failed: ");
        put("[CH]… 已Done ", "Working… ");
        put(" 步", " steps");
        put("[CH]Failed：", "Polling failed: ");
        put("[CH] ", "This run: ");
        put(" [CH] · Input ", " calls · in ");
        put(" · Output ", " · out ");
        put(" · [CH] ", " · map replays ");
        put(" 次", "");
        put("[CH]Cancel…", "Cancelling…");
        put("[CH]Failed：", "Could not send the answer: ");
        put("176 second", "176 s");
        put("Bluetooth macro ok (3/3 steps)", "Bluetooth macro ok (3/3 steps)");
        put("[CH]：[CH]「", "Routing: this step uses \"");
        put("」[CH]Screenabove", "\" and landed on your own screen");
        put("[CH]「", "Following \"");
        put("」[CH]ScreenaboveContinue", "\" onto your own screen");
        put("Input「", "Typing \"");
        put("[CH] App", "Target app");
        put("」[CH]Screenabove，[CH]VirtualScreen", "\" jumped to your screen; moved back to the virtual display");
        put("[CH]Page[CH]，[CH]PageContinue", "The screen differs from the map; continuing from what is on it");
        put("Model[CH]Page，[CH]Continuelook", "The model did not see the screen; taking another look");
        put("[CH]Page[CH]", "Checking the screen");
        put("[CH]Notification[CH]Interface，[CH]", "The notification shade was covering the screen; dismissed");
        put("[CH]Info", "Noted one item from the screen");
        put("[CH]：", "Noted: ");
        put("[CH]Path", "Known path");
        put("」 ", "\": ");
        put(" [CH]", " actions");
        put("（Done）", " (done)");
        put("Open App", "Open app");
        put("[CH]Path[CH]", "Follow the known path");
        put("[CH]", "Tap a number on the screenshot");
        put("[CH]Screen", "Tap the screen");
        put("[CH]Page", "Scroll");
        put("WaitingInterface[CH]", "Wait for the screen");
        put("Back[CH]", "Go back");
        put("[CH]", "Tap the text");
        put("[CH]「", "Tap \"");
        put("[CH]", "Run a command");
        put("[CH]：", "Run command: ");
        put("· [CH]Path[CH]（", "· follow the known path (");
        put("· [CH]Path[CH]「", "· follow the known path into \"");
        put("· [CH]", "· use the known map");
        put("· [CH]「", "· use the map for \"");
        put("」[CH]", "\"");
        put(" second", " s");
        put("[CH] [CH]", "Tap Recommended");
        put("[CH] ", "Tap ");
        put("Pairing", "Pair");
        put("PhoneAgent [CH]Pairing", "PhoneAgent is pairing");
        put("[CH]PairingPopup（[CH]Debugging里Open「[CH]Pairing码PairingDevice」）", "No pairing dialog seen (turn on \"Pair device with pairing code\" in Wireless debugging)");
        put("，[CH] agent", ", starting the agent");
        put("PhoneAgent Pairing[CH]", "PhoneAgent pairing result");
        put("发Message给 PhoneGo…", "Message PhoneGo…");
        put("[CH]", "Send");
        put("Settings", "Settings");
        put("Virtual[CH]", "Agent's screen");
        put("VirtualScreen · [CH]", "Agent's screen · tap to enlarge");
        put("Phone[CH] AI [CH]", "An AI assistant on your phone");
        put("[CH]Phone[CH]？", "What should your phone do?");
        put("[CH]，[CH]Continue用Phone", "It works on a separate screen in the background, so you keep using the phone");
        put("Open WLAN Settings", "Open WLAN settings");
        put("[CH]", "Weather in Shanghai tomorrow");
        put("OpenBluetoothSettings", "Open Bluetooth settings");
        put("⚡ Auto", "⚡ Auto");
        put("👁 [CH]", "👁 Vision");
        put("[CH]Phone", "How to drive the phone");
        put("[CH]Path，[CH]Screen", "With a map it follows the known path; otherwise it looks at the screen");
        put("[CH]，[CH]Screen", "No map: every step is decided from the screen");
        put("[CH]Auto：[CH]Path，Failed[CH]Screen", "Auto: known paths first, screen when they fail");
        put("[CH]：[CH]Screen", "Vision: every step is decided from the screen");
        put("[CH]Screen[CH]（[CH]）", "Drive your own screen (hands-off)");
        put("Open[CH]Screen[CH]，[CH]。[CH]、[CH] App [CH]。", "Operates on your screen so you can watch every step. Apps like JD or Taobao only run this way.");
        put("已Open[CH]：[CH]Screen[CH]", "Hands-off on: it operates on your own screen");
        put("已Close[CH]：[CH]VirtualScreen", "Hands-off off: back to the background display");
        put("[CH]Virtual[CH]，让 PhoneGo [CH]，[CH]。", "Reads the view tree of the agent's display so PhoneGo knows what each button is instead of tapping coordinates blindly.");
        put("VirtualScreen", "Agent's screen");
        put("[CH] · [CH] · [CH]", "Pinch to zoom · double-tap to enlarge · drag to pan");
        put("[CH]（共 %1$d 项）", "Show all (%1$d)");
        put("%1$d [CH]", "%1$d calls");
        put("VirtualScreen · 第 %1$d 步", "Agent's screen · step %1$d");
        put("[CH]（AutoOrder/Payment）", "Never ask me about money (auto-pay / auto-order)");
        put("Openback，[CH]Payment、Order、[CH]Order[CH]，[CH]。", "With this on, paying, ordering and submitting run without asking again.");
    }

    /** Translate every TextView under {@code root} that has a mapping. */
    static void apply(android.view.View root) {
        if (!english() || root == null) {
            return;
        }
        if (root instanceof android.widget.TextView) {
            android.widget.TextView tv = (android.widget.TextView) root;
            CharSequence text = tv.getText();
            if (text != null) {
                String mapped = EN.get(text.toString());
                if (mapped != null) {
                    tv.setText(mapped);
                }
            }
            CharSequence hint = tv.getHint();
            if (hint != null) {
                String mapped = EN.get(hint.toString());
                if (mapped != null) {
                    tv.setHint(mapped);
                }
            }
        }
        if (root instanceof android.view.ViewGroup) {
            android.view.ViewGroup group = (android.view.ViewGroup) root;
            for (int i = 0; i < group.getChildCount(); i++) {
                apply(group.getChildAt(i));
            }
        }
    }

    private static void put(String zh, String en) {
        EN.put(zh, en);
    }
}
