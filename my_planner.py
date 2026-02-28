from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import aladhan
import datetime
from datetime import date
from hijridate import Gregorian
import calendar


def a(x):    # ARABIZE
    reshaped_text = arabic_reshaper.reshape(x)
    bidi_text = get_display(reshaped_text)
    return(bidi_text)


def read_tasks():

    tasks = {}
    day = {}
    i = 0

    with open("./tasks.txt", "r") as f:
        for line in f:
            if "`.`" in line:
                day[i] = tasks
                tasks = {}
                i += 1
            elif "~.~" in line:
                last_key = list(tasks)[-1]
                tasks[last_key].append(line.strip("\n")[3:])
            else:
                tasks[line.strip("\n")] = []
        if tasks:
            day[i] = tasks   
    return([i, day])


def page_lay(pdf, timeoffset):
    with pdf.local_context(fill_opacity=0.2):
        # Center the image on the page
        # pdf.w and pdf.h are page width/height; 100 is image width
        pdf.image("./background.png", x=(pdf.w-200), y=(pdf.h - 200), w=200)

    pdf.set_font("Amiri", size=20)
    pdf.cell(w=0, h=10, text="﷽", align="C", 
         new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Amiri", size=15)
    pdf.cell(w=0, h=10, text=a("الواجبات"), align="R", 
         new_x="LMARGIN", new_y="TOP")

    # Now this prints on the SAME line but aligned right
    pdf.cell(w=0, h=10, text=a("مواقيت الصلاة"), align="L", 
            new_x="LMARGIN", new_y="NEXT")

    cursor_pos_x = pdf.get_x()
    cursor_pos_y = pdf.get_y() 


    client = aladhan.Client()
    # 1. Calculate the specific date we want
    target_date = datetime.date.today() + datetime.timedelta(days=timeoffset)
    
    # 2. Define location
    location = aladhan.City("X", "Y", "Z")
    
    # 3. Fetch the time for the target month/year
    # This returns a list where each element is a day's Timings object
    times = client.get_calendar_times(
        location, 
        month=target_date.month, 
        year=target_date.year
    )
    _, num_days = calendar.monthrange(datetime.date.today().year, datetime.date.today().month)

    if (datetime.date.today().day + timeoffset) > num_days:
        n = ((timeoffset) * 5) - 5
    else:
        n = (((datetime.date.today().day + timeoffset)) * 5) - 5

    pdf.set_font("Amiri", size=14)
    pdf.cell(w=30, h=10, text=a("الصبح"), align="L", new_x="RIGHT", new_y="TOP")
    time_obj = datetime.datetime.strptime(times[n].readable_timing(), "%Y/%m/%d %I:%M (%p)")
    pdf.cell(w=30, h=10, text=f"{time_obj.hour:02}:{time_obj.minute:02}", align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.cell(w=30, h=10, text=a("الظهر"), align="L", new_x="RIGHT", new_y="TOP")
    time_obj = datetime.datetime.strptime(times[n + 1].readable_timing(), "%Y/%m/%d %I:%M (%p)")
    pdf.cell(w=30, h=10, text=f"{time_obj.hour:02}:{time_obj.minute:02}", align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.cell(w=30, h=10, text=a("العصر"), align="L", new_x="RIGHT", new_y="TOP")
    time_obj = datetime.datetime.strptime(times[n + 2].readable_timing(), "%Y/%m/%d %I:%M (%p)")
    pdf.cell(w=30, h=10, text=f"{time_obj.hour:02}:{time_obj.minute:02}", align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.cell(w=30, h=10, text=a("المغرب"), align="L", new_x="RIGHT", new_y="TOP")
    time_obj = datetime.datetime.strptime(times[n + 3].readable_timing(), "%Y/%m/%d %I:%M (%p)")
    pdf.cell(w=30, h=10, text=f"{time_obj.hour:02}:{time_obj.minute:02}", align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.cell(w=30, h=10, text=a("العشاء"), align="L", new_x="RIGHT", new_y="TOP")
    time_obj = datetime.datetime.strptime(times[n + 4].readable_timing(), "%Y/%m/%d %I:%M (%p)")
    pdf.cell(w=30, h=10, text=f"{time_obj.hour:02}:{time_obj.minute:02}", align="L", new_x="LMARGIN", new_y="NEXT")


    today = datetime.date.today() + datetime.timedelta(days=timeoffset)

    g = Gregorian(today.year, today.month, today.day)
    h = g.to_hijri()

    # Get the components
    h_day = h.day
    h_month = h.month_name(language='ar')
    h_year = h.year

    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_y(-15)
    pdf.cell(w=0, h=0, text=str(today), align="L", new_x="RIGHT", new_y="TOP")
    pdf.cell(w=0, h=0, text=f"{h_day} {a(h_month)} {h_year}", align="R", new_x="RIGHT", new_y="NEXT")

    pdf.set_xy(cursor_pos_x, cursor_pos_y)



def main():

    #ini
    pdf = FPDF()

    pdf.add_font('Amiri', fname='./fonts/Amiri/Amiri-Regular.ttf')
    pdf.add_font('Noto Sans Symbols', fname='./fonts/Noto_Sans_Symbols/NotoSansSymbols-VariableFont_wght.ttf')
  
    dt = read_tasks()
    pdf.set_font("Amiri", size=12)

    for ds in range(0, dt[0]+1):
        # DAY

        pdf.add_page()
        page_lay(pdf, ds)

        for key in dt[1][ds].keys():
            #TASK
            pdf.set_font("Noto Sans Symbols", size=12)
            pdf.cell(w=pdf.w-20, h=10, text="⏍", align="R", 
                new_x="LMARGIN", new_y="TOP")

            pdf.set_font("Amiri", size=12)
            pdf.cell(w=pdf.w-27.5, h=10, text=a(key), align="R", 
                new_x="LMARGIN", new_y="NEXT")

            if dt[1][ds][key]:
                for i in dt[1][ds][key]:
                    pdf.set_font("Noto Sans Symbols", size=12)
                    pdf.cell(w=pdf.w-35, h=10, text="⌂", align="R", 
                        new_x="LMARGIN", new_y="TOP")

                    pdf.set_font("Amiri", size=12)
                    pdf.cell(w=pdf.w-40, h=10, text=a(i), align="R", 
                        new_x="LMARGIN", new_y="NEXT")


    pdf.output(f"tasks_{date.today()}.pdf") # output

if __name__ == '__main__':
    main()