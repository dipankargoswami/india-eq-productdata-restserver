from datetime import date, timedelta


def get_nse_bhavcopy_filename():
    today = date.today()

    if today.isoweekday() == 1:
        today -= timedelta(days=3)
    elif today.isoweekday() == 7:
        today -= timedelta(days=2)
    else:
        today -= timedelta(days=1)

    date_str = today.strftime('%d%b%Y')
    return f'cm{date_str.upper()}bhav.csv'
