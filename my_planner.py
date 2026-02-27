from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import aladhan
import datetime
from hijridate import Gregorian


def wl(pdf, x, just_write=True):    # Write Line Arabic
    if just_write:
        pdf.cell(0, 10, a(x), new_x="RMARGIN", new_y="NEXT", align="R")
    else:
        pdf.cell(0, 10, x, new_x="RMARGIN", new_y="NEXT", align="R")



def a(x):    # ARABIZE
    reshaped_text = arabic_reshaper.reshape(x)
    bidi_text = get_display(reshaped_text)
    return(bidi_text)



def connectToPrayerService():

    # Create a client instance
    client = aladhan.Client()

    client = aladhan.Client()
    
    # Just tell it the city and the country!
    location = aladhan.City("Bloomington", "US", "Indiana")
    
    times = client.get_today_times(location)

    return (times)





def main():

    #ini
    pdf = FPDF()
    pdf.add_page()

    #gets the fonts
    pdf.add_font("Amiri", style="", fname="./fonts/Amiri/Amiri-Regular.ttf")

    #sets font and adds text
    pdf.set_font("Amiri", size=25)
    pdf.cell(0, 20, text='﷽', new_x="LMARGIN", new_y="NEXT", align='C')

    t = connectToPrayerService()

    pdf.set_font("Amiri", size=20)
    pdf.cell(0, 20, text=a('الواجبات'), new_x="LMARGIN", new_y="NEXT", align="R")

    for i in range(1, 15):
        pdf.rect(190, 45 + (i) * 15, 3, 3, style="")
        pdf.line(190, 50 + (i) * 15 , 100, 50 + (i) * 15)

    # PRAYER TIMES DISPLAY
    pdf.cell(0, 20, text=a('مواقيت الصلاة'), new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.set_font("Amiri", size=15)
    pdf.cell(0, 10, text=f'{t[0].readable_timing(show_date=False, _24h=True)}      ' + a('الصبح'), new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 10, text=f'{t[1].readable_timing(show_date=False, _24h=True)}      ' + a('الظهر'), new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 10, text=f'{t[2].readable_timing(show_date=False, _24h=True)}      ' + a('العصر'), new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 10, text=f'{t[3].readable_timing(show_date=False, _24h=True)}      ' + a('المغرب'), new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 10, text=f'{t[4].readable_timing(show_date=False, _24h=True)}      ' + a('العشاء'), new_x="LMARGIN", new_y="NEXT", align='L')


    pdf.set_font("Amiri", size=20)
    pdf.cell(0, 20, text='\n\n\n\n\n\n\n\n\n\n\n', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(0, 20, text=a('تاريخ اليوم  '), new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(0, 10, text=f'{str(Gregorian.today().to_hijri())}', new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 10, text=f'{str(Gregorian.today())}', new_x="LMARGIN", new_y="NEXT", align='L')
    

    pdf.output("tuto1.pdf") # output

if __name__ == '__main__':
    main()