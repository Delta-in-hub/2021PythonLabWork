from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font, ttk
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import requests
import json5
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import numpy as np
import seaborn

seaborn.set()

matplotlib.use("TkAgg")


keyInfo = "&key=2a3820bad6a94d4a891bfbe1dc469ffa&gzip=n"


def getCityId(cityName: str):
    r = requests.get(
        f"https://geoapi.qweather.com/v2/city/lookup?location={cityName}{keyInfo}")
    if(r.status_code == 200):
        res = json5.loads(r.content.decode())
        if res['code'] != '200':
            return None
        # print(res)
        return (res["location"][0]['name'], res["location"][0]['id'])
    else:
        return None


def getAirQuality(locationId: str):
    r = requests.get(
        f"https://devapi.qweather.com/v7/air/now?location={locationId}{keyInfo}")
    if(r.status_code == 200):
        res = json5.loads(r.content.decode())
        if res['code'] != '200':
            return None
        # print(res)
        # return (res["location"][0]['name'], res["location"][0]['id'])
        return res['now']
    else:
        return None


def getHistoryAqi(cityName: str):
    r = requests.get(
        f"https://geoapi.qweather.com/v2/city/lookup?lang=en&location={cityName}{keyInfo}")
    if(r.status_code == 200):
        res = json5.loads(r.content.decode())
        if res['code'] != '200':
            return None
        # print(res)
        adm1 = res["location"][0]['adm1']  # shenyang
        adm2 = res["location"][0]['adm2']  # liaoning
        fullCityName = str()
        if adm1 == adm2:
            fullCityName = adm1.lower()
            pass  # 直辖市
        else:
            fullCityName = adm1.lower() + "/" + adm2.lower()
            pass
        rcityid = requests.get(
            f"https://website-api.airvisual.com/v1/routes/china/{fullCityName}")

        cityid = json5.loads(rcityid.content.decode())['id']

        rHis = requests.get(
            f"https://website-api.airvisual.com/v1/cities/{cityid}/measurements")

        history = json5.loads(rHis.content.decode())['measurements']['daily']
        return history[len(history)-7: len(history)]
    else:
        return None


def creatMathPlot(cityName: str):
    res = getHistoryAqi(cityName)
    d = list()
    daqi = list()
    for i in res:
        d.append(str(i['ts']).split('T')[0])
        daqi.append(int(i['aqi']))

    fig = Figure(figsize=(7, 5), dpi=100)

    ax = fig.add_subplot()
    ax.plot(d, daqi)

    ax.set_title("AQI History 7 days", loc='center', pad=20,
                 fontsize='xx-large', color='red')  # 设置标题
    return fig


# from tkinter import *
# Explicit imports to satisfy Flake8
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("800x600")
window.configure(bg="#3973EF")


canvas = Canvas(
    window,
    bg="#3973EF",
    height=600,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    207.0,
    38.0,
    anchor="nw",
    text="空气质量查询",
    fill="#FFFFFF",
    font=("微软雅黑", 58 * -1)
)

canvas.create_rectangle(
    102.0,
    122.0,
    312.0,
    128.0,
    fill="#FFFFFF",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    400.0,
    246.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#DCDCDC",
    highlightthickness=0,
    font=("微软雅黑", 48 * -1)

)
entry_1.place(
    x=258.0,
    y=198.0,
    width=284.0,
    height=94.0,
)

# {'pubTime': '2021-10-18T19:00+08:00', 'aqi': '39', 'level': '1', 'category': '优', 'primary': 'NA', 'pm10': '39', 'pm2p5': '14', 'no2': '19', 'so2': '7', 'co': '0.4', 'o3': '48'}


def createNewWindow(air):
    width = 900
    height = 500
    style = ttk.Style()
    style.theme_use('clam')
    print(air)

    newWindow = tk.Toplevel(window)
    screen_width = newWindow.winfo_screenwidth()
    screen_height = newWindow.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    newWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
    newWindow.title("更新时间"+air['pubTime'])

    tree = ttk.Treeview(newWindow, height=180,
                        selectmode="extended")
    tree.heading('#0', text=air['name'], anchor='w')

    tree.insert('', tk.END, text='空气质量', iid=0, open=True)
    tree.insert('', tk.END, text='AQI', iid=1, open=True)
    tree.insert('', tk.END, text='首要污染物', iid=2, open=True)
    tree.insert('', tk.END, text='pm10', iid=3, open=True)
    tree.insert('', tk.END, text='pm2.5', iid=4, open=True)
    tree.insert('', tk.END, text='No2', iid=5, open=True)
    tree.insert('', tk.END, text='So2', iid=6, open=True)
    tree.insert('', tk.END, text='Co', iid=7, open=True)
    tree.insert('', tk.END, text='O3', iid=8, open=True)

    tree.insert('', tk.END, text=air['category'], iid=9, open=False)
    tree.move(9, 0, 0)

    tree.insert('', tk.END, text=air['aqi'], iid=10, open=False)
    tree.move(10, 1, 0)

    tree.insert('', tk.END, text=air['primary'], iid=11, open=False)
    tree.move(11, 2, 0)

    tree.insert('', tk.END, text=air['pm10'], iid=12, open=False)
    tree.move(12, 3, 0)

    tree.insert('', tk.END, text=air['pm2p5'], iid=13, open=False)
    tree.move(13, 4, 0)

    tree.insert('', tk.END, text=air['no2'], iid=14, open=False)
    tree.move(14, 5, 0)

    tree.insert('', tk.END, text=air['so2'], iid=15, open=False)
    tree.move(15, 6, 0)

    tree.insert('', tk.END, text=air['co'], iid=16, open=False)
    tree.move(16, 7, 0)

    tree.insert('', tk.END, text=air['o3'], iid=17, open=False)
    tree.move(17, 8, 0)

    # tree.grid(row=0, column=10)
    # tree.pack()

    canvas = FigureCanvasTkAgg(creatMathPlot(air['name']), master=newWindow)
    canvas.draw()
    # canvas.get_tk_widget().grid(row=0, column=0)
    canvas.get_tk_widget().pack(side=tk.LEFT)
    tree.pack(side=tk.RIGHT)
    # tree.grid(row=0, column=1)

    newWindow.focus()
    # newWindow.grab_set()


def main():
    cityName = entry_1.get()
    if not cityName:
        messagebox.showwarning("空气质量查询", "城市输入为空")
        return
    cityId = getCityId(cityName)
    if not cityId:
        messagebox.showwarning("空气质量查询", cityName + " Not Found")
        return
    air = getAirQuality(cityId[1])
    if not air:
        messagebox.showwarning("空气质量查询", cityName + " Not Found")
        return
    air['name'] = cityId[0]
    createNewWindow(air)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=main,
    relief="flat"
)
button_1.place(
    x=314.0,
    y=396.0,
    width=172.0,
    height=54.0
)
entry_1.focus()

window.resizable(False, False)
window.mainloop()
