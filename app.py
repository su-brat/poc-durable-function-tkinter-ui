from tkinter import *
import time
import threading
import requests


def get_body_from_inputs():
    return {"firstDate": first_date_entry.get(), "lastDate": last_date_entry.get()}


class MonitorStatus:
    def __init__(self, status_query_uri) -> None:
        self.status_query_uri = status_query_uri

    def run(self):
        while True:
            response = requests.get(self.status_query_uri)
            if response.status_code == 200:
                response_body = response.json()
                status = response_body["runtimeStatus"]
                if status in ("Completed", "Failed"):
                    results = response_body.get("output", [])
                    results_output_label = Label(window, text="\n".join(results))
                    results_output_label.grid(row=6, column=1)
                    return
                time.sleep(30)
            else:
                return


def on_trigger():
    response = requests.post(url_entry.get(), get_body_from_inputs())
    if response.status_code == 202:
        response_body = response.json()
        status_query_uri = response_body["statusQueryGetUri"]
        monitor = MonitorStatus(status_query_uri=status_query_uri)
        monitor_thread = threading.Thread(target=monitor.run)
        monitor_thread.start()


window = Tk()
window.geometry("500x200")

url_label = Label(window, text="Enter function url")
url_label.grid(row=0, column=0)

url_entry = Entry(window)
url_entry.grid(row=0, column=1)

first_date_label = Label(window, text="Enter first date")
first_date_label.grid(row=1, column=0)

first_date_entry = Entry(window)
first_date_entry.grid(row=1, column=1)

last_date_label = Label(window, text="Enter last date")
last_date_label.grid(row=2, column=0)

last_date_entry = Entry(window)
last_date_entry.grid(row=2, column=1)

trigger_btn = Button(window, text="Trigger")
trigger_btn.grid(row=3, column=0)

status_label = Label(window, text="Status:")
status_label.grid(row=4, column=0)

results_label = Label(window, text="Task results:")
results_label.grid(row=5, column=0)


window.mainloop()
