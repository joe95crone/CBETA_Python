# JC Degauss/Standardize Magnets All
# 01/11/2019
# S3 + S4 dipoles and quads currently don't have setpoint values so the program would currently just be degaussing these not standardizing them

# PSEUDO 
# get list of magnets 
# caget_many to get the drive high, drive lows + setpoints (3xnmag array)
# set variables
# for loop to set all N_pts, Pause, Amplitude (swing value)
# check current doesn't exceed the drive high or drive low + return bad magnet name + break code if so [NEED FLAG FOR WHICH WAY]
# caput_many to set the degaussing procedure going

from epics import caget, caput, caget_many, caput_many
from pyiocs.utilities.user_tools import vprint

def degauss_magnets():

        # CHOOSE MAGNETS + LIST FOR SETPOINTS

        trial_magnets = [ ]
        f = open("field_strength.cal","r")
        h = f.readlines()
        
        for find_magnets in range(0,len(h)):

            if  'DIP'  in h[find_magnets][3:6] :
                trial_magnets.append(h[find_magnets][:8])
            elif 'QUA' in h[find_magnets][3:6] : 
                trial_magnets.append(h[find_magnets][:8])
            elif 'CRV' in h[find_magnets][3:6] :
                trial_magnets.append(h[find_magnets][:8])                

        trial_magnets = trial_magnets[13:] 
        # excludes dump and diagnostic magnets

        # trial_magnets = ["MD2DIP01","MD2QUA02"]
        # test magnets in dump
        
        # CREATE 2D ARRAY OF SETPOINTS AND LIMITS

        trial_magnet_setpoint = [caget_many([x + "_cmd" for x in trial_magnets]) ,caget_many([x + "_cmd.DRVH" for x in trial_magnets]),caget_many([x + "_cmd.DRVL" for x in trial_magnets])]

        # array of setpoint, drive high, drive low current values, caget_many to get each parameter for each magnet, list comprehension used to add needed string to magnet name 
        
        # SET VARIABLES
        No_pts = 25
        pause_time = 2
        swing_current = 1
        
        # SET DEGAUSSING PARAMETERS

        caput_many(["degauss:" + x + "_N_pts" for x in trial_magnets],[No_pts]*len(trial_magnets))
        caput_many(["degauss:" + x + "_pause" for x in trial_magnets],[pause_time]*len(trial_magnets))
        caput_many(["degauss:" + x + "_amplitude" for x in trial_magnets],[swing_current]*len(trial_magnets))
        
        # FOR LOOP TO STOP EXCEEDING POWER SUPPLIES

        for nmag in range(0,len(trial_magnets)):
        
             if (trial_magnet_setpoint[0][nmag] + swing_current) > trial_magnet_setpoint[1][nmag] or (trial_magnet_setpoint[0][nmag] - swing_current) < trial_magnet_setpoint[2][nmag]:

                print("Outside of Power Supply Tolerance in EPICS: ", trial_magnets[nmag])  
                return
                
        # SET THE STANDARDIZATION PROCEDURE TO RUN
        #caput degauss:MAGNETNAME_cmd TargetValue
        #caput_many(["degauss:" + x + "_cmd" for x in trial_magnets],caget_many([x + "_cmd" for x in trial_magnets]))

        # CHECK IF SUCCESSFUL
        vprint("...Magnets Standardizing",True,0,True)