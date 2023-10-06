import tkinter as tk
from tkinter import filedialog
import pyautogui
from PIL import Image, ImageTk, ImageDraw
import time
from pynput import mouse



def main():

    #Window and Frame Initialization***********************************************************
    window_width=800
    window_height=700
    #Main window and frames
    root = tk.Tk()
    root.title("PR3 Image Drawer")
    root.resizable(False,False)
    default_color = root.cget("bg")
    root.geometry( "800x800" )
    topleft_Frame = tk.Frame(master=root, width=400, height=800)
    topright_Frame = tk.Frame(master=root, width=400, height=800,borderwidth=20, bg = "black")
    image_widget_frame = tk.Frame(master=topleft_Frame)
    image_frame = tk.Frame(master=image_widget_frame,width=200,height=200,bg="black", relief=tk.RIDGE, borderwidth=20)
    zoomed_display_frame = tk.Frame(master=topright_Frame,width=400,height=400,bg="grey")
    pixels_mapped = {}


    #Tkinter Vars************************************************* Referenced during execution

    #Positions
    cb_position_x_var=tk.StringVar()
    cb_position_y_var=tk.StringVar()
    hexCodeBox_position_x_var = tk.StringVar()
    hexCodeBox_position_y_var = tk.StringVar()
    startingPixel_position_x_var = tk.StringVar()
    startingPixel_position_y_var = tk.StringVar()
    alphaBox_position_x_var = tk.StringVar()
    alphaBox_position_y_var = tk.StringVar()
    alphaValue_position_x_var = tk.StringVar()
    alphaValue_position_y_var = tk.StringVar()

    #flags
    found_pix_coord = tk.StringVar()
    found_pix_coord.set("n")
    use_alpha = tk.IntVar()
    cbCoordSet = tk.IntVar()
    cbCoordSet.set(0)
    hexCoordSet = tk.IntVar()
    hexCoordSet.set(0)
    tlCoordSet = tk.IntVar()
    tlCoordSet.set(0)
    abCoordSet = tk.IntVar()
    abCoordSet.set(0)
    avCoordSet = tk.IntVar()
    avCoordSet.set(0)
    imgPrepSet = tk.IntVar()
    imgPrepSet.set(0)

    drawingPaused = tk.IntVar()
    drawingPaused.set(0)

    #delays
    boxToValDelay = tk.StringVar()
    boxToValDelay.set(0)
    valToPasteDelay = tk.StringVar()
    valToPasteDelay.set(0)
    pasteToExitDelay = tk.StringVar()
    pasteToExitDelay.set(0)
    exitToDrawDelay = tk.StringVar()
    exitToDrawDelay.set(.25)
    drawToDrawDelay = tk.StringVar()
    drawToDrawDelay.set(0)
    drawToBoxDelay = tk.StringVar()
    drawToBoxDelay.set(0)

    #img url
    img_url = tk.StringVar()

    #options
    tool_options = [
        'Block',
        'Stamp'
    ]
    tool_option = tk.StringVar()
    tool_option.set('Block')


    def update_image_frame(option):
        if option== 'Block':
            imglab.configure(text="No Valid 40x40 Selection", image='')
        if option == 'Stamp':
            imglab.configure(text="Max Dimensions 256x256\nNo Valid Selection", image='')
        prepareBut.configure(state=tk.DISABLED, text="Prepare Image", background=default_color)
        pixels_mapped.clear()
        imgPrepSet.set(0)
        dimLab.configure(text = "Dimensions: ~")

    def get_hex_coords():
        def on_click(x, y, button, pressed):
            if pressed and button == button.left:
                hexCodeBox_position_x_var.set(x)
                hexCodeBox_position_y_var.set(y)
                hexLabel.config(text="("+str(x)+","+str(y)+")")
                hexButton.configure(relief="raised", background=default_color)
                listener.stop()
                hexCoordSet.set(1)
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        hexButton.configure(relief="sunken", background="white")
    

    def get_colorbox_coords():
        def on_click(x, y, button, pressed):
            if pressed and button == button.left:
                cb_position_x_var.set(x)
                cb_position_y_var.set(y)
                cbLabel.config(text="("+str(x)+","+str(y)+")")
                cbButton.configure(relief="raised", background=default_color)
                listener.stop()
                cbCoordSet.set(1)
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        cbButton.configure(relief="sunken", background="white")

    def get_alphabox_coords():
        def on_click(x, y, button, pressed):
            if pressed and button == button.left:
                alphaBox_position_x_var.set(x)
                alphaBox_position_y_var.set(y)
                alphaBoxLabel.config(text="("+str(x)+","+str(y)+")")
                alphaBoxBut.configure(relief="raised", background=default_color)
                listener.stop()
                abCoordSet.set(1)
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        alphaBoxBut.configure(relief="sunken", background="white")

    def get_alphaval_coords():
        def on_click(x, y, button, pressed):
            if pressed and button == button.left:
                alphaValue_position_x_var.set(x)
                alphaValue_position_y_var.set(x)
                alphaValLabel.config(text="("+str(x)+","+str(y)+")")
                alphaValBut.configure(relief="raised", background=default_color)
                listener.stop()
                avCoordSet.set(1)
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        alphaValBut.configure(relief="sunken", background="white")

    def select_image_file():
        global display
        filename = filedialog.askopenfilename(title="Select a PNG file", filetypes=[("PNG files", "*.png")],)
        img_url.set(filename)
        display = Image.open(img_url.get())
        color_mode = display.mode
        width = display.width
        height = display.height
        if tool_option.get()=='Block':
            if width == 40 and height == 40:
                display = display.resize((160,160), Image.NEAREST)
                display = ImageTk.PhotoImage(display)            
                #enable the prepare button, which creates a dictionary of all color codes and pixels
                prepareBut.configure(state=tk.ACTIVE)

                #enable alpha checkbox if img contains alpha channel
                if color_mode == "RGBA":
                    #use_alpha.set(1)
                    #alpha_checkbox.configure(state=tk.ACTIVE)
                    #alphaBoxBut.configure(state=tk.ACTIVE)
                    #alphaValBut.configure(state=tk.ACTIVE)
                    pass

                imglab.configure(image=display, borderwidth=0, highlightthickness=0, width= 160, height = 160)
                dimLab.config(text="Dimensions: (" + str(width) + "x" + str(height) + ")")
                if not(imglab.winfo_ismapped()):
                    imglab.pack()
            else:
                imglab.configure(text="Invalid Image")

        if tool_option.get() == 'Stamp':
            if width <= 256 and height <= 256:
                display = display.resize((160,160), Image.NEAREST)
                display = ImageTk.PhotoImage(display)            
                #enable the prepare button, which creates a dictionary of all color codes and pixels
                prepareBut.configure(state=tk.ACTIVE)

                #enable alpha checkbox if img contains alpha channel
                if color_mode == "RGBA":
                    #use_alpha.set(1)
                    #alpha_checkbox.configure(state=tk.ACTIVE)
                    #alphaBoxBut.configure(state=tk.ACTIVE)
                    #alphaValBut.configure(state=tk.ACTIVE)
                    pass

                imglab.configure(image=display, borderwidth=0, highlightthickness=0, width= 160, height = 160)
                dimLab.config(text="Dimensions: (" + str(width) + "x" + str(height) + ")")
                if not(imglab.winfo_ismapped()):
                    imglab.pack()
            else:
                imglab.configure(text="Invalid Image")

    def start_zoom_operation():
        def on_click(x, y, button, pressed):
            if pressed and button == button.left:
                startingPixel_position_x_var.set(x)
                startingPixel_position_y_var.set(y)
                canvasTLLabel.config(text="("+str(x)+","+str(y)+")")
                canvasTLBut.configure(relief="raised", background=default_color)
                found_pix_coord.set("y")
                tlCoordSet.set(1)
                listener.stop()                

        def zoom_operation():
            x, y = pyautogui.position()
            
            
            global zoom_img
            x, y = pyautogui.position()
            screenshot = pyautogui.screenshot(region=(x-4,y-4,9,9))
            screenshot = screenshot.resize((396, 396), Image.NEAREST)
            box = ImageDraw.Draw(screenshot)
            box.rectangle([176,176, 220,220], outline="red", width=2)
            zoom_img = ImageTk.PhotoImage(screenshot)
            zoomedInRegionLabel.configure(image=zoom_img)

            #loop unless loc found
            if found_pix_coord.get()=="y":
                found_pix_coord.set("n")
                return
            
            root.after(100, zoom_operation)

        listener = mouse.Listener(on_click=on_click)
        listener.start()
        canvasTLBut.configure(relief="sunken", background="white")
        zoom_operation()

    
    def prepareImage():
        img = Image.open(img_url.get())
        pixels = img.load()
        width, height = img.size
        print(img.mode)

        count_check = 0
        if(img.mode=="RGBA"):
            for x in range(width):
                for y in range(height):
                    count_check+=1
                    pixel = pixels[x, y]
                    hex_color = "#{:02x}{:02x}{:02x}".format(pixel[0], pixel[1], pixel[2])

                    if hex_color not in pixels_mapped:
                        pixels_mapped[hex_color] = []

                    pixels_mapped[hex_color].append((x, y, pixel[3]))
        else:

            for x in range(width):
                for y in range(height):
                    pixel = pixels[x, y]
                    hex_color = "#{:02x}{:02x}{:02x}".format(pixel[0], pixel[1], pixel[2])

                    if hex_color not in pixels_mapped:
                        pixels_mapped[hex_color] = []

                    pixels_mapped[hex_color].append((x, y))

        prepareBut.configure(text="Finished Prep!", state=tk.DISABLED, background="#cccc66")
        imgPrepSet.set(1)
        print(count_check)
        second_check = 0
        for p, coord in pixels_mapped.items():
            for c in coord:
                second_check+=1
        print(second_check)
                
        #print(len(pixels_mapped))

    def on_use_alpha_clicked():
        if use_alpha.get():
            alphaBoxBut.configure(state=tk.ACTIVE)
            alphaValBut.configure(state=tk.ACTIVE)
        else:
            alphaBoxBut.configure(state=tk.DISABLED)
            alphaValBut.configure(state=tk.DISABLED)

    def startDrawingCommand():
        cont = False
        if use_alpha.get():
            if cbCoordSet.get() and hexCoordSet.get() and tlCoordSet.get() and imgPrepSet.get() and abCoordSet.get() and avCoordSet.get():
                startDrawingInfo.configure(text="Started with alpha!")
                cont = True
            else:
                startDrawingInfo.configure(text="Missing Something!")
        else:
            if cbCoordSet.get() and hexCoordSet.get() and tlCoordSet.get() and imgPrepSet.get():
                startDrawingInfo.configure(text="Started without alpha!")
                cont = True
            else:
                startDrawingInfo.configure(text="Missing Something!")
        if cont:
            cbx = int(cb_position_x_var.get())
            cby = int(cb_position_y_var.get())
            hvx = int(hexCodeBox_position_x_var.get())
            hvy = int(hexCodeBox_position_y_var.get())
            tlx = int(startingPixel_position_x_var.get())
            tly = int(startingPixel_position_y_var.get())
            bTVDelay = float(boxToValDelay.get())
            vtPDelay = float(valToPasteDelay.get())
            ptEDelay = float(pasteToExitDelay.get())
            etDDelay = float(exitToDrawDelay.get())
            dtDdelay = float(drawToDrawDelay.get())
            dtbDelay = float(drawToBoxDelay.get())
            first_one = True
            for hexColor, coords in pixels_mapped.items():
                first_one = True
                pyautogui.click(cbx,cby)
                time.sleep(bTVDelay)
                pyautogui.click(hvx,hvy)
                time.sleep(vtPDelay)
                pyautogui.hotkey('ctrl','a')
                pyautogui.write(hexColor)
                time.sleep(ptEDelay)
                pyautogui.press('tab')
                time.sleep(ptEDelay)
                pyautogui.press('tab')
                time.sleep(ptEDelay)
                pyautogui.press('enter')
                time.sleep(etDDelay)
                for coord in coords:
                    while(drawingPaused.get()):
                        time.sleep(1)
                    if first_one:
                        pyautogui.click(tlx+int(coord[0]),tly+int(coord[1]))
                        first_one = False
                    pyautogui.click(tlx+int(coord[0]),tly+int(coord[1]))
                    time.sleep(dtDdelay)
                time.sleep(dtbDelay)
            
            startDrawingInfo.configure(text="Finished!")
                    
                    
                    

    #Frame configuration from top left to bottom right

    #topleft
    #RadioButton image size
    drawTypeRadio = tk.OptionMenu(image_widget_frame, tool_option, *tool_options, command=update_image_frame)
    drawTypeRadio.pack(pady=5)

    #search for image button
    imglab = tk.Label(image_frame, text= "No Valid 40x40 Selection", width= 160, height = 160)
    imglab.pack()
    button = tk.Button(image_widget_frame , text = "Select Image (png's only)" , command = lambda: select_image_file())
    image_frame.pack( anchor="n")
    image_frame.pack_propagate(0)
    button.pack( anchor="n")

    #dimensions label
    dimLab = tk.Label(image_widget_frame, text = "Dimensions: ~")
    dimLab.pack()
    #Prepare button
    prepareBut = tk.Button(image_widget_frame, text="Prepare Image", command=prepareImage)
    prepareBut.pack(pady=20)
    prepareBut.configure(state=tk.DISABLED)
    image_widget_frame.pack(pady=25)
  

    
    # Button to set Colorbox coords
    colorBox_frame = tk.Frame(master=topleft_Frame)
    cbButton = tk.Button(colorBox_frame , text = "Set Colorbox Coordinate" , command = get_colorbox_coords)
    cbButton.pack(side=tk.LEFT)
    cbLabel = tk.Label(colorBox_frame, text = "N/A")
    cbLabel.pack(side=tk.LEFT)
    colorBox_frame.pack(pady=10, anchor="w",padx=20)

    # Button to set hexcode coords
    hexButton_frame = tk.Frame(master=topleft_Frame)
    hexButton = tk.Button(hexButton_frame , text = "Set HexCode Coordinate" , command = get_hex_coords)
    hexButton.pack(side=tk.LEFT)
    hexLabel = tk.Label(hexButton_frame, text = "N/A")
    hexLabel.pack(side=tk.LEFT)
    hexButton_frame.pack(pady=10, anchor="w",padx=20)

    # Button to start zoom and topleft pixel selection process.
    canvasTL_frame = tk.Frame(master=topleft_Frame)
    canvasTLBut = tk.Button(canvasTL_frame , text = "Set topleft-most pixel" , command = start_zoom_operation)
    canvasTLBut.pack(side=tk.LEFT)
    canvasTLLabel = tk.Label(canvasTL_frame, text = "N/A")
    canvasTLLabel.pack(side=tk.LEFT)
    canvasTL_frame.pack(pady=10, anchor="w",padx=20)

    #checkbox to determine if you want opacity, if given the option
    alpha_checkbox = tk.Checkbutton(topleft_Frame, text="Use Alpha?", variable=use_alpha, command= on_use_alpha_clicked)
    alpha_checkbox.pack()
    alpha_checkbox.configure(state=tk.DISABLED)
    #alpha coordbuttons
    alpha_frame = tk.Frame(master=topleft_Frame)    
    alphaBoxBut = tk.Button(alpha_frame , text = "Set AlphaBox Coord" , command = get_alphabox_coords)
    alphaBoxBut.pack(side=tk.LEFT)
    alphaBoxBut.configure(state=tk.DISABLED)
    alphaBoxLabel = tk.Label(alpha_frame, text = "N/A")
    alphaBoxLabel.pack(side=tk.LEFT)
    alphaValBut = tk.Button(alpha_frame , text = "Set AlphaVal Coord" , command = get_alphaval_coords)
    alphaValBut.pack(side=tk.LEFT)
    alphaValBut.configure(state=tk.DISABLED)
    alphaValLabel = tk.Label(alpha_frame, text = "N/A")
    alphaValLabel.pack(side=tk.LEFT)
    alpha_frame.pack(anchor="w",padx=20)


    #entrys to input delays.
    #Main window that holds the 3 sub windows
    mainDelayFrame=tk.Frame(master=topleft_Frame)

    #sub window 1
    delayFrameS1 = tk.Frame(master=mainDelayFrame)

    #sub1 left (draw to box)
    delayFrameS1Left = tk.Frame(master=delayFrameS1)
    drawToBoxDelayLabel = tk.Label(master=delayFrameS1Left,text="Draw to Box Delay")
    drawToBoxDelayEntry = tk.Entry(master=delayFrameS1Left,textvariable=drawToBoxDelay,width=5)
    drawToBoxDelayLabel.pack(side=tk.LEFT)
    drawToBoxDelayEntry.pack(side=tk.LEFT)

    #sub1 right (draw to draw)
    delayFrameS1Right = tk.Frame(master=delayFrameS1)
    drawToDrawDelayLabel = tk.Label(master=delayFrameS1Right,text="Draw to Draw Delay")
    drawToDrawDelayEntry = tk.Entry(master=delayFrameS1Right,textvariable=drawToDrawDelay,width=5)
    drawToDrawDelayLabel.pack(side=tk.LEFT)
    drawToDrawDelayEntry.pack(side=tk.LEFT)

    #packing sub1
    delayFrameS1Left.pack(side=tk.LEFT, padx=20)
    delayFrameS1Right.pack(side=tk.LEFT)
    delayFrameS1.pack()

    #sub window 2
    delayFrameS2 = tk.Frame(master=mainDelayFrame)

    #sub2 left (box to val)
    delayFrameS2Left = tk.Frame(master=delayFrameS2)
    boxToValDelayLabel = tk.Label(master=delayFrameS2Left,text="Box to Val Delay")
    boxToValDelayEntry = tk.Entry(master=delayFrameS2Left,textvariable=boxToValDelay,width=5)
    boxToValDelayLabel.pack(side=tk.LEFT)
    boxToValDelayEntry.pack(side=tk.LEFT)

    #sub2 right
    delayFrameS2Right = tk.Frame(master=delayFrameS2)
    valToPasteDelayLabel = tk.Label(master=delayFrameS2Right,text="Val to Paste Delay")
    valToPasteDelayEntry = tk.Entry(master=delayFrameS2Right,textvariable=valToPasteDelay,width=5)
    valToPasteDelayLabel.pack(side=tk.LEFT)
    valToPasteDelayEntry.pack(side=tk.LEFT)

    #packing sub2
    delayFrameS2Left.pack(side=tk.LEFT, padx=20)
    delayFrameS2Right.pack(side=tk.LEFT)
    delayFrameS2.pack(pady=5)

    #sub window 3
    delayFrameS3 = tk.Frame(master=mainDelayFrame)

    #sub3 left (box to val)
    delayFrameS3Left = tk.Frame(master=delayFrameS3)
    pasteToExitDelayLabel = tk.Label(master=delayFrameS3Left,text="Paste To Exit Delay")
    pasteToExitDelayEntry = tk.Entry(master=delayFrameS3Left,textvariable=pasteToExitDelay,width=5)
    pasteToExitDelayLabel.pack(side=tk.LEFT)
    pasteToExitDelayEntry.pack(side=tk.LEFT)

    #sub3 right
    delayFrameS3Right = tk.Frame(master=delayFrameS3)
    exitToDrawDelayLabel = tk.Label(master=delayFrameS3Right,text="Exit to Draw Delay")
    exitToDrawDelayEntry = tk.Entry(master=delayFrameS3Right,textvariable=exitToDrawDelay,width=5)
    exitToDrawDelayLabel.pack(side=tk.LEFT)
    exitToDrawDelayEntry.pack(side=tk.LEFT)

    #packing sub3
    delayFrameS3Left.pack(side=tk.LEFT, padx=20)
    delayFrameS3Right.pack(side=tk.LEFT)
    delayFrameS3.pack()

    mainDelayFrame.pack(anchor="w",pady=50)


    

    #Region to display cursors location zoomed in
    zoomedInRegionLabel = tk.Label(zoomed_display_frame)
    zoomedInRegionLabel.pack()
    zoomed_display_frame.pack()
    zoomed_display_frame.pack_propagate(0)

    #Start Drawing Button
    startDrawingButton = tk.Button(master=topright_Frame, text="START!", command=startDrawingCommand, width=30, height = 5, background="green")
    startDrawingButton.pack(pady=40)

    startDrawingInfo = tk.Label(master=topright_Frame, text="~~~~~~~~~~~~", fg = "white", background="black")
    startDrawingInfo.pack()

    #label.pack()
    topleft_Frame.pack(side=tk.LEFT)
    topleft_Frame.pack_propagate(0)
    topright_Frame.pack()
    topright_Frame.pack_propagate(0)
    root.mainloop()

    
    

if __name__ == "__main__":
    main()