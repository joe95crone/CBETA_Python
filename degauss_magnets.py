# JC Degauss/Standardize Magnets
# 04/11/2019
# S3 + S4 dipoles and quads currently don't have setpoint values so the program would currently just be degaussing these not standardizing them


def degauss_magnets():

        # CHOOSE MAGNETS + LIST FOR SETPOINTS
        trial_magnets = ["MS1DIP03","MS2DIP04","MS3DIP03","MS2DIP02","MS4DIP02","MS1DIP01","MS1QUA02","MS1QUA06","MS2QUA05","MS4QUA04","MS2DIP01", "MS4DIP01","MS3CRV02","MS1CRV01"]
        # trial of 1 of every magnet - S4 + S3 and V corr have a nominal value of 0 so would just be normal degaussing right now
        # also included an extra air cooled quad for data comparison
        
        trial_magnet_setpoint = [caget_many([x + "_cmd" for x in trial_magnets]) ,caget_many([x + "_cmd.DRVH" for x in trial_magnets]),caget_many([x + "cmd.DRVL" for x in trial_magnets])] 
        
        # SET DEGAUSSING PARAMETERS
        N_pts = 40
        pause_time = 2
        swing_current = 1
        
        caput_many(["degauss:" + x + "_N_pts" for x in trial_magnets],[No_pts]*len(trial_magnets))
        caput_many(["degauss:" + x + "_pause" for x in trial_magnets],[pause_time]*len(trial_magnets))
        caput_many(["degauss:" + x + "_amplitude" for x in trial_magnets],[swing_current]*len(trial_magnets))
        
        
        for nmag in the range (0:len(trial_magnets):
            
            if (trial_magnet_setpoint[0][nmag] + swing_current) > trial_magnet_setpoint[1][nmag] or (trial_magnet_setpoint[0][nmag] - swing_current) < trial_magnet_setpoint[2][nmag]:

                print("Outside of Power Supply Tolerance in EPICS: ", trial_magnets[nmag])  
                return
                
            else:
                
                caput("degauss:" + trial_magnets[0][nmag] , caget( trial_magnets[0][nmag] + "_cmd")            
