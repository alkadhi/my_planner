from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import aladhan
import datetime
from datetime import date
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

    with pdf.local_context(fill_opacity=0.2):
        # Center the image on the page
        # pdf.w and pdf.h are page width/height; 100 is image width
        pdf.image("./background.png", x=(pdf.w-200), y=(pdf.h - 200), w=200)
    
    pdf.add_font('Amiri', fname='./fonts/Amiri/Amiri-Regular.ttf')
    pdf.set_font("Amiri", size=20)
    pdf.cell(w=0, h=10, text="﷽", align="C", 
         new_x="LMARGIN", new_y="NEXT")

    pdf.cell(w=0, h=10, text="work", align="R", 
         new_x="LMARGIN", new_y="TOP")

    # Now this prints on the SAME line but aligned right
    pdf.cell(w=0, h=10, text="prayer times", align="L", 
            new_x="LMARGIN", new_y="NEXT")

    pdf.output(f"tasks_{date.today()}.pdf") # output

if __name__ == '__main__':
    main()