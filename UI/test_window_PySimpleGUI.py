import PySimpleGUI as sg                       

layout = [  [sg.Text("This is a test window.")],    
            [sg.Button('Ok')] ]

window = sg.Window('Test Window', layout)     
                                                
event, values = window.read()                  
print(event, values)

window.close()                                 

