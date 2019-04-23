"""
Plot computes a rolling ensemble average to assess the stationarity of the
Holton-Tan effect (QBO-E minus QBO-W)

Notes
-----
    Author : Zachary Labe
    Date   : 5 June 2018
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import nclcmaps as ncm
import datetime
import read_DailyOutput_AllMembers as DO
import read_DailyOutput_AllRegional as DOR
import calc_Utilities as UT
import cmocean

### Define directories
directorydata = '/surtsey/zlabe/simu/'
directorydata2 = '/home/zlabe/green/simu/'
directoryfigure = '/home/zlabe/Desktop/'
#directoryfigure = '/home/zlabe/Documents/Research/SeaIceQBO/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting U30 rolling ensemble average - %s----' % titletime)

### Alott time series
year1 = 1800
year2 = 2000
years = np.arange(year1,year2+1,1)

### Add parameters
varnames = 'U'
runnames = [r'\textbf{FIT}',r'\textbf{HIT}',r'\textbf{FICT}',
            r'\textbf{FIC}',r'\textbf{CIT}',r'\textbf{FSUB}',
            r'\textbf{FPOL}',r'\textbf{CTLQ}']
qbophase = ['pos','non','neg']

### Function to read in control
def readCTLQ(varid,experi,level):
    """
    Function reads daily data from WACCM4 control that are 
    already averaged over latitude/longitude (See script called
    calc_global_ave.proc)

    Parameters
    ----------
    varid : string
        variable name to read
    experi : string
        experiment name (CTLQ)
    level : string
        Height of variable (surface or profile)
        

    Returns
    -------
    lat : 1d numpy array
        latitudes
    lon : 1d numpy array
        longitudes
    time : 1d numpy array
        standard time (days since 1870-1-1, 00:00:00)
    var : 1d or 2d numpy array
        [days] or [days,lev]

    Usage
    -----
    lat,lon,time,lev,var = readCTLQ(varid,experi,level)
    """
    print('\n>>> Using readCTLQ function! \n')
    
    ### Directory 1 for ensemble members 1-200 (remote server - Surtsey)
    directorydatac = '/surtsey/zlabe/simu/'
    
    ### Number of ensembles (years)
    ENS = 200
       
    ### Call files
    if level == 'surface': # 1d variable
        var = np.empty((ENS,365,96,144))
    elif level == 'profile': # 2d variable
        var = np.empty((ENS,365,17))
    
    ### Call files for directory 1 (1-200 members)       
    for i in range(0,ENS,1):
        
        totaldirectory = directorydatac + experi + '/daily/' + experi + \
                        '%s/' % (i+1)
        filename = totaldirectory + varid + '_%s_' % (i+1) + 'mean.nc'
        
        if varid == 'Z500':
            filename = totaldirectory + varid + '_%s.nc' % (i+1)
        elif varid == 'T1000':
            filename = totaldirectory + varid + '_%s.nc' % (i+1)
        
        ### Read in Data
        if level == 'surface': # 3d variables
            data = Dataset(filename,'r')
            time = data.variables['time'][:]
            lev = 'surface'
            lat = data.variables['latitude'][:]
            lon = data.variables['longitude'][:]
            var[i,:,:,:] = data.variables['%s' % varid][:].squeeze()
            data.close()
        elif level == 'profile': # 4d variables
            data = Dataset(filename,'r')
            time = data.variables['time'][:]
            lev = data.variables['level'][:]
            lat = data.variables['latitude'][:]
            lon = data.variables['longitude'][:]
            var[i,:,:] = data.variables['%s' % varid][:]
            data.close()
        else:
            print(ValueError('Wrong height - (surface or profile!)!'))    
        print('Completed: Read data for *%s%s* : %s!' % (experi[:4],
                                                         i+1,varid))
    print('Completed: Read members 1-200!')  
    print('\n*Completed: Finished readCTLQ function!')
    return lat,lon,time,lev,var

### Call functions for variable profile data for polar cap
lat,lon,time,lev,tashit = DO.readMeanExperiAll('%s' % varnames,'HIT',
                                           'profile')
lat,lon,time,lev,tasfit = DO.readMeanExperiAll('%s' % varnames,'FIT',
                                           'profile')
lat,lon,time,lev,tasfict = DO.readMeanExperiAll('%s' % varnames,'FICT',
                                            'profile')
lat,lon,time,lev,tasfic = DO.readMeanExperiAll('%s' % varnames,'FIC',
                                            'profile')
lat,lon,time,lev,tascit = DO.readMeanExperiAll('%s' % varnames,'CIT',
                                            'profile')
lat,lon,time,lev,tasfsub = DOR.readMeanExperiAllRegional('%s' % varnames,
                                            'FSUB','profile')
lat,lon,time,lev,tasfpol = DOR.readMeanExperiAllRegional('%s' % varnames,
                                            'FPOL','profile')
lat,lon,time,lev,tasctlq = readCTLQ('%s' % varnames,'CTLQ','profile')

### Create 2d array of latitude and longitude
lon2,lat2 = np.meshgrid(lon,lat)

### Read in QBO phases 
filenamehitp = directorydata + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[0]
filenamehitn = directorydata + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[2]
filenamehitp2 = directorydata2 + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[0]
filenamehitn2 = directorydata2 + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[2]
pos_hit = np.append(np.genfromtxt(filenamehitp,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamehitp2,unpack=True,usecols=[0],dtype='int')+100)
neg_hit = np.append(np.genfromtxt(filenamehitn,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamehitn2,unpack=True,usecols=[0],dtype='int')+100)    

filenamefitp = directorydata + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[0]
filenamefitn = directorydata + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[2]
filenamefitp2 = directorydata2 + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[0]
filenamefitn2 = directorydata2 + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[2]
pos_fit = np.append(np.genfromtxt(filenamefitp,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefitp2,unpack=True,usecols=[0],dtype='int')+100)
neg_fit = np.append(np.genfromtxt(filenamefitn,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefitn2,unpack=True,usecols=[0],dtype='int')+100)

filenamefictp = directorydata + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[0]
filenamefictn = directorydata + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[2]
filenamefictp2 = directorydata2 + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[0]
filenamefictn2 = directorydata2 + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[2]
pos_fict = np.append(np.genfromtxt(filenamefictp,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefictp2,unpack=True,usecols=[0],dtype='int')+100)
neg_fict = np.append(np.genfromtxt(filenamefictn,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefictn2,unpack=True,usecols=[0],dtype='int')+100)  

filenameficp = directorydata + 'FIC/monthly/QBO_%s_FIC.txt' % qbophase[0]
filenameficn = directorydata + 'FIC/monthly/QBO_%s_FIC.txt' % qbophase[2]
filenameficp2 = directorydata2 + 'FIC/monthly/QBO_%s_FIC.txt' % qbophase[0]
filenameficn2 = directorydata2 + 'FIC/monthly/QBO_%s_FIC.txt' % qbophase[2]
pos_fic = np.append(np.genfromtxt(filenameficp,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenameficp2,unpack=True,usecols=[0],dtype='int')+100)
neg_fic = np.append(np.genfromtxt(filenameficn,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenameficn2,unpack=True,usecols=[0],dtype='int')+100)   

filenamecitp = directorydata + 'CIT/monthly/QBO_%s_CIT.txt' % qbophase[0]
filenamecitn = directorydata + 'CIT/monthly/QBO_%s_CIT.txt' % qbophase[2]
filenamecitp2 = directorydata2 + 'CIT/monthly/QBO_%s_CIT.txt' % qbophase[0]
filenamecitn2 = directorydata2 + 'CIT/monthly/QBO_%s_CIT.txt' % qbophase[2]
pos_cit = np.append(np.genfromtxt(filenamecitp,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamecitp2,unpack=True,usecols=[0],dtype='int')+100)
neg_cit = np.append(np.genfromtxt(filenamecitn,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamecitn2,unpack=True,usecols=[0],dtype='int')+100)    

filenamefsubp = directorydata2 + 'FSUB/monthly/QBO_%s_FSUB.txt' % qbophase[0]
filenamefsubn = directorydata2 + 'FSUB/monthly/QBO_%s_FSUB.txt' % qbophase[2]
filenamefsubp2 = directorydata + 'FSUB/monthly/QBO_%s_FSUB.txt' % qbophase[0]
filenamefsubn2 = directorydata + 'FSUB/monthly/QBO_%s_FSUB.txt' % qbophase[2]
pos_fsub = np.append(np.genfromtxt(filenamefsubp,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefsubp2,unpack=True,usecols=[0],dtype='int')+100)
neg_fsub = np.append(np.genfromtxt(filenamefsubn,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefsubn2,unpack=True,usecols=[0],dtype='int')+100)

filenamefpolp = directorydata2 + 'FPOL/monthly/QBO_%s_FPOL.txt' % qbophase[0]
filenamefpoln = directorydata2 + 'FPOL/monthly/QBO_%s_FPOL.txt' % qbophase[2]
filenamefpolp2 = directorydata + 'FPOL/monthly/QBO_%s_FPOL.txt' % qbophase[0]
filenamefpoln2 = directorydata + 'FPOL/monthly/QBO_%s_FPOL.txt' % qbophase[2]
pos_fpol = np.append(np.genfromtxt(filenamefpolp,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefpolp2,unpack=True,usecols=[0],dtype='int')+100)
neg_fpol = np.append(np.genfromtxt(filenamefpoln,unpack=True,usecols=[0],dtype='int'),
                    np.genfromtxt(filenamefpoln2,unpack=True,usecols=[0],dtype='int')+100)

filenamefctlqp = directorydata + 'CTLQ/monthly/QBO_%s_CTLQ.txt' % qbophase[0]
filenamefctlqn = directorydata + 'CTLQ/monthly/QBO_%s_CTLQ.txt' % qbophase[2]
pos_ctlq = np.genfromtxt(filenamefctlqp,unpack=True,usecols=[0],dtype='int')
neg_ctlq = np.genfromtxt(filenamefctlqn,unpack=True,usecols=[0],dtype='int')

### Concatonate runs with selected level
levq = np.where(lev == 30)[0] # selected at 30 hPa
var_mo = [tashit[:,:,levq],tasfit[:,:,levq],tasfict[:,:,levq],
          tasfic[:,:,levq],tascit[:,:,levq],tasfsub[:,:,levq],tasfpol[:,:,levq],
          tasctlq[:,:,levq]]

### Composite by QBO phase    
var_mofitpos = var_mo[1][pos_fit,:]
var_mohitpos = var_mo[0][pos_hit,:]
var_mofictpos = var_mo[2][pos_fict,:]
var_moficpos = var_mo[3][pos_fic,:]
var_mocitpos = var_mo[4][pos_cit,:]
var_mofsubpos = var_mo[5][pos_fsub,:]
var_mofpolpos = var_mo[6][pos_fpol,:]
var_moctlqpos = np.append(var_mo[7][pos_ctlq[1:],-30:],var_mo[7][(pos_ctlq+1)[:-1],:60],axis=1)

var_mofitneg = var_mo[1][neg_fit,:]
var_mohitneg = var_mo[0][neg_hit,:]
var_mofictneg = var_mo[2][neg_fict,:]
var_moficneg = var_mo[3][neg_fic,:]
var_mocitneg = var_mo[4][neg_cit,:]
var_mofsubneg = var_mo[5][neg_fsub,:]
var_mofpolneg = var_mo[6][neg_fpol,:]
var_moctlqneg = np.append(var_mo[7][neg_ctlq[:],-30:],var_mo[7][(neg_ctlq+1)[:],:60],axis=1)

### Calculate over DJF (90-180)
timeq = np.arange(90,180)
monthqq = 'DJF'
var_wfitpos = var_mofitpos[:-4,timeq]
var_whitpos = var_mohitpos[:-4,timeq]
var_wfictpos = var_mofictpos[:-4,timeq]
var_wficpos = var_moficpos[:-4,timeq]
var_wcitpos = var_mocitpos[:-4,timeq]
var_wfsubpos = var_mofsubpos[:-4,timeq]
var_wfpolpos = var_mofpolpos[:-4,timeq]
var_wctlqpos = var_moctlqpos[:-1,:]

var_wfitneg = var_mofitneg[:,timeq]
var_whitneg = var_mohitneg[:,timeq]
var_wfictneg = var_mofictneg[:,timeq]
var_wficneg = var_moficneg[:,timeq]
var_wcitneg = var_mocitneg[:,timeq]
var_wfsubneg = var_mofsubneg[:,timeq]
var_wfpolneg = var_mofpolneg[:,timeq]
var_wfctlqneg = var_moctlqneg[:,:]

### Calculate difference over time average
difffit = np.nanmean(var_wfitneg - var_wfitpos,axis=1).squeeze()
diffhit = np.nanmean(var_whitneg - var_whitpos,axis=1).squeeze()
difffict = np.nanmean(var_wfictneg - var_wfictpos,axis=1).squeeze()
difffic = np.nanmean(var_wficneg - var_wficpos,axis=1).squeeze()
diffcit = np.nanmean(var_wcitneg - var_wcitpos,axis=1).squeeze()
difffsub = np.nanmean(var_wfsubneg - var_wfsubpos,axis=1).squeeze()
difffpol = np.nanmean(var_wfpolneg - var_wfpolpos,axis=1).squeeze()
diffctlq = np.nanmean(var_wfctlqneg - var_wctlqpos,axis=1).squeeze()

dataq = [difffit,diffhit,difffict,difffic,diffcit,difffsub,difffpol,diffctlq]

### Enter running ensembles
def calcLinearTrend(data,length):
    """
    Calculates moving average for n number of ensembles
    
    Parameters
    ----------
    data : 1d array
        [time series data]
    length : integer
        [n ensembles]
        
    Returns
    -------
    ave : 1d array
        time series of smoothed data from moving average
    
    Usage
    -----
    ave = calcLinearTrend(data,years,length)
    """
    print('\n>>> Using calcMovingAverage function!')
    
    ### Calculate moving average for n months (length)
    aven = np.convolve(data, np.ones((length,))/length, mode='valid') 
    print('Completed: *%s ENSEMBLES* averages!' % length)
    
    ### Append nans for consistent ensembles
    empty = np.array([np.nan]*(length-1))
    ave = np.append(empty,aven,axis=0)
    
    print('*Completed: Finished calcMovingAverage function!\n')    
    return ave

### Enter number of ensembles
N = 40
ensmovfit = calcLinearTrend(difffit,N)
ensmovhit = calcLinearTrend(diffhit,N)
ensmovfict = calcLinearTrend(difffict,N)
ensmovfic = calcLinearTrend(difffic,N)
ensmovcit = calcLinearTrend(diffcit,N)
ensmovfsub = calcLinearTrend(difffsub,N)
ensmovfpol = calcLinearTrend(difffpol,N)
ensmovctlq = calcLinearTrend(diffctlq,N)

###############################################################################
###############################################################################
###############################################################################    
### Plot figure
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([])
        
fig = plt.figure()
ax = plt.subplot(111) 

adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('dimgrey')
ax.spines['bottom'].set_color('dimgrey')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params('both',length=4,width=2,which='major',color='dimgrey')

plt.plot(ensmovfit,color=cmocean.cm.phase(0.1),linewidth=3,
         label=r'\textbf{FIT}',alpha=1,zorder=1)
plt.plot(ensmovhit,color=cmocean.cm.phase(0.2),linewidth=3,
         label=r'\textbf{HIT}',alpha=1,zorder=2)
plt.plot(ensmovfict,color=cmocean.cm.phase(0.35),linewidth=3,
         label=r'\textbf{FICT}',alpha=1,zorder=3)
plt.plot(ensmovfic,color=cmocean.cm.phase(0.5),linewidth=3,
         label=r'\textbf{FIC}',alpha=1,zorder=2)
plt.plot(ensmovcit,color=cmocean.cm.phase(0.65),linewidth=3,
         label=r'\textbf{HIC}',alpha=1,zorder=3)
plt.plot(ensmovfsub,color=cmocean.cm.phase(0.75),linewidth=3,
         label=r'\textbf{FSUB}',alpha=1,zorder=2)
plt.plot(ensmovfpol,color=cmocean.cm.phase(0.9),linewidth=3,
         label=r'\textbf{FPOL}',alpha=1,zorder=3)
plt.plot(ensmovctlq,color=cmocean.cm.phase(0.99),linewidth=3,
         label=r'\textbf{CTLQ}',alpha=1,zorder=3)

plt.axhline(0,color='dimgrey',linestyle='--',dashes=(0.9,1),linewidth=2)

plt.ylabel(r'\textbf{U30 [m/s]}',color='k',fontsize=12)
plt.yticks(np.arange(-8,9,4),list(map(str,np.arange(-8,9,4))))
plt.ylim([-5,5])

l = plt.legend(shadow=False,fontsize=7.5,loc='upper center',
           bbox_to_anchor=(0.5, 1.03),fancybox=True,ncol=8,
            frameon=False,labelspacing=0.2,columnspacing=1)
for text in l.get_texts():
    text.set_color('k')

plt.savefig(directoryfigure + 'movingEnsemblesMean_H-Teffect.png',dpi=300)
    
###############################################################################
###############################################################################
###############################################################################    
### Plot box plot distributions
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([])
        
fig = plt.figure()
ax = plt.subplot(111) 

adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('dimgrey')
ax.spines['bottom'].set_color('w')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params('both',length=4,width=2,which='major',color='dimgrey')
ax.tick_params(axis='x',which='both',bottom=False)

plt.axhline(0,color='dimgrey',linestyle='--',dashes=(0.9,1),linewidth=2)
bx = plt.boxplot(dataq,0,'',patch_artist=True,showmeans=True,meanline=True,
                 whis=[5,95])

for i in bx['caps']:
    i.set(color='k',linewidth=0)
for whisker in bx['whiskers']:
    whisker.set(color='dimgrey',linestyle='-',linewidth=2)
for box in bx['boxes']: 
    box.set(color='deepskyblue')
for box in bx['means']:
    box.set(color='r',linewidth=2,linestyle='-')
for box in bx['medians']:
    box.set(linewidth=0)
    
for i in range(len(dataq)):
    y = dataq[i]
    x = np.random.normal(1+i,0.04,size=len(y))
    plt.plot(x,y,'r.',alpha=0.3,zorder=5)

plt.ylabel(r'\textbf{U30 [m/s]}',color='k',fontsize=12)

plt.yticks(np.arange(-20,21,5),list(map(str,np.arange(-20,21,5))))
plt.xticks(np.arange(1,9,1),runnames) 
plt.ylim([-18,18])

plt.savefig(directoryfigure + 'distributions_H-Teffect_%s.png' % monthqq,dpi=300)
