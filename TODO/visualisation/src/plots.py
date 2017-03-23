import sys,os,yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from parameters import NP, A
from summarystats import SummaryStats

class Process_parameters():    
    def plot_parameters(self):
        with open("plot_config.yaml", 'r') as stream:
            try:
                param = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        #for key, value in param.iteritems():           
        #print param[key]['plot_type']
        #print value 
        return param   

class Parameter_mapper():

    def __init__(self, param):
        self.__param = param
        
    def legend(self, key):
        return self.__param[key]['plot_legend']

    def legend_label(self, key):
        return self.__param[key]['legend_label']

    def plot_type(self, key):
        return self.__param[key]['plot_type']

    def num_plots(self, key):
        return self.__param[key]['number_plots']

    def y_label(self, key):
        return self.__param[key]['y-axis label']

    def x_label(self, key):
        return self.__param[key]['x-axis label']

    def plot_name(self, key):
        return self.__param[key]['plot_name']

    def llim(self, key):
        return self.__param[key]['l_lim']

    def ulim(self, key):
        return self.__param[key]['u_lim']

    def linestyle(self, key):
        return self.__param[key]['linestyle']


class Plot(NP,Parameter_mapper):
    def __init__(self, idx, data):
        self.__data = data
        self.key = idx
        PP = Process_parameters()
        self.__parameter = PP.plot_parameters()
        self.__param_map = Parameter_mapper(self.__parameter)   

    def timeseries( self, n, analysis_type ):     
        T = Timeseries(self.__data, n, analysis_type, self.__parameter, self.key)      
        one_plot = lambda : T.one_output()
        many_plot = lambda : T.many_output()        
        options = {'one' : one_plot, 'many' : many_plot}
        #return options['one']()      
        return options[self.__param_map.num_plots(self.key)]()

    def histogram( self, n ):          
        H = Histogram(self.__data, num_plots, n)      
        one_plot = lambda : H.one_output()
        many_plot = lambda : H.many_output()        
        options = {'one' : one_plot, 'many' : many_plot}        
        return options[self.__param_map.num_plots(self.key)]()

    def boxplot( self, n, analysis_type ):
        B = Boxplot(self.__data, n, analysis_type, self.__parameter, self.key)      
        one_plot = lambda : B.one_output()
        many_plot = lambda : B.many_output()        
        options = {'one' : one_plot, 'many' : many_plot} 
        return options[self.__param_map.num_plots(self.key)]()


class Timeseries(A):

    def __init__(self, data, n, a, parameter, key):
        self.__data = data
        print self.__data.head(10)
        print len(self.__data.columns)
        self.__N = n
        self.__analysistype = a
        self.__parameter = parameter
        self.__param_map = Parameter_mapper(self.__parameter)
        self.key = key
                
    def many_output(self):
        if self.__analysistype == A.agent:
            print " -Warning: too many plots will be produced !!! " 
            count = 0                        
            minor_index = self.__data.index.get_level_values('minor').unique()  # get the index values for minor axis, which will later be used to sort the dataframe 
            for i in minor_index:
                D = self.__data.xs( int(i) , level='minor')
                   
                for i in range(0,len(D),self.__N):
                    y = np.array(D[i:i+self.__N])                
                    x = np.linspace(0, self.__N, self.__N, endpoint=True)
                    plt.plot(x,y,color = 'blue', linestyle=self.__param_map.linestyle(self.key), marker='o', markerfacecolor = 'green', markersize =4, label = self.__param_map.x_label(self.key)) 
                    plot_name = self.__param_map.plot_name(self.key)[:-4]+str(count)+".png"              
                    plt.savefig(plot_name, bbox_inches='tight')
                    plt.close()
                    count = count + 1	                
        else:
            y =[]
            for i in range(0,len(self.__data),self.__N):
                y.append(np.array(self.__data[i:i+self.__N]))        
            count = 0            
            for i in range(0,len(self.__data)/self.__N):
                x = np.linspace(0, self.__N, self.__N, endpoint=True)
                plt.plot(x,y[i],color = 'blue', linestyle=self.__param_map.linestyle(self.key), marker='o', markerfacecolor = 'green', markersize =4, label = self.__param_map.legend_label(self.key)) 
                plot_name = self.__param_map.plot_name(self.key)[:-4]+str(count)+".png"
                plt.savefig(plot_name, bbox_inches='tight')	 
                count = count + 1
                plt.clf() # clear current figure
            plt.close()    
    
    def one_output(self):
        if self.__analysistype == A.agent:
            print " -Warning: too many lines will be printed in a single plot !!! "
            minor_index = self.__data.index.get_level_values('minor').unique()  # get the index values for minor axis, which will later be used to sort the dataframe 
            for i in minor_index:
                D = self.__data.xs( int(i) , level='minor')
            count = 0          
            for i in range(0,len(D),self.__N):
                y = np.array(D[i:i+self.__N])
                x = np.linspace(0, self.__N, self.__N, endpoint=True)
                #print x

                plt.plot(x,y, linestyle = self.__param_map.linestyle(self.key), marker='o', markerfacecolor = 'green', markersize =1, label = self.__param_map.legend_label(self.key)+"_"+str(count))
                count = count + 1
                plt.hold(True)
            plt.legend(loc='best', fancybox=True, shadow=True)
            plot_name = self.__param_map.plot_name(self.key) 
            plt.savefig(plot_name, bbox_inches='tight')
            plt.close()

        else:
            self.__data.plot(kind = 'line')
            plt.show()
            print "aba main kaam kuro"
            y =[]
            for i in range(0,len(self.__data),self.__N):
                y.append(np.array(self.__data[i:i+self.__N])) # y values are appended here, if dataframe has more than one columns, all the columns are appended           
            count = 0
            print len(self.__data)
            print self.__N
            
            for i in range(0,len(self.__data)/self.__N):
                x = np.linspace(0, self.__N, self.__N, endpoint=True)
            print "i ko value hai",i
            print len(y)            
            print len(y[0])
            #TODO: separate plotting from here, and add separate legend, now same legend, also add fill in
            # when plotting, if df has two cols, in case of two quantiles, both plotted simultaneously, i.e. x against array y of 2 values
            plt.plot(x,y[i],color = 'blue', linestyle=self.__param_map.linestyle(self.key), marker='o', markerfacecolor = 'green', markersize =1, label = self.__param_map.legend_label(self.key)) 
            
            plt.hold(True)
            count = count + 1     	 
            plt.legend(loc='best', fancybox=True, shadow=True)
            plot_name = self.__param_map.plot_name(self.key)            
            plt.savefig(plot_name, bbox_inches='tight')
            plt.close()


class Histogram():

    def __init__(self, data, num_plots, n):
        self.__data = data
        self.__N = n

    def many_output(self): ####TODO###
        return
        y =[]
        for i in range(0,len(self.__data),self.__N):
            y.append(np.array(self.__data[i:i+self.__N]))
        for i in range(0,len(self.__data)/self.__N):
            hist, bins = np.histogram(y[i],bins = 50)
            width = 0.7 * (bins[1] - bins[0])
            center = (bins[:-1] + bins[1:]) / 2
            plt.bar(center, hist, align='center', width=width)
            #plt.show()
            #plt.plot(x,y[i])
            plot_name = "histogram_"+str(i)+".png"
            plt.savefig(plot_name, bbox_inches='tight')	 
            
            # plt.show() # reset the plot, but gives output in display
            # So, alternatively:
            # plt.cla() # clear current axes
            plt.clf() # clear current figure
            # plt.close() # close the whole plot
        plt.close()    
    
    def one_output(self):
        self.__data.hist(bins = 50)
        plt.savefig('histogram_main.png', bbox_inches='tight')
        plt.close()


class Boxplot(NP, A):
    def __init__(self, data, n, a_type, parameter, key):
        self.__data = data
        self.__N = n
        self.__a_type = a_type
        self.__parameter = parameter
        self.__param_map = Parameter_mapper(self.__parameter)
        self.key = key     
  

    def one_output(self):
        s = SummaryStats(self.__data, self.__a_type )   
        box_df = pd.DataFrame()
        box_df['mean'] = [x for sublist in s.mean().values for x in sublist]  # [x for sublist in s.mean().values for x in sublist] done to flatten a 2D list to 1D so pandas accepts it
        # box_df['mean'] = s.mean() # this was the old simpler method which did not work once the config file variables was turned to a hierarchy with filters (bug in df, see for new patches)
        box_df['median'] = [x for sublist in s.median().values for x in sublist]
        box_df['upper_quartile'] = [x for sublist in s.upper_quartile().values for x in sublist]
        box_df['lower_quartile'] = [x for sublist in s.lower_quartile().values for x in sublist]
        box_df['max'] = [x for sublist in s.maximum().values for x in sublist]
        box_df['min'] = [x for sublist in s.minimum().values for x in sublist]

        # box_df['mean'].plot() # shortcut pandas method to plot the whole thing
        # box_df.plot()
        # plt.show()
        
        t_df = box_df.T
        t_df = t_df.mean(axis =1)
        bp = t_df.to_frame().boxplot()
        #bp = box_df.boxplot(column = ['min','median','mean','upper_quartile','lower_quartile','max'], positions =[1,3,4,5,2,6])
        # plt.hold(True)   
        plot_name = self.__param_map.plot_name(self.key)            
        plt.savefig(plot_name, bbox_inches='tight')      
        plt.clf()

    def many_output(self):
        print "many ma ni aaucha ta?"
        s = SummaryStats(self.__data, self.__a_type )           
        box_df = pd.DataFrame()
        box_df['mean'] = s.mean()
        box_df['median'] = s.median()
        box_df['upper_quartile'] = s.upper_quartile()
        box_df['lower_quartile'] = s.lower_quartile()
        box_df['max'] = s.maximum()
        box_df['min'] = s.minimum()

        count = 0
        for i in range(0,len(box_df.index)/self.__N):                    
            tmp_df = box_df[count:count+self.__N]
            bp = tmp_df.boxplot(column = ['min','median','mean','upper_quartile','lower_quartile','max'], positions =[1,3,4,5,2,6])
            plot_name = "boxplot_"+str(i)+".png"        
            plt.savefig(plot_name, bbox_inches='tight')  
            plt.clf()           
            count = count + self.__N
        plt.close()

