""" Creates surface plot from 2D CSV File. """

import argparse
import textwrap
import csv
import os

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

class SurfacePlot_CLI(object):

    '''Command line interface. Main entrance point for the program.'''

    def __init__(self):
        self.args = None
        self.command = None

        self.parse_commandline()     

    def parse_commandline(self):
        '''Parses Command line arguments and initiates rest of program.'''

        #Instantiate command line parser.
        self.command = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''
                                                            Plotting Utility v0.1.
                                                            Author: James Kent. 
                                                            Email: jameschristopherkent@gmail.com

                                                            Takes a CSV File and Plots and outputs to csv file.'''))

        
        #Add required arguments.
        self.command.add_argument('filepath',help=
                                 ('CSV File Path'))
        self.command.add_argument('--echocommands',dest='echocommands',action='store_true',help='Echo Commands Back. Stops profiler from running. For debugging.')
        #self.command.add_argument('--power=',dest='powerof',default='2',help='Specifies what factor to test powers of, e.g 3^N, 7^N, 11^N etc. If this argument is not stated the default is 2^N.')    

        self.args = self.command.parse_args()


        if(self.args.echocommands is True):
            self.echo_commands()

    def echo_commands(self):
        '''Mostly for debug purposes when changing CLI.'''

        print("Received arguments: \n")
        print(self.args) 


class twoD_CSV_Parser(object):

    def __init__(self,args):

        self.args = args

    def load_from_csv(self):
        
        csvar = np.loadtxt(open(self.args.filepath,"rb"), delimiter=",")
        print(csvar[1:,1:])

        x_leg = csvar[:,0]
        y_leg = csvar[0,:]

        self.create_surface_plot(csvar)
        
    def create_surface_plot(self,data):
        '''Assumes first column/row is the legend values.'''
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        x_dat = data[1:,0]
        y_dat = data[0,:]

        X = np.arange(20,90,10)
        Y = np.arange(100,1100,100)

        print(X)
        
        Y = np.append(Y,2000)
        print(Y)
        X, Y = np.meshgrid(X, Y)

        print(data[1:,1:])
        print(X)
        print(Y)
        print("Shape X: {} Shape Y: {} Shape Data: {}".format(np.shape(X),np.shape(Y),np.shape(data[1:,1:])))
        
        surf = ax.plot_surface(X, Y, data[1:,1:], cmap=cm.coolwarm,
                               linewidth=0, antialiased = False)
        
        ax.set_zlim(-1.01, 20.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()
    
def main():

    cli = SurfacePlot_CLI()

    parse = twoD_CSV_Parser(cli.args)
    parse.load_from_csv()

    


    

if __name__=="__main__":
    main()
