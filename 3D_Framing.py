"""
 Simulation of a rotating 3D Wire Frame
 Developed by Derek Sawle
"""

import sys, math, pygame, random, os, time, numpy
# import pyautogui
from operator import itemgetter
import tkinter as tk
from tkinter import Menu
# import pynput (???? module installed, but not recognised!!)

# Construct Main window

window = tk.Tk() # create a Tk root window

w = 1920 # width for the Tk root
h = 0 # height for the Tk root

# get screen width and height
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = -10
y = 0

# set the dimensions of the screen 
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

# DISPLAYSURF = pygame.display.set_mode((1920, 568-30),)

window.title("FrameStudio (LITE)")

# Display Menu

menu = Menu(window)

new_item = Menu(menu)
new_item.add_command(label='New Model Ctrl+N')
new_item.add_command(label='Open Model Ctrl+O')
new_item.add_command(label='Open Examples')
new_item.add_command(label='Recent Models ')
new_item.add_command(label='Save Ctrl+S')
new_item.add_command(label='Save As Ctrl+Shift+S')
new_item.add_command(label='Save Copy As Alt+Shift+S')
new_item.add_command(label='Print Window Ctrl+P')
new_item.add_command(label='Export Crtl+E')
new_item.add_command(label='Close Alt+F4')
new_item.add_command(label='Exit Ctrl+Q)')
menu.add_cascade(label='File', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Box Template')
new_item.add_command(label='Pyramid Template')
new_item.add_command(label='Duo Pitch Template')
new_item.add_command(label='Dome')
menu.add_cascade(label='Modeler', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Select Nodes')
new_item.add_command(label='Select Members')
new_item.add_command(label='Members Properties')
new_item.add_command(label='Delete Selected Del')
menu.add_cascade(label='Edit', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Joint Loads')
new_item.add_command(label='Member Loads')
new_item.add_command(label='Load Combinations')
new_item.add_command(label='Applied Displacements')
new_item.add_command(label='Dynamic Response')
menu.add_cascade(label='Loads', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Static')
new_item.add_command(label='P-Delta')
new_item.add_command(label='Non-Linear')
new_item.add_command(label='Dynamic Response')
menu.add_cascade(label='Analysis', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Show')
new_item.add_command(label='Print Results')

menu.add_cascade(label='Output', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Show')
new_item.add_command(label='Print Results')

menu.add_cascade(label='Preferences', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Show')
new_item.add_command(label='Print Results')

menu.add_cascade(label='Settings', menu=new_item)

new_item = Menu(menu)
new_item.add_command(label='Tutorial')

menu.add_cascade(label='Help', menu=new_item)

window.config(menu=menu)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRACE_1 = (55, 55, 55)
TRACE_2 = (60, 60, 160)
GREY_1 = (150,150,150)
CROSS_HR_COL = (200,200,200)

# define window environment parameters
SCRN_ASP_RATIO = 1.7777
SCRN_WDTH = 1540
SCRN_HGT = int(SCRN_WDTH/1.7777)
BACKGRD = GREY_1
ORIGIN_X = int(SCRN_WDTH/2)
ORIGIN_Y = int(SCRN_HGT/2)

# Define Font
font_name = pygame.font.match_font('arial') # finds font closest to arial
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# define plot paraameters
FPS = 60
Pxl_Amt = 5 # Tranlational separation rate f object from Origin
Zoom_Rate = 1.03; Max_Zoom = 30; Min_Zoom = 0.2
Jnt_Siz = int(6)
CURSOR_RECT = int(11)
CURSOR_X = 0
CURSOR_Y = 0

# First-see window settings
ANG_X = 27 # Elipse Plot Orientation in degrees
ANG_Y = 330 # Nodal Plot Orientation in degrees
Zoom_Fact = 1; 

# Model Geometric Data - 
# Nodes
Input_Data = [1,-150,100,100,
            2,100,100,100,
            3,100,100,-100,
            4,-150,100,-100,
            5,-150,-100,100,
            6,100,-100,100,
            7,100,-100,-100,
            8,-150,-100,-100,
            9,-150,150,0,
            10,100,150,0,
            11,-100,150,0,
            12,-100,100,100,
            13,-150,175,0,
            14,-100,175,0,
            15,-150,175,100,
            16,-100,175,100]

# Lines (LinRef, FromPt, ToPt)
Lines=[1,1,2,
       2,10,3,
       3,3,4,
       4,9,1,
       5,5,6,
       6,6,7,
       7,7,8,
       8,8,5,
       9,1,5,
       10,2,6,
       11,3,7,
       12,4,8,
       13,10,2,
       14,4,9,
       15,9,11,
       16,11,10,
       17,11,12,
       18,13,14,
       19,14,16,
       20,16,15,
       21,15,13,
       22,12,16,
       23,1,15,
       24,9,13,
       25,11,14]

NODAL_SCRN_CORDS = []
Node_Qty=Input_Data[-4]
Line_Qty=Lines[-3]

# Initiate 
pygame.init()

# Set Display Parameters
SCRN_POS_X = 0
SCRN_POS_Y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCRN_POS_X,SCRN_POS_Y)
screen = pygame.display.set_mode((SCRN_WDTH,SCRN_HGT))
pygame.display.set_caption("FrameStudio - (LITE)")

# System Parameters
clock = pygame.time.Clock()


# Convert Node Input Data to Node Screen Data

Nodes = []

for i in range(Node_Qty):
    JT = (Input_Data[i*4+0])
    X = (Input_Data[i*4+1])
    Z = (Input_Data[i*4+2])
    Y = (Input_Data[i*4+3])
    
    if X == 0 and Y == 0: ANG = 0
    if X <= 0 and Y >= 0: ANG = math.degrees(math.atan(Y/-X))
    if X >= 0 and Y >= 0: ANG = 180 - math.degrees(math.atan(Y/X))
    if X >= 0 and Y <= 0: ANG = 180 + math.degrees(math.atan(-Y/X))
    if X <= 0 and Y <= 0: ANG = 360 - math.degrees(math.atan(-Y/-X))

    Nodes.append(JT)
    Nodes.append(X)
    Nodes.append(Z)
    Nodes.append(ANG)

""" Main Loop """

running = True
while running:
    clock.tick(FPS)
    screen.fill(BACKGRD)
    NODAL_SCRN_CORDS =[]
    
    # Check for pressed keys:
    keystate = pygame.key.get_pressed()

##    if keystate[pygame.K_F3]:
##        # DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
##        DISPLAYSURF = pygame.display.set_mode((1540, 968-30),) # Pygame only seems to support 1540 x 968
##
##    if keystate[pygame.K_F4]:
##        DISPLAYSURF = pygame.display.set_mode((SCRN_WDTH,SCRN_HGT),0,0)
    
    if keystate[pygame.K_F12]: # Exit Program
        DISPLAYSURF = pygame.display.set_mode((480,320))                                     
        print ('Routine Exited on Command!')
        running = False

    # Rotate about Y axis
    if keystate[pygame.K_LEFT]: ANG_Y-=2
    if ANG_Y<1:ANG_Y=359
    if keystate[pygame.K_RIGHT]: ANG_Y+=2
    if ANG_Y>359:ANG_Y=1    
    # Rotate about X axis
    if keystate[pygame.K_DOWN]: ANG_X-=1.5
    if ANG_X<1:ANG_X=0
    if keystate[pygame.K_UP]: ANG_X+=1.5
    if ANG_X>90:ANG_X=90
    # Apply Zoom
    if keystate[pygame.K_d]: Zoom_Fact = Zoom_Fact * Zoom_Rate
    if Zoom_Fact>Max_Zoom:Zoom_Fact=Max_Zoom
    if keystate[pygame.K_a]: Zoom_Fact = Zoom_Fact/Zoom_Rate
    if Zoom_Fact<Min_Zoom:Zoom_Fact=Min_Zoom
    # Translate Object and Origin
    if keystate[pygame.K_i]: ORIGIN_Y-=5
    if keystate[pygame.K_j]: ORIGIN_X-=5
    if keystate[pygame.K_l]: ORIGIN_X+=5
    if keystate[pygame.K_m]: ORIGIN_Y+=5
    # Recall Main Menu Bar
    if keystate[pygame.K_TAB]:
        pass
    
    
     # Translate Object relative to Origin
##    if keystate[pygame.K_F1]:
##        for i in range(Node_Qty):
##            Nodes [4*i+1]=Nodes [4*i+1] - Pxl_Amt    
##    if keystate[pygame.K_F2]:
##        for i in range(Node_Qty):
##            Nodes [4*i+1]=Nodes [4*i+1] + Pxl_Amt
  
        
    # if keystate[pygame.K_F3]: 
    
            
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
            
    draw_text(screen, "X-Cursor = "+str(round(CURSOR_X,1)), 14, 80, 710)
    draw_text(screen, "Y-Cursor = "+str(round(CURSOR_Y,1)), 14, 80, 725)
    draw_text(screen, "X-Axis Rotation = "+str(round(ANG_Y,1)), 14, 80, 740)
    draw_text(screen, "Y-Axis Rotation = "+str(round(ANG_X,1)), 14, 80, 755)
    draw_text(screen, "Zoom Factor = "+str(round(Zoom_Fact,2)), 14, 80, 770)
    draw_text(screen, "Origin X = "+str(round(ORIGIN_X,0)), 14, 80, 785)
    draw_text(screen, "Origin Y = "+str(round(ORIGIN_Y,)), 14, 80, 800)

    # --------- Map Nodes ----------#

    for i in range (Node_Qty):

        # Read in Data
        Node = Nodes[i*4:i*4+4]
        Node_Num = Node[0]
        X_CORD = Node[1]
        Z_CORD = Node[2]
        NODE_ANG = Node[3]
        
        # Calulate Node/Eliptical math
        X_CORD = X_CORD/(math.cos(math.radians(NODE_ANG))) # Calulates 2D X from 3D
        Elip_Wid = abs(2*X_CORD)
    
        # Elipse Math (For each node)
        Elip_Hyt = (math.cos(math.radians(90-ANG_X)))*Elip_Wid
        x1 = int(-Elip_Wid/2) # left most point of elipse
        x2 = int(Elip_Wid/2) # right most point of elipse
        a = Elip_Wid/2
        b = Elip_Hyt/2

        # Caluclate Position of Node on Screen relative to Angle             
        x = (math.cos(math.radians(ANG_Y+NODE_ANG)))*a
        SIGN_Y =  numpy.sign(math.sin(math.radians(ANG_Y+NODE_ANG)))
        # check SQRT isnt a finite negative number
        Check_Num = (b**2)-(((b**2)*(x**2))/(a**2))
        if Check_Num < 0.1 and Check_Num > -0.1: Check_Num = 0
        
        y = SIGN_Y*math.sqrt(Check_Num)
        z = math.sin(math.radians(90-ANG_X))*Z_CORD

        # Apply Zoom Factor
        x = x *Zoom_Fact
        y = y *Zoom_Fact
        z = z *Zoom_Fact
        
        # Set Eleptical Path of Node on Screen
        Wide = int(Zoom_Fact*Elip_Wid)
        High = int(Zoom_Fact*Elip_Hyt)
        At_X = int(ORIGIN_X - Wide/2)
        At_Y = int(ORIGIN_Y - (High/2) - z)
        if High < 2: High = 2 #check ellipse height doesnt fall below 2 causing error

        # Screen Coordinates for Nodes -
        SCRN_X = int(ORIGIN_X-x)
        SCRN_Y = int(ORIGIN_Y-y-z)

        # Record Screen Map for drawing lines between nodes (node num. x y)
        NODAL_SCRN_CORDS.append(i)
        NODAL_SCRN_CORDS.append(SCRN_X)
        NODAL_SCRN_CORDS.append(SCRN_Y)

        # Label Nodes
        draw_text(screen, str(Node_Num), 12, SCRN_X+6, SCRN_Y+6)

        # Show Node on Screen
        pygame.draw.rect(screen, GREEN, (int(ORIGIN_X-x-(6/2)), int(ORIGIN_Y-y-(6/2)-z),6,6),1)

    # Draw Lines
    for j in range (Line_Qty):
        Joint_1 = Lines[j*3+1]
        Joint_2 = Lines[j*3+2]
        From_X = NODAL_SCRN_CORDS[(Joint_1-1)*3+1]
        From_Y = NODAL_SCRN_CORDS[(Joint_1-1)*3+2]
        To_X = NODAL_SCRN_CORDS[(Joint_2-1)*3+1]
        To_Y = NODAL_SCRN_CORDS[(Joint_2-1)*3+2]
        pygame.draw.line(screen, YELLOW, (From_X, From_Y),(To_X, To_Y), 1)

    # Show point of origin on screen
    pygame.draw.rect(screen, YELLOW, (ORIGIN_X, ORIGIN_Y,1,1),1)

    # Show XY-Scale line
    Line300=150*Zoom_Fact
    pygame.draw.line(screen, TRACE_1,(int(ORIGIN_X),int(ORIGIN_Y)),((int(ORIGIN_X+Line300)),(int(ORIGIN_Y))),1)
    pygame.draw.line(screen, TRACE_1,(int(ORIGIN_X-Line300),int(ORIGIN_Y)),((int(ORIGIN_X)),(int(ORIGIN_Y))),1)
    pygame.draw.line(screen, TRACE_1,(int(ORIGIN_X),int(ORIGIN_Y+Line300)),((int(ORIGIN_X)),(int(ORIGIN_Y-Line300))),1)
    pygame.draw.line(screen, TRACE_1,(int(ORIGIN_X-Line300),int(ORIGIN_Y)),((int(ORIGIN_X)),(int(ORIGIN_Y))),1)

    Line200=100*Zoom_Fact
    pygame.draw.line(screen, TRACE_2,(int(ORIGIN_X),int(ORIGIN_Y)),((int(ORIGIN_X+Line200)),(int(ORIGIN_Y))),1)
    pygame.draw.line(screen, TRACE_2,(int(ORIGIN_X-Line200),int(ORIGIN_Y)),((int(ORIGIN_X)),(int(ORIGIN_Y))),1)
    pygame.draw.line(screen, TRACE_2,(int(ORIGIN_X),int(ORIGIN_Y+Line200)),((int(ORIGIN_X)),(int(ORIGIN_Y-Line200))),1)
    pygame.draw.line(screen, TRACE_2,(int(ORIGIN_X-Line200),int(ORIGIN_Y)),((int(ORIGIN_X)),(int(ORIGIN_Y))),1)

    # GUI - Display Cursor Cross Hairs 
    CURSOR_X, CURSOR_Y = pygame.mouse.get_pos()
    CURSOR_X = int(CURSOR_X)
    CURSOR_Y = int(CURSOR_Y)
    pygame.draw.line(screen,CROSS_HR_COL,(CURSOR_X-SCRN_WDTH,CURSOR_Y),(CURSOR_X+SCRN_WDTH,CURSOR_Y),1)
    pygame.draw.line(screen,CROSS_HR_COL,(CURSOR_X,CURSOR_Y-SCRN_HGT),(CURSOR_X,CURSOR_Y+SCRN_HGT),1)
    pygame.draw.rect(screen, CROSS_HR_COL, (CURSOR_X-int(CURSOR_RECT/2), CURSOR_Y-int(CURSOR_RECT/2),CURSOR_RECT,CURSOR_RECT),1)

    pygame.display.flip()
    window.update()

pygame.quit()

