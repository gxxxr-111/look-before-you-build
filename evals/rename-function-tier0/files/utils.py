from datetime import date

def fmt_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")
