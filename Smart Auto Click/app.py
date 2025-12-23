from ui import App
import threading

app = App()

threading.Thread(
    target=app.clicker.loop,
    daemon=True
).start()

app.mainloop()
