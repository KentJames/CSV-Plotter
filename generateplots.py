""" Will take a CSV file and generate a plot of data """

import argparse
import textwrap
import matplotlib.pyplot as plt
import csv
import os


class PlotGenerator_CLI(object):
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
        self.command.add_argument('X_Column', metavar='X', help=
                                        ('Column of the CSV file to plot on the X Axis.'))
        self.command.add_argument('Y_Columns',metavar='Y',help='Plots these columns against X input. For multiple columns use [variable1,variable2].')
        self.command.add_argument('output_file',metavar='O',help='Saves plot to this PNG filepath.')

        #Optional arguements.
        self.command.add_argument('--echocommands',dest='echocommands',action='store_true',help='Echo Commands Back. Stops profiler from running. For debugging.')
        #self.command.add_argument('--power=',dest='powerof',default='2',help='Specifies what factor to test powers of, e.g 3^N, 7^N, 11^N etc. If this argument is not stated the default is 2^N.')
        self.command.add_argument('--generateplot',dest='generateplot',action='store_true',help='Show plot in window. If not selected, script will only output to a file')
        self.command.add_argument('--recursive',dest='recursive',action='store_true',help='Recursively generates png plots for every csv file found in a directory. Not compatible with generateplot (will be ignored).') 
        self.command.add_argument('--directory',dest='directory',action='store_true',help='Tells plotter to search a directory for csv files and try and plot every single one. Not  compatible with generate plot (will be ignored).')
        self.command.add_argument('--directoryext=',dest='directoryext',default='.pdf',help='Tells plotter what type of output file to save to. Default is PDF file.')
        self.command.add_argument('--multipleplots',dest='multipleplots',action='store_true',help='Look at multiple CSV files and take the same column from each and plot them all on same plot.')
    

        self.args = self.command.parse_args()


        if(self.args.echocommands is True):
            self.echo_commands()
        elif(self.args.multipleplots is True):
            self.processcsvfile_multiple()
        elif(self.args.directory is True):
            self.processdirectory()
        else:
            self.processcsvfile()

    def echo_commands(self):
        '''Mostly for debug purposes when changing CLI.'''

        print("Received arguments: \n")
        print(self.args) 


    def processcsvfile(self):
        '''Instantiates Output_Plot object which plots and saves a png or pdf file. Can show it to user too.'''

        if((self.args.output_file.split('.')[1] == 'png') or (self.args.output_file.split('.')[1] == 'pdf')):
        
            Output_Plot(self.args)

        else:

            print("Invalid output file specified. PNG or GIF only.")
            print("Exiting...")
            quit()


    def processdirectory(self):
        '''Instantiates directory plot object.'''

        #Bit of error checking to avoid silly mistakes!
        if(os.path.isdir(self.args.output_file) is False):
            print("Output directory string not valid.")
            print("Exiting...")
            quit()
        elif(os.path.isdir(self.args.filepath) is False):
            print("CSV directory string not valid. Did you specify a .csv file instead of a directory containing csv files?")
            print("Exiting...")
            quit()
        else:

            Directory_Plot(self.args)

    def processcsvfile_multiple(self):
        
        multiple_paths = self.args.filepath.split(',')
    
        #Bit of extra code to add some robustness.
        for filepaths in multiple_paths:
            if(filepaths.endswith('.csv') is False):
                print("One of these files is not a csv file. Check your input arguments!")
                print("Exiting...")
                quit()
        
        if((self.args.output_file.split('.')[1] == 'png') or (self.args.output_file.split('.')[1] == 'pdf')):
             Multiple_Plot(self.args)



# Parent object for parsing CSV file and outputting data required for putting into plots.
class CSV_Parser(object):
    '''Handles all the CSV reading, column extracting and the main part of plotting.'''
    '''Change the matplotlib code in the Plot_Data method to vary how the individual plots look. '''

    def __init__(self,filename,XColumn,YColumns):

        self.filename = filename
        self.XColumn = XColumn
        self.YColumns = YColumns.split(',')

        self.csvdata_raw = []
        self.csvdata_columns = []
        self.ParseCSV(self.filename)
        self.Extract_Columns()


    def ParseCSV(self,csvfilename):
        '''Pretty simple: extracts data from csv files as rows.'''

        with open(csvfilename,'r') as filename:
            reader = csv.reader(filename,delimiter=',')
            for row in reader:
                self.csvdata_raw.append(row)


    def Extract_Columns(self):
        '''Re-arranges data to be in columns instead of rows, which is what everyone prefers for plotting... '''    

        column_index = []
        csv_data = []
        csv_concatenated_data = []
        #print(self.csvdata_raw)

        column_index.append(int(self.XColumn))
        
        for x in self.YColumns:
            column_index.append(int(x))

        for csv_column in range(0,len(self.csvdata_raw[0])):
            #print(csv_column)
            for csv_row in self.csvdata_raw:
            #    print(csv_row)
                csv_data.append(csv_row[csv_column])
            #print(csv_data)
            csv_concatenated_data.append(csv_data)
            csv_data=[]
        self.csvdata_columns = csv_concatenated_data
        

    def Plot_Data(self,filename):
        '''Plots CSV data using matplotlib. Works for a single file only.'''


        #Horrible way of doing this, but I couldn't think of anything else at the time.
        colors=['bs','r--','g^']
        xdata_name = self.csvdata_columns[int(self.XColumn)][0]
        ydata_name = self.csvdata_columns[int(self.YColumns[0])][0]
        #Change anything here to vary how the plot looks:
        for Y_Data in self.YColumns:

            plt.plot(self.csvdata_columns[0][1:],self.csvdata_columns[int(Y_Data)][1:],colors[int(Y_Data)%3],label=self.csvdata_columns[int(Y_Data)][0])
        
        plt.xlabel(xdata_name)
        plt.ylabel(ydata_name)
        plt.title(filename)
        plt.legend(filename)
        #plt.show()

# Child of CSV_Parser and outputs data collected to PNG file.
class Output_Plot(CSV_Parser):
    '''Plots a single CSV File and saves it to a file. Will also display to user if --generateplot set on CLI'''

    def __init__(self,args):

        #Instantiate parent object
        super().__init__(args.filepath,args.X_Column,args.Y_Columns)
        #self.CSV_Parser = CSV_Parser(csvfilename,XColumn,YColumns)
        self.generateplot = args.generateplot
        self.outputfile = args.output_file
        self.Plot_Data()

    def Plot_Data(self):
        '''Mostly piggybacks on parent method. Just saves plot to file then shows it to user. One would argue why the fuck I did it this way at all, trying to be smart I guess...'''

        #Call parent method.
        super().Plot_Data(self.filename)
        
        #Turns out you need to save before you show it to the user in matplotlib. Bit weird...
        print("Saving plot to: {}".format(self.outputfile))
        plt.savefig(self.outputfile)
        
        #Show to user.
        if(self.generateplot==True):
            plt.show()

class Multiple_Plot(object):
    '''Plots the same column from several csv files.'''

    def __init__(self,args):
        
        self.args = args
        self.filepaths = args.filepath.split(',')
        self.XColumn = args.X_Column
        self.YColumns = args.Y_Columns
        self.outputfilepath = args.output_file

        self.Plot_Data()

    def Plot_Data(self):
        '''Cannibalised from the CSV_Parser method. There is definitely a nicer way of doing this, but this seems to do the job. Still reuse most of CSV_Parser though!'''

        i = 0
        for filepath in self.filepaths:
            i=i+1
            csvparser = CSV_Parser(filepath,self.XColumn,self.YColumns)
            #csvparser.Plot_Data(filepath)
            #Horrible way of doing this, but I couldn't think of anything else at the time.
            colors=['b--','r--','g--','c--','m--','y--','k--','w--','b^','r^','g^','c^','m^']
            xdata_name = csvparser.csvdata_columns[int(self.XColumn)][0]
            ydata_name = csvparser.csvdata_columns[int(self.YColumns[0])][0]
            #Change anything here to vary how the plot looks:
            for Y_Data in self.YColumns:

                plt.plot(csvparser.csvdata_columns[0][1:],csvparser.csvdata_columns[int(Y_Data)][1:],colors[i%13],label=csvparser.csvdata_columns[int(Y_Data)][0])
            #Set labels to that of last file to make life easier...
            plt.xlabel(xdata_name)
            plt.ylabel(ydata_name)

        print("Generating {}".format(self.outputfilepath))

        plt.title('Multiple:'+str(self.filepaths))

        plt.legend(self.filepaths)
        plt.savefig(self.outputfilepath)

        if(self.args.generateplot == True):
            plt.show()




# Child of CSV_Parser and outputs data collected to GIF file. 
class Directory_Plot(object):
    '''Looks at a whole directory of CSV files and plots them to output directory. Won't show to user as that would be hideous. '''

    def __init__(self,args):
        
        self.args = args
        self.csvfilepaths = []
        self.directorypath = args.filepath
        self.XColumn = args.X_Column
        self.YColumns = args.Y_Columns
        self.outputfilepath = args.output_file
        self.SearchDirectory(self.directorypath)

        self.Plot_Data()


    def SearchDirectory(self,filepath):
        '''Searches directory for any csv files. TODO: Add a walk option?'''

        for filepathcsv in os.listdir(filepath):
            if filepathcsv.endswith(".csv"):
                self.csvfilepaths.append(filepathcsv)




    def Plot_Data(self):
        '''Plots every csv file in the directory.'''

        for filepath in self.csvfilepaths:
            csvparser = CSV_Parser(filepath,self.XColumn,self.YColumns)
            csvparser.Plot_Data(filepath)

            path = self.outputfilepath+'/'+filepath.split('.')[0]+self.args.directoryext
            print("Generating {}".format(path))
            plt.savefig(path)
            plt.clf()




if __name__ == "__main__":
    PlotGenerator =  PlotGenerator_CLI()
