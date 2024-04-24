from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser
import matplotlib.pyplot as plt
import matplotlib
import time
import pygame.mixer
## part 4 color selection
## part 5 price duration. repayment(i,month,price) <= income
##        duration options. meanwhile recommend earliest month
## part 6 curve
## part 7 ?
def play_sound_effect():
    pygame.mixer.Sound('sound_effect.wav').play()

def play_bgm1():
    pygame.mixer.music.load('bgm1.mp3')
    pygame.mixer.music.play(-1)  # -1 means endless loop

def play_bgm2():
    pygame.mixer.music.load('bgm2.mp3')
    pygame.mixer.music.play(-1)  # -1 means endless loop

def play_bgm0():
    pygame.mixer.music.load('bgm0.mp3')
    pygame.mixer.music.play(-1)  # -1 means endless loop

def play_bgm3():
    pygame.mixer.music.load('bgm3.mp3')
    pygame.mixer.music.play(-1)  # -1 means endless loop
def play_bgm4():
    pygame.mixer.music.load('bgm4.mp3')
    pygame.mixer.music.play(-1)  # -1 means endless loop

def play_bgm5():
    pygame.mixer.music.load('bgm5.mp3')
    pygame.mixer.music.play(-1)  # -1 means endless loop
def play_bgmfinal():
    pygame.mixer.music.load('bgmfinal.mp3')
    pygame.mixer.music.play(-1)  # -1 means endless loop

def stop_bgm():
    pygame.mixer.music.stop()

    
def duration():#part 5
    try:
        duration = Toplevel()
        duration.title('How long is your preferred payment duration')
        duration.geometry('850x500')
        car_type = type_car.get()  # Get the selected car type from the previous window
        #cartype=StringVar()
        #cartype.set(type_car.get())


        subframe_duration = ttk.Frame(duration, padding="30 30 100 100")
        subframe_duration.grid(column=0, row=0, sticky=(N, W, E, S))
        subframe_duration.columnconfigure(0, weight=1)
        subframe_duration.rowconfigure(0, weight=1)
        ttk.Label(subframe_duration, textvariable=car_type).grid(column=1, row=2, sticky=(W, E))        
        ttk.Label(subframe_duration, text=f'You selected a {car_type}', font=('Arial', 14)).grid(column=1, row=1, sticky=W)
        ttk.Label(subframe_duration, text="You can choose the months that you pay:", font=('Arial', 14)).grid(column=1, row=3, sticky=W)



        def cash_flow(price,i=0.1,month=1,first=0.3):
            month=int(month)
            first=float(first)
            if month>=1:
                x=0
                for j in range(1,month+1):
                    x+=(1+i/12)**(-1*j)
                month_pay=(price-first*price)/(x)
            elif month==0:
                month_pay=0
                first=1
            total_pay=month_pay*month+first*price
            return month_pay, total_pay
 
        def gen_button(k):
            listk=[1,2,3,4,5,6,7,8,9,10,11,12,15,18,21,24,30,36,48,60,72,84,96,108,120]
            values = [str(i) for i in listk if i <= k]
            combo_var = StringVar()
            combobox = ttk.Combobox(subframe_duration, textvariable=combo_var,values=values)
            combobox['values'] = values
            combobox.grid(column=1, row=5, sticky=W)
            global selected_month
            selected_month=0
            
            result_label = ttk.Label(subframe_duration, text="")
            result_label.grid(column=1, row=6, sticky=W )
            def on_select(event):
                global selected_month
                try:
                    selected_month = combo_var.get()
                    i1=float(selected_month)//12
                    i2=float(selected_month)%12
                    if i1>0 and i2>0:
                        text1='Your payment duration is '+str(int(i1))+' year(s) and '+str(int(i2))+' month(s)'
                        result_label.config(text=text1)
                    elif i1==0 and i2>0:
                        text1='Your payment duration is '+str(int(i2))+' month(s)'
                        result_label.config(text=text1)
                    else:
                        text1='Your payment duration is '+str(int(i1))+' year(s) '
                        result_label.config(text=text1)
                    if float(selected_month)>k:
                        text1='Your payment duration is has exceeded the maximum deadline, please select in the table'
                        result_label.config(text=text1,wraplength=300)
                except:
                        text1='your input is invalid, please input an integer'
                        result_label.config(text=text1)

            combobox.bind("<FocusOut>", on_select)

        def get_down(total_price,k):
            downlist=[1,0.95,0.9,0.85,0.8,0.75,0.7,0.65,0.6,0.55,0.5,0.4,0.3,0.2,0.1, 0]
            # values2 = [str(i) for i in downlist if i >= k]
            values2 = ["{:.0%}".format(i) for i in downlist if i >= k]
            combo_var2 = StringVar()
            combobox2 = ttk.Combobox(subframe_price, textvariable=combo_var2,state="readonly")
            combobox2['values'] = values2
            combobox2.grid(column=1, row=5, sticky=W)
            global selected_down
            selected_down=0

            
            result_label2 = ttk.Label(subframe_price, text="")
            result_label2.grid(column=1, row=6, sticky=W )
            def on_select2(event):
                global selected_down
                selected_down = combo_var2.get()
                
                selected_down=float(selected_down.strip('%')) / 100.0
           
                # i3=1-float(selected_down)#
                i3 = 1 - float(selected_down)
                if (selected_down*total_price)>total_net:
                    text2='WARNING! Your down payment is over your asset net! Please reselect.'
                    result_label2.config(text=text2, wraplength=250, foreground="red")
                else:
                    text2='You choose to pay S$'+ str(int(selected_down*total_price))+' as down payment and S$'+str(int(total_price*i3))+' as loan'
                    result_label2.config(text=text2,wraplength=250, foreground="black")
                    
            combobox2.bind("<<ComboboxSelected>>", on_select2)

        subframe_price = ttk.Frame(duration, padding="30 30 100 100")
        subframe_price.grid(column=1, row=0, sticky=(N, W, E, S))
        subframe_price.columnconfigure(0, weight=1)
        subframe_price.rowconfigure(0, weight=1)
        ttk.Label(subframe_price, textvariable=car_type).grid(column=1, row=3, sticky=(W, E))
        
        ttk.Label(subframe_price, text="You can choose the down payment ratio:", font=('Arial', 14)).grid(column=1, row=4, sticky=W)
        

        if car_type == "BYD Atto 3 Electric":
            carprice= 215888
            gen_button(120)
            interest=0.12
            get_down(carprice,0)
        elif car_type == "BYD Dolphin Electric":
            carprice= 163888
            gen_button(120)
            interest=0.12
            get_down(carprice,0)
        elif car_type == "BYD T3 Electric":
            carprice= 124097
            gen_button(120)
            interest=0.14
            get_down(carprice,0)
        elif car_type == "Toyota Camry Hybrid":
            carprice= 242888
            gen_button(120)
            interest=0.12
            get_down(carprice,0)
        elif car_type == "Toyota Land Cruiser Prado":
            carprice= 314988
            gen_button(120)
            interest=0.11
            get_down(carprice,0)
        elif car_type == "Toyota Alphard":
            carprice= 351416
            gen_button(120)
            interest=0.11
            get_down(carprice,0)
                     
        elif car_type == "Mercedes-Benz GLA-Class":
            carprice= 446888
            gen_button(120)
            interest=0.1
            get_down(carprice,0)
        elif car_type == "Mercedes-Benz V-Class Diesel":
            carprice= 588988
            gen_button(120)
            interest=0.09
            get_down(carprice,0)
        elif car_type == "Mercedes-Benz G-Class Diesel":
            carprice= 700988
            gen_button(120)
            interest=0.08
            get_down(carprice,0)
                
        elif car_type == "Rolls-Royce Ghost Series II F1 Auto Edition":
            carprice= 1522988
            gen_button(120)
            interest=0.07
            get_down(carprice,0)
        elif car_type == "Rolls-Royce Ghost F1 Auto Edition":
            carprice= 1775988
            gen_button(120)
            interest=0.07
            get_down(carprice,0)
        elif car_type == "Rolls-Royce Cullinan F1 Auto Cars Edition":
            carprice= 1992988
            gen_button(120)
            interest=0.06
            get_down(carprice,0)
        elif car_type == "Rolls-Royce Ghost F1 Auto Edition":
            carprice= 1775988
            gen_button(120)
            interest=0.07
            get_down(carprice,0)
        elif car_type == "Rolls-Royce Cullinan F1 Auto Cars Edition":
            carprice= 1992988
            gen_button(120)
            interest=0.06
            get_down(carprice,0)    
        elif car_type == "Aima Electric Motorcycle":
            carprice= 1288.88
            gen_button(120)
            interest= 0.06
            get_down(carprice,0)
        elif car_type == "Aima Mini Plus":
            carprice= 1666.67
            gen_button(120)
            interest= 0.06
            get_down(carprice,0) 
        else:
            carprice= 2000
            gen_button(120)
            interest=0.06
            get_down(carprice,0)
        



        ttk.Label(subframe_price, text=f"Your total car price is S${format(carprice, ',.2f')}", font=('Arial', 14)).grid(column=1, row=2, sticky=W)
        def button5(*args):
            text0='                                                                                                                '
            button5_label=ttk.Label(duration, text="")
                
            button5_label.grid(columnspan=2, row=2)
            try:
                button5_label.config(text=text0,wraplength=255)  
                month_pay,total_pay=cash_flow(price=carprice,i=interest,month=selected_month,first=selected_down)
                #print(selected_month,selected_down)

                
                n1="{:,.2f}".format(month_pay)
                n2="{:,.2f}".format(total_pay)
                if month_pay>month_net:
                    text3="WARNING! Your month payment is over your monthly income net. Please reselect the no. of months above."
                            
                    button5_label.config(text=text3,wraplength=250, foreground="red")

                    
                else:
                    text4=f'You need to pay S${n1} every month'+f' and your total payment is S${n2}'
                    button5_label.config(text=text4,wraplength=250)   
                    stop_bgm()
                    play_bgmfinal()
               
            except ValueError:
                button5_label.config(text=text0,wraplength=450) 
                text5="Please review your inputs, only numerical values are allowed."
                button5_label.config(text=text5,wraplength=250) 

       

        # part 6
        matplotlib.use("TkAgg")
        def plot_total_pay_vs_month():
            try:
                plt.figure(figsize=(10, 6))
                for _j in range(3):
                    p_total_pays = []
                    for month in month_list:
                        p_month_pay, p_total_pay = cash_flow(p_carprice[_j],p_interest[_j],month,selected_down)
                        p_total_pays.append(p_total_pay)
                    plt.plot(month_list,p_total_pays,label = f'{p_name[_j]}')

                plt.xlabel('Month')
                plt.ylabel('Total Payment')
                plt.title('Total Payment vs. Month')
                plt.legend()
                plt.grid(True)
                plt.show()
            except:
                pass

        def plot_total_pay_vs_ratio():
            try:
                plt.figure(figsize=(10, 6))
                for _j in range(3):
                    p_total_pays = []
                    for p_ratio in ratio_list:
                        p_month_pay, p_total_pay = cash_flow(p_carprice[_j],p_interest[_j],selected_month,p_ratio)
                        p_total_pays.append(p_total_pay)
                    plt.plot(ratio_list,p_total_pays,label = f'{p_name[_j]}')

                plt.xlabel('Down payment ratio')
                plt.ylabel('Total Payment')
                plt.title('Total Payment vs. Down payment ratio')
                plt.legend()
                plt.grid(True)
                plt.show()
            except:
                pass

        car_type_dict = {"BYD":{"name":["Atto 3","Dolphin","T3"],"carprice":[215888,163888,124097],"interest":[0.12,0.12,0.14]},"Toyota":{"name":["Toyota Camry Hybrid","Toyota Land Cruiser Prado","Toyota Alphard"],"carprice":[242888,314988,351416],"interest":[0.12,0.11,0.11]},\
                         "Mercedes":{"name":["GLA-Class","V-Class Diesel","G-Class Diesel"],"carprice":[446888,588988,700988],"interest":[0.1,0.09,0.08]},"Rolls-Royce":{"name":["Ghost Series II F1 Auto Edition","Ghost F1 Auto Edition","Cullinan F1 Auto Cars Edition"],"carprice":[1522988,1775988,2332988],"interest":[0.07,0.07,0.06]}}
        car_type = type_car.get()
        for _i in car_type_dict:
            if _i in car_type:
                p_carprice = car_type_dict[_i]["carprice"]
                p_interest = car_type_dict[_i]["interest"]
                p_name = car_type_dict[_i]["name"]
            else:
                pass
        month_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,15,18,21,24,30,36,48,60,72,84,96,108,120]
        ratio_list = [1,0.95,0.9,0.85,0.8,0.75,0.7,0.65,0.6,0.55,0.5,0.4,0.3,0.2,0.1]

        
        ttk.Button(duration, text='calculate Payment',command=button5).grid(row=1,columnspan=2)
        ttk.Label(duration, text="_________________________________________________________________________________________", font=('Arial', 14)).grid(row=6, columnspan=3)
        ttk.Label(duration, text="After sucessfully calculating, you may view comparison reports of the different models of your chosen car brand", font=('Arial', 14)).grid(row=7, columnspan=2)

        ## Code below is for enabling the graph buttons only when "calculate payment" button is clicked
        # Add the code for initializing and enabling the graph buttons
        pay_vs_month_button = ttk.Button(duration, text='pay_vs_month', command=plot_total_pay_vs_month, state="disabled")
        pay_vs_month_button.grid(row=8, column=0)
        pay_vs_ratio_button = ttk.Button(duration, text='pay_vs_ratio', command=plot_total_pay_vs_ratio, state="disabled")
        pay_vs_ratio_button.grid(row=8, column=1)

        # Add this function to enable the buttons when 'calculate Payment' is pressed
        def enable_graph_buttons():
            pay_vs_month_button['state'] = 'normal'
            pay_vs_ratio_button['state'] = 'normal'

        # Update the 'calculate Payment' button to call the enable_graph_buttons function
        ttk.Button(duration, text='calculate Payment', command=lambda: [button5(), enable_graph_buttons()]).grid(row=1, columnspan=2)


        duration.mainloop()


    except:
        pass
    
def color():# part 4
    try:
        brand4 = Toplevel()
        brand4.title('Which color do you prefer?')
        brand4.geometry('500x525')
        car_type = type_car.get()  # Get the selected car type from the previous window
        #cartype=StringVar()
        #cartype.set(type_car.get())


        subframe_brand4 = ttk.Frame(brand4, padding="30 30 60 60")
        subframe_brand4.grid(column=0, row=0, sticky=(N, W, E, S))
        subframe_brand4.columnconfigure(0, weight=1)
        subframe_brand4.rowconfigure(0, weight=1)
        ttk.Label(subframe_brand4, textvariable=car_type).grid(column=2, row=2, sticky=(W, N))        
        ttk.Label(subframe_brand4, text=f'You selected a {car_type}', font=('Arial', 14)).grid(column=2, row=1, sticky=N)
        ttk.Label(subframe_brand4, text="Please select your preferred color:", font=('Arial', 14)).grid(column=2, row=3, sticky=N)

        # Create Radiobuttons for color selection
        color_var = StringVar()
        color_options = []  
       
        # Define color options for specific car models
        if car_type == "BYD Atto 3 Electric":
            color_options = ["Red", "Blue", "White"]
            color_files = ["BYD_Atto3_red.jpg", "BYD_Atto3_blue.jpg", "BYD_Atto3_white.jpg"]
        elif car_type == "BYD Dolphin Electric":
            color_options = ["Blue", "White", "Pink"]
            color_files = ["BYD_Dolphin_blue.jpg", "BYD_Dolphin_white.jpg", "BYD_Dolphin_pink.jpg"]
        elif car_type == "BYD T3 Electric":
            color_options = ["White", "Silver"]
            color_files = ["BYD_T3_white.jpg", "BYD_T3_silver.jpg"]
        
        elif car_type == "Toyota Camry Hybrid":
            color_options = ["Red", "Blue", "White"]
            color_files = ["Toyota_Camry_red.jpg", "Toyota_Camry_blue.jpg", "Toyota_Camry_white.jpg"]
        elif car_type == "Toyota Land Cruiser Prado":
            color_options = ["Black", "Silver", "White"]
            color_files = ["Toyota_Cruiser_black.jpg", "Toyota_Cruiser_silver.jpg", "Toyota_Cruiser_white.jpg"]
        elif car_type == "Toyota Alphard":
            color_options = ["Black", "Blue", "White"]
            color_files = ["Toyota_Alphard_black.jpg", "Toyota_Alphard_blue.jpg", "Toyota_Alphard_white.jpg"]
                     
        elif car_type == "Mercedes-Benz GLA-Class":
            color_options = ["Black", "Red", "White"]
            color_files = ["Mercedes_GLA_black.jpg", "Mercedes_GLA_red.jpg", "Mercedes_GLA_white.jpg"]
        elif car_type == "Mercedes-Benz V-Class Diesel":
            color_options = ["Black", "Grey", "White"]
            color_files = ["Mercedes_V_black.jpg", "Mercedes_V_grey.jpg", "Mercedes_V_white.jpg"]
        elif car_type == "Mercedes-Benz G-Class Diesel":
            color_options = ["Black", "Red", "White"]
            color_files = ["Mercedes_G_black.jpg", "Mercedes_G_red.jpg", "Mercedes_G_white.jpg"]
                
        elif car_type == "Rolls-Royce Ghost Series II F1 Auto Edition":
            color_options = ["Black", "Blue", "Red"]
            color_files = ["Rolls_Ghost_II_black.jpg", "Rolls_Ghost_II_blue.jpg", "Rolls_Ghost_II_red.jpg"]
        elif car_type == "Rolls-Royce Ghost F1 Auto Edition":
            color_options = ["Black", "Grey", "White"]
            color_files = ["Rolls_F1_black.jpg", "Rolls_F1_grey.jpg", "Rolls_F1_white.jpg"]
        elif car_type == "Rolls-Royce Cullinan F1 Auto Cars Edition":
            color_options = ["Black", "Blue", "Red"]
            color_files = ["Rolls_Cullinan_black.jpg", "Rolls_Cullinan_blue.jpg", "Rolls_Cullinan_red.jpg"]
        
        elif car_type == "Aima Electric Motorcycle":
            color_options = ["Black", "Red", "White"]
            color_files = ["Aima_E_Motor_black.jpg", "Aima_E_Motor_red.jpg", "Aima_E_Motor_white.jpg"]
        elif car_type == "Aima Mini Plus":
            color_options = ["Blue", "Green", "Pink"]
            color_files = ["Aima_Mini_blue.jpg", "Aima_Mini_green.jpg", "Aima_Mini_pink.jpg"]
        else:
            color_options = ["Black", "Joint", "White"]
            color_files = ["Aima_Max_black.jpg","Aima_Max_joint.jpg","Aima_Max_white.jpg"]
            
        
        image_label = ttk.Label(subframe_brand4)
        image_label.grid(column=2, row=len(color_options)+3, columnspan=2, sticky=(E, S), padx=(0, 20), pady=(0, 20))

        # Checker if radio button is selected to activate next screen
        radio_button_selected = BooleanVar()
        radio_button_selected.set(False)

        def check_radio_selection():
            if color_var.get():
                radio_button_selected.set(True)
                next_button.config(state="active")
            else:
                radio_button_selected.set(False)
                next_button.config(state="disabled")

        color_var.trace_add("write", lambda name, index, mode: check_radio_selection())

        next_button = ttk.Button(brand4, text='Next', command=duration)
        next_button.grid(row=13, column=0, padx=1, pady=1)
        next_button.config(state="disabled") 

        #Function for showing Image
        def show_car_image():
            selected_color = color_var.get()
            # Get the corresponding file name for the selected color
            image_index = color_options.index(selected_color)
            image_path = color_files[image_index]  # Use the file name based on the selected color
            try:
                image = Image.open(image_path)
                image = image.resize((280, 210), Image.ANTIALIAS)  # Resize the image if necessary #Use LANCZOS for Macbook
                img = ImageTk.PhotoImage(image)
                image_label.config(image=img)
                image_label.image = img  # Keep a reference to the image to prevent garbage collection
            except FileNotFoundError:
                # Handle the case when the image file is not found
                image_label.config(text="Image not found")

        for i, color_option in enumerate(color_options):
            ttk.Radiobutton(subframe_brand4, variable=color_var, value=color_option, text=color_option,
                            command=show_car_image).grid(column=1, row=i + 4, sticky=W)     
      
        show_car_image()  # Show the default image

    ########       
        brand4.mainloop()
    except ValueError:
        pass


def brand_choose():#the 3rd part
    stop_bgm()
    try:
        selected_brand = brand1.get()  # Get the selected brand from the previous window
        brand = Toplevel()
        #brand.title('What kind of car do you want to purchase?')#to be revised
        brand.geometry('400x250')
        
        price=brand1.get()
        band=StringVar()
        band.set(price)
        global type_car
        type_car=StringVar()
        
        subframe_brand = ttk.Frame(brand, padding="30 30 100 100")
        subframe_brand.grid(column=0, row=0, sticky=(N, W, E, S))
        subframe_brand.columnconfigure(0, weight=1)
        subframe_brand.rowconfigure(0, weight=1)
        ttk.Label(subframe_brand, textvariable=band).grid(column=1, row=2, sticky=(W, E)) 
        ttk.Label(subframe_brand, text="Your brand choice is:", font=('Arial', 14)).grid(column=1, row=1, sticky=W)
        ttk.Label(subframe_brand, text="\nYou can choose from the following models:", font=('Arial', 14)).grid(column=1, row=3, sticky=W)
         
        if selected_brand=="Aima electric scooters":
            play_bgm3()
            brand.title('What kind of Aima electric scooters do you want to purchase?')
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Aima Electric Motorcycle',text ='Aima Electric Motorcycle').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Aima Mini Plus',text ='Aima Mini Plus').grid(column=1, row=5, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Aima Maxspeed',text ='Aima Maxspeed').grid(column=1, row=6, sticky=W)      
        
        elif selected_brand=="BYD":    
            play_bgm2()
            brand.title('What kind of BYD do you want to purchase?')
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='BYD T3 Electric',text ='BYD T3 Electric').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='BYD Dolphin Electric',text ='BYD Dolphin Electric').grid(column=1, row=5, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='BYD Atto 3 Electric',text ='BYD Atto 3 Electric').grid(column=1, row=6, sticky=W)
        
        elif selected_brand=="Toyota":    
            play_bgm1()
            brand.title('What kind of Toyota do you want to purchase?')
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Toyota Camry Hybrid',text ='Toyota Camry Hybrid').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Toyota Land Cruiser Prado',text ='Toyota Land Cruiser Prado').grid(column=1, row=5, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Toyota Alphard',text ='Toyota Alphard').grid(column=1, row=6, sticky=W)
        
        elif selected_brand=="Mercedes-Benz":    
            play_bgm2()
            brand.title('What kind of Mercedes-Benz do you want to purchase?')
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Mercedes-Benz GLA-Class',text ='Mercedes-Benz GLA-Class').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Mercedes-Benz V-Class Diesel',text ='Mercedes-Benz V-Class Diesel').grid(column=1, row=5, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Mercedes-Benz G-Class Diesel',text ='Mercedes-Benz G-Class Diesel').grid(column=1, row=6, sticky=W)
        
        else:
            #band=="Rolls-Royce":    
            play_bgm5()
            brand.title('What kind of Rolls-Royce do you want to purchase?')
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Rolls-Royce Ghost Series II F1 Auto Edition',text ='Rolls-Royce Ghost Series II F1 Auto Edition').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Rolls-Royce Ghost F1 Auto Edition',text ='Rolls-Royce Ghost F1 Auto Edition').grid(column=1, row=5, sticky=W)
            ttk.Radiobutton(subframe_brand,variable = type_car,value ='Rolls-Royce Cullinan F1 Auto Cars Edition',text ='Rolls-Royce Cullinan F1 Auto Cars Edition').grid(column=1, row=6, sticky=W)


        # Check if any radio button is selected to trigger NEXT button and correspondingly the fourth window
        radio_button_selected = BooleanVar()
        radio_button_selected.set(False)

        def check_radio_selection():
            if type_car.get():
                radio_button_selected.set(True)
                next_button.config(state="active")
            else:
                radio_button_selected.set(False)
                next_button.config(state="disabled")

        type_car.trace_add("write", lambda name, index, mode: check_radio_selection())

        next_button = ttk.Button(subframe_brand, text='Next', command=color)
        next_button.grid(row=9, column=1, padx=1, pady=1)
        next_button.config(state="disabled")
             
        
        brand.mainloop()
    except ValueError:
        pass


def price_input(*args): # second part
    try: # avoid an error break the whole process
        top = Toplevel() # new window
        top.title('What is your target band?') # as the first part below
        top.geometry('400x250')
        feet=float(budget_amount) 
        
        price=DoubleVar()
        # price.set(value) # define a new variable equal to feet
        price.set(format(feet, ',.2f')) 
        global brand1 # gen global variable 
        brand1=StringVar()
        
        subframe = ttk.Frame(top, padding="30 30 100 100")
        subframe.grid(column=0, row=0, sticky=(N, W, E, S))
        subframe.columnconfigure(0, weight=1)
        subframe.rowconfigure(0, weight=1)
        # if value <>= 10000 and so on
        ttk.Label(subframe, textvariable=price).grid(column=1, row=2, sticky=(W, E))        
        ttk.Label(subframe, text="Your budget in SGD is:", font=('Arial', 14)).grid(column=1, row=1, sticky=W)
        ttk.Label(subframe, text="\nYou can choose from the following brands:", font=('Arial', 14)).grid(column=1, row=3, sticky=W)


        if feet<100000:
            ttk.Radiobutton(subframe,variable = brand1,value ='Aima electric scooters',text ='Aima electric scooters').grid(column=1, row=4, sticky=W) # below 10000
        elif feet<230000:
            ttk.Radiobutton(subframe,variable = brand1,value ='BYD',text ='BYD').grid(column=1, row=4, sticky=W)
        elif feet<440000:
            ttk.Radiobutton(subframe,variable = brand1,value ='BYD',text ='BYD').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe,variable = brand1,value ='Toyota',text ='Toyota').grid(column=1, row=5, sticky=W)     
        elif feet<2000000:
            ttk.Radiobutton(subframe,variable = brand1,value ='BYD',text ='BYD').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe,variable = brand1,value ='Toyota',text ='Toyota').grid(column=1, row=5, sticky=W) 
            ttk.Radiobutton(subframe,variable = brand1,value ='Mercedes-Benz',text ='Mercedes-Benz').grid(column=1, row=6, sticky=W)
        else:
            ttk.Radiobutton(subframe,variable = brand1,value ='BYD',text ='BYD').grid(column=1, row=4, sticky=W)
            ttk.Radiobutton(subframe,variable = brand1,value ='Toyota',text ='Toyota').grid(column=1, row=5, sticky=W)
            ttk.Radiobutton(subframe,variable = brand1,value ='Mercedes-Benz',text ='Mercedes-Benz').grid(column=1, row=6, sticky=W)
            ttk.Radiobutton(subframe,variable = brand1,value ='Rolls-Royce',text ='Rolls-Royce').grid(column=1, row=7, sticky=W)

        # Create a variable to keep track of whether a radio button is selected
        radio_button_selected = BooleanVar()
        radio_button_selected.set(False)

        # Define a function to enable/disable the "Next" button based on radio button selection
        def check_radio_selection():
            if brand1.get():
                radio_button_selected.set(True)
                next_button.config(state="active")
            else:
                radio_button_selected.set(False)
                next_button.config(state="disabled")

        # Bind the check_radio_selection function to the radio button variable
        brand1.trace_add("write", lambda name, index, mode: check_radio_selection())

        # Create the "Next" button with an initial state of "disabled"
        next_button = ttk.Button(subframe, text='Next', command=brand_choose)
        next_button.grid(row=9, column=1, padx=1, pady=1)
        next_button.config(state="disabled")


        if feet<=1000:
            delete_all_widgets(top)

            play_bgm4
            top.geometry('500x250')
            ttk.Label(subframe, textvariable=price).grid(column=1, row=2, sticky=(W, E))        
            ttk.Label(subframe, text="Your budget in SGD is:", font=('Arial', 14)).grid(column=1, row=1, sticky=W)
            ttk.Label(subframe, text="\nYou are currently in an insolvent state           ",font=('Arial', 14)).grid(column=1, row=3, sticky=W)
            ttk.Label(subframe, text="We suggest that you reconsider your budget before buying a car",font=('Arial', 14)).grid(column=1, row=4, sticky=W)
            def feetneg():
                stop_bgm()
                top.destroy()
                # First_Screen()
                play_bgm1()
            ttk.Button(subframe, text='Come back',command=feetneg).grid(row=9,column=1,padx=1,pady=1) # trigger the third window
        top.mainloop()
    except ValueError:
        pass

def delete_all_widgets(root):
    for widget in root.winfo_children():
        widget_name = widget.winfo_name()
        if widget_name.startswith("TButton") or widget_name.startswith("TEntry") or widget_name.startswith("TLabel"):
            widget.destroy()

def adjust_window_size(root, mainframe):
    try:
        root.update()  # 更新主窗口以确保小部件已布局
        width = root.winfo_width()
        height = root.winfo_height()
        font_size = 12  # 初始字体大小

        while width < 400 or height < 400:  # 设置窗口最小大小
            font_size -= 1
            style = ttk.Style()
            style.configure("TButton", font=("Arial", font_size))
            root.update()
            width = root.winfo_width()
            height = root.winfo_height()

        mainframe.update()
    except Exception as e:
        print(f"An error occurred: {e}")

def upload_image(price_var):
    try:
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])

        if file_path:
            # 获取用户输入的价格
            price = price_var.get()

            # 创建一个本地HTML文件，其中包含图像链接和价格
            html_content = f"<html><body><img src='file://{file_path}' alt='Uploaded Image' width='400'><br>Price: ${price}</body></html>"
            with open("image_viewer.html", "w") as html_file:
                html_file.write(html_content)

            # 打开默认浏览器以查看图像
            webbrowser.open("image_viewer.html")
    except Exception as e:
        print(f"An error occurred: {e}")

def First_Screen():
    pygame.mixer.init()
    play_bgm0()
    # Create the Homescreen window
    homescreen_window = Tk()
    homescreen_window.title("Automobile Advisor - Home")
    homescreen_window.geometry("450x150")  # Adjust the window size as needed

    # Customize fonts and styles
    style = ttk.Style()
    style1=ttk.Style()
    style1.configure('.',foreground='black',font=('Helvetica',14))
    style1.configure('1.TButton',background='blue',foreground='red',font=('黑体',12))
    style.configure('TLabel', font=('Arial', 14), foreground='black')
    style.configure('TButton', font=('Arial', 12))

    # Create a label for welcome message
    welcome_label = ttk.Label(homescreen_window, text="Welcome to Automobile Advisor!", style='TLabel')
    welcome_label.pack(pady=20)
    
    def start_button_clicked():
        homescreen_window.destroy()  # Hide the Homescreen window
        GUI_Budget()
        
    # Create a start buttont
    start_button = ttk.Button(homescreen_window, text="Begin Your Journey With Us!", command=start_button_clicked, style='TButton')
    start_button.pack(pady=20)

    homescreen_window.mainloop()



def GUI_Budget():
    stop_bgm()
    play_bgm1()
    # Define the credit retrieval function
    def credit_retrieval(missed_repayment):
        if missed_repayment in range(0, 2):
            loan_factor = 12
        elif missed_repayment in range(2, 4):
            loan_factor = 10
        elif missed_repayment in range(4, 6):
            loan_factor = 8
        else:
            loan_factor = 3
        return loan_factor

    # Define the budget generation function (unchanged)
    def budget_generation(salary, bonus, other_income, expenditure, commitment, saving, saving_utilization, missed_repayment):
        monthly_bonus = bonus / 12
        total_monthly_income = salary + monthly_bonus + other_income
        disposable_income = total_monthly_income - expenditure - commitment
        loan_factor = credit_retrieval(missed_repayment)
        loan_from_income = loan_factor * disposable_income
        budget_from_savings = saving_utilization / 100 * saving
        budget_amount = loan_from_income + budget_from_savings
        return round(budget_amount, 2)

    def calculate_budget():
        try:
            salary = float(salary_entry.get())
            bonus = float(bonus_entry.get())
            other_income = float(other_income_entry.get())
            expenditure = float(expenditure_entry.get())
            commitment = float(commitment_entry.get())
            saving = float(saving_entry.get())
            saving_utilization = float(saving_utilization_entry.get())
            missed_repayment = float(missed_repayment_entry.get())

            
            # If all conversions are successful, calculate the budget
            if any(value < 0 for value in [salary, bonus, other_income, expenditure, commitment, saving, saving_utilization, missed_repayment]):
                result_label.config(text="Input values cannot be negative.", foreground="red")
                continue_button.config(state=DISABLED)
            elif saving_utilization > 100:
                result_label.config(text="Your input for savings utilization cannot be greater than 100 for 100%.", foreground="red")
                continue_button.config(state=DISABLED)
            else:
                global month_net
                month_net=salary+bonus/12+other_income-expenditure-commitment
                global total_net
                total_net= saving-missed_repayment
                global budget_amount
                budget_amount = budget_generation(salary, bonus, other_income, expenditure, commitment, saving, saving_utilization, missed_repayment)
                result_label.config(text=f"Suggested budget amount: S${format(budget_amount, ',.2f')}", foreground="black")
                
                # Enable the "Continue" button since there are no input errors
                continue_button.config(state=NORMAL)
            
        # Handle the case where the user enters an invalid data type
        except ValueError:
            result_label.config(text="Please review your inputs, only numerical values are allowed.", foreground="red")

    # Create the main GUI window
    root = Tk()
    root.title("Car Purchase Budget Calculator")

    # Add an intro message
    intro_label = Label(root, text="Let's start by knowing your budget!", font=('Arial', 18))
    intro_label.grid(row=0, column=0, columnspan=2, padx=100, pady=20, sticky="w")
    
    # Create and grid labels and entry widgets
    Label(root, text="Monthly Salary (in SGD):").grid(row=2, column=0, sticky="w")
    salary_entry = Entry(root)
    salary_entry.grid(row=2, column=1)

    Label(root, text="Variable Bonus (Annual in SGD):").grid(row=4, column=0, sticky="w")
    bonus_entry = Entry(root)
    bonus_entry.grid(row=4, column=1)

    Label(root, text="Other Income (Total in SGD):").grid(row=6, column=0, sticky="w")
    other_income_entry = Entry(root)
    other_income_entry.grid(row=6, column=1)

    Label(root, text="Monthly Living Expenditure (in SGD):").grid(row=8, column=0, sticky="w")
    expenditure_entry = Entry(root)
    expenditure_entry.grid(row=8, column=1)

    Label(root, text="Monthly Financial Commitment (in SGD):").grid(row=10, column=0, sticky="w")
    commitment_entry = Entry(root)
    commitment_entry.grid(row=10, column=1)

    Label(root, text="Savings Balance (total in SGD):").grid(row=12, column=0, sticky="w")
    saving_entry = Entry(root)
    saving_entry.grid(row=12, column=1)

    Label(root, text="Savings Utilization (ex. '50' for 50%):").grid(row=14, column=0, sticky="w")
    saving_utilization_entry = Entry(root)
    saving_utilization_entry.grid(row=14, column=1)

    Label(root, text="Missed Repayments (Recent 12 Months):").grid(row=16, column=0, sticky="w")
    missed_repayment_entry = Entry(root)
    missed_repayment_entry.grid(row=16, column=1)

    # Create and grid a button to calculate the budget
    calculate_button = Button(root, text="Calculate Budget", command=calculate_budget)
    calculate_button.grid(row=18, columnspan=2)

    # Create a label to display the result
    result_label = Label(root, text="", pady=10)
    result_label.grid(row=20, columnspan=2)
        
    # Create a "Continue" button initially disabled until user correctly calculates budget
    def p_i():
        # root.destroy()
        price_input()
    continue_button = Button(root, text="Continue to Select Your Car",command= p_i, state=DISABLED)
    continue_button.grid(row=22, columnspan=2)
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":

    First_Screen()
    


