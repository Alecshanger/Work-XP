"""Quest Log desktop launcher.

Opens QuestLog.html in its own window and gives it real file access:
progress is saved to questlog-save.json in this folder automatically,
with no browsers or permission prompts involved.

Run with:  pyw questlog.py   (or double-click "Quest Log.bat")
Requires:  pip install pywebview
"""
import os
import webview

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(APP_DIR, 'QuestLog.html')
SAVE_PATH = os.path.join(APP_DIR, 'questlog-save.json')
LEGACY_BACKUP = os.path.join(APP_DIR, 'questlog-backup.json')


class Api:
    def load_data(self):
        """Return the saved game JSON, falling back to a browser-exported
        backup on first run so existing progress carries over."""
        for path in (SAVE_PATH, LEGACY_BACKUP):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                continue
            except Exception:
                continue
        return None

    def save_data(self, data):
        """Atomically write the game JSON next to the app."""
        tmp = SAVE_PATH + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(data)
        os.replace(tmp, SAVE_PATH)
        return True


if __name__ == '__main__':
    webview.create_window(
        'Quest Log',
        HTML_PATH,
        js_api=Api(),
        width=1280,
        height=880,
        background_color='#12141a',
    )
    webview.start()
