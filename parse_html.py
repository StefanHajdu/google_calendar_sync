"""
    Table:
        html - ul
        css - class="olo-daynumbers-default olo-daynumbers"
    
    Days:
        html - li
        css - class="olo-number"

    Day value:
        html - a
    
    Color: 
        html - span
"""

from bs4 import BeautifulSoup


COLOR_CONTAINER = "color-container"

COLOR_ACTIONS = {
    "Zber SKLO": ["background-color: #008d26", 2],
    "Zber PLASTY": ["background-color: #ffff00", 5],
    "Zber BIO": ["background-color: #714d14", 4],
    "Zber PAPIER": ["background-color: #0000ff", 9],
}


def zeropad_int(n):
    return f"0{n}" if n < 10 else f"{n}"


def parse_html_response(html, **kwargs):
    soup = BeautifulSoup(html, "html.parser")

    data = []

    color_containers = soup.find_all("div", class_=COLOR_CONTAINER)

    for cc in color_containers:
        cc_day = int(cc.previous_sibling.get_text())
        for key, value in COLOR_ACTIONS.items():
            action = cc.find("span", attrs={"style": f"{value[0]}"})
            if action:
                data.append(
                    {
                        "summary": f"{key}",
                        "location": "Vráble",
                        "description": "Vyložiť do zajtra rána!",
                        "start": {
                            "dateTime": f"{kwargs['year']}-{zeropad_int(kwargs['month'])}-{zeropad_int(cc_day-1)}T17:00:00",
                            "timeZone": "Europe/Prague",
                        },
                        "end": {
                            "dateTime": f"{kwargs['year']}-{zeropad_int(kwargs['month'])}-{zeropad_int(cc_day)}T07:00:00",
                            "timeZone": "Europe/Prague",
                        },
                        "attendees": [
                            {"email": "stehajx@gmail.com"},
                            {"email": "anndreyca@gmail.com"},
                        ],
                        "colorId": f"{value[1]}",
                    }
                )

    return data
