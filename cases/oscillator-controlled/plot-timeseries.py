import pandas as pd
from matplotlib import pyplot as plt
import argparse
from enum import Enum


class PlotType(Enum):
    POS_OVER_T = "position over time"
    V_OVER_T = "velocity over time"
    U1_OVER_T = "control output 1 over time"
    U2_OVER_T = "control output 2 over time"
    E_OVER_T = "error over time"
    P_OVER_T = "proportional term over time"
    I_OVER_T = "integral term over time"
    D_OVER_T = "derivative term over time"
    


parser = argparse.ArgumentParser()
parser.add_argument("csvFile", help="CSV file.", type=str)
parser.add_argument("plotType", help="Plot type.", type=str, choices=[pt.name for pt in PlotType])
args = parser.parse_args()

filename = args.csvFile
split_filename = filename.split('/')
solver = split_filename[0]

if solver == 'python':
    df = pd.read_csv(filename, delimiter=';')
    if args.plotType == PlotType.POS_OVER_T.name:
        plt.plot(df['time'], df['position'])
        plt.title(PlotType.POS_OVER_T.value)
    elif args.plotType == PlotType.V_OVER_T.name:
        plt.plot(df['time'], df['velocity'])
        plt.title(PlotType.V_OVER_T.value)
    else:
        print("Warning: Oscillator can not plot controller values over time.")  
elif solver == 'fmi':
    df = pd.read_csv(filename, delimiter=',')
    if args.plotType == PlotType.U1_OVER_T.name:
        plt.plot(df['time'], df['u_1'])
        plt.title(PlotType.U1_OVER_T.value)
    elif args.plotType == PlotType.U2_OVER_T.name:
        plt.plot(df['time'], df['u_2'])
        plt.title(PlotType.U2_OVER_T.value)
    elif args.plotType == PlotType.E_OVER_T.name:
        plt.plot(df['time'], df['e'])
        plt.title(PlotType.E_OVER_T.value)
    elif args.plotType == PlotType.P_OVER_T.name:
        plt.plot(df['time'], df['P'])
        plt.title(PlotType.P_OVER_T.value)
    elif args.plotType == PlotType.I_OVER_T.name:
        plt.plot(df['time'], df['I'])
        plt.title(PlotType.I_OVER_T.value)
    elif args.plotType == PlotType.D_OVER_T.name:
        plt.plot(df['time'], df['D'])
        plt.title(PlotType.D_OVER_T.value)
    else:
        print("Warning: Controller can not plot oscillator values over time.") 

plt.show()
