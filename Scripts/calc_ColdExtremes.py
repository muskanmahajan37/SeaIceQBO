"""
Plot comparisons between WACCM4 sea ice experiments. These are 
sea ice thickness and concentration perturbation experiments. This script is
for DAILY data for temperature extremes at 1000 hPa (10%)

Notes
-----
    Author : Zachary Labe
    Date   : 21 May 2018
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import nclcmaps as ncm
import datetime
import read_DailyOutput_AllMembers as DO
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
print('\n' '----Plotting Daily T1000 for SeaIceQBO - %s----' % titletime)

#### Alott time series
year1 = 1800
year2 = 2000
years = np.arange(year1,year2+1,1)

### Add parameters
MASK = True
varnames = ['T1000']
runnames = [r'HIT',r'FIT',r'FICT']
experiments = [r'\textbf{FIT--HIT}',r'\textbf{FIT--HIT}',
               r'\textbf{FICT--HIT}',r'\textbf{FICT--HIT}']
qbophase = ['pos','non','neg']

### Call functions for variable profile data for polar cap
for v in range(len(varnames)):
    ### Call function for surface temperature data from reach run
    lat,lon,time,lev,tashit = DO.readMeanExperiAll('%s' % varnames[v],'HIT',
                                               'surface')
    lat,lon,time,lev,tasfit = DO.readMeanExperiAll('%s' % varnames[v],'FIT',
                                               'surface')
    lat,lon,time,lev,tasfict = DO.readMeanExperiAll('%s' % varnames[v],'FICT',
                                                'surface')
    
    ### Create 2d array of latitude and longitude
    lon2,lat2 = np.meshgrid(lon,lat)
    
    ### Read in QBO phases 
    filenamehitp = directorydata + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[0]
    filenamehitno = directorydata + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[1]
    filenamehitn = directorydata + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[2]
    filenamehitp2 = directorydata2 + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[0]
    filenamehitno2 = directorydata2 + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[1]
    filenamehitn2 = directorydata2 + 'HIT/monthly/QBO_%s_HIT.txt' % qbophase[2]
    pos_hit = np.append(np.genfromtxt(filenamehitp,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamehitp2,unpack=True,usecols=[0],dtype='int')+100)
    non_hit = np.append(np.genfromtxt(filenamehitno,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamehitno2,unpack=True,usecols=[0],dtype='int')+100)
    neg_hit = np.append(np.genfromtxt(filenamehitn,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamehitn2,unpack=True,usecols=[0],dtype='int')+100)    

    filenamefitp = directorydata + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[0]
    filenamefitno = directorydata + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[1]
    filenamefitn = directorydata + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[2]
    filenamefitp2 = directorydata2 + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[0]
    filenamefitno2 = directorydata2 + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[1]
    filenamefitn2 = directorydata2 + 'FIT/monthly/QBO_%s_FIT.txt' % qbophase[2]
    pos_fit = np.append(np.genfromtxt(filenamefitp,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamefitp2,unpack=True,usecols=[0],dtype='int')+100)
    non_fit = np.append(np.genfromtxt(filenamefitno,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamefitno2,unpack=True,usecols=[0],dtype='int')+100)
    neg_fit = np.append(np.genfromtxt(filenamefitn,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamefitn2,unpack=True,usecols=[0],dtype='int')+100)
    
    filenamefictp = directorydata + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[0]
    filenamefictno = directorydata + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[1]
    filenamefictn = directorydata + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[2]
    filenamefictp2 = directorydata2 + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[0]
    filenamefictno2 = directorydata2 + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[1]
    filenamefictn2 = directorydata2 + 'FICT/monthly/QBO_%s_FICT.txt' % qbophase[2]
    pos_fict = np.append(np.genfromtxt(filenamefictp,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamefictp2,unpack=True,usecols=[0],dtype='int')+100)
    non_fict = np.append(np.genfromtxt(filenamefictno,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamefictno2,unpack=True,usecols=[0],dtype='int')+100)
    neg_fict = np.append(np.genfromtxt(filenamefictn,unpack=True,usecols=[0],dtype='int'),
                        np.genfromtxt(filenamefictn2,unpack=True,usecols=[0],dtype='int')+100)   
    
    ### Concatonate runs
    var_mo = [tashit,tasfit,tasfict]
    
    ### Composite by QBO phase    
    var_mofitpos = var_mo[1][pos_fit,:,:] - 273.15
    var_mohitpos = var_mo[0][pos_hit,:,:] - 273.15
    var_mofictpos = var_mo[2][pos_fict,:,:] - 273.15
    
    var_mofitnon = var_mo[1][non_fit,:,:] - 273.15
    var_mohitnon = var_mo[0][non_hit,:,:] - 273.15
    var_mofictnon = var_mo[2][non_fict,:,:] - 273.15
    
    var_mofitneg = var_mo[1][neg_fit,:,:] - 273.15
    var_mohitneg = var_mo[0][neg_hit,:,:] - 273.15
    var_mofictneg = var_mo[2][neg_fict,:,:] - 273.15
    
    ### Calculate over DJF (90-180)
    timeq = np.arange(90,120)
    monthqq = 'Dec'
    var_wfitpos = var_mofitpos[:,timeq,:,:]
    var_whitpos = var_mohitpos[:,timeq,:,:]
    var_wfictpos = var_mofictpos[:,timeq,:,:]
    
    var_wfitneg = var_mofitneg[:,timeq,:,:]
    var_whitneg = var_mohitneg[:,timeq,:,:]
    var_wfictneg = var_mofictneg[:,timeq,:,:]
    
    ### Compute 10th percentile temperature at each grid point
    ten_wfitpos = np.empty((var_wfitpos.shape[0],lat.shape[0],lon.shape[0]))
    ten_whitpos = np.empty((var_whitpos.shape[0],lat.shape[0],lon.shape[0]))
    ten_wfictpos = np.empty((var_wfictpos.shape[0],lat.shape[0],lon.shape[0]))
    for ens in range(var_wfitpos.shape[0]):
        for i in range(lat.shape[0]):
            for j in range(lon.shape[0]):
                ten_wfitpos[ens,i,j] = np.nanpercentile(var_wfitpos[ens,:,i,j],10)
                ten_whitpos[ens,i,j] = np.nanpercentile(var_whitpos[ens,:,i,j],10)
                ten_wfictpos[ens,i,j] = np.nanpercentile(var_wfictpos[ens,:,i,j],10)
        print('Completed: 10th perc of QBO-W for %s member!' % ens)
                
    ten_wfitneg = np.empty((var_wfitneg.shape[0],lat.shape[0],lon.shape[0]))
    ten_whitneg = np.empty((var_whitneg.shape[0],lat.shape[0],lon.shape[0]))
    ten_wfictneg = np.empty((var_wfictneg.shape[0],lat.shape[0],lon.shape[0]))
    for ens in range(var_wfitneg.shape[0]):
        for i in range(lat.shape[0]):
            for j in range(lon.shape[0]):
                ten_wfitneg[ens,i,j] = np.nanpercentile(var_wfitneg[ens,:,i,j],10)
                ten_whitneg[ens,i,j] = np.nanpercentile(var_whitneg[ens,:,i,j],10)
                ten_wfictneg[ens,i,j] = np.nanpercentile(var_wfictneg[ens,:,i,j],10)
        print('Completed: 10th perc of QBO-E for %s member!' % ens)
        
    ten_wfitnegc = np.empty((var_wfitneg.shape[0],lat.shape[0],lon.shape[0]))
    ten_wfictnegc = np.empty((var_wfictneg.shape[0],lat.shape[0],lon.shape[0]))
    for ens in range(var_wfitneg.shape[0]):
        for i in range(lat.shape[0]):
            for j in range(lon.shape[0]):
                ten_wfitnegc[ens,i,j] = np.nansum(var_wfitneg[ens,:,i,j] < ten_whitneg[ens,i,j])
                ten_wfictnegc[ens,i,j] = np.nansum(var_wfictneg[ens,:,i,j] < ten_whitneg[ens,i,j])
        print('Completed: Day count QBO-E for %s member!' % ens)
        
    ten_wfitposc = np.empty((var_wfitpos.shape[0],lat.shape[0],lon.shape[0]))
    ten_wfictposc = np.empty((var_wfictpos.shape[0],lat.shape[0],lon.shape[0]))
    for ens in range(var_wfitpos.shape[0]):
        for i in range(lat.shape[0]):
            for j in range(lon.shape[0]):
                ten_wfitposc[ens,i,j] = np.nansum(var_wfitpos[ens,:,i,j] < ten_whitpos[ens,i,j])
                ten_wfictposc[ens,i,j] = np.nansum(var_wfictpos[ens,:,i,j] < ten_whitpos[ens,i,j])
        print('Completed: Day count QBO-W for %s member!' % ens)
        
    diffruns = [np.nanmean(ten_wfitposc,axis=0),
                np.nanmean(ten_wfitnegc,axis=0),
                np.nanmean(ten_wfictposc,axis=0),
                np.nanmean(ten_wfictnegc,axis=0)]
    
    ### Calculate significance for DJF
    stat_fithitpos,pvalue_fithitpos = UT.calc_indttest(ten_wfitpos,ten_whitpos)
    stat_fithitneg,pvalue_fithitneg = UT.calc_indttest(ten_wfitneg,ten_whitneg)
    
    stat_ficthitpos,pvalue_ficthitpos = UT.calc_indttest(ten_wfictpos,ten_whitpos)
    stat_ficthitneg,pvalue_ficthitneg = UT.calc_indttest(ten_wfictneg,ten_whitneg)

    pruns = [pvalue_fithitpos,pvalue_fithitneg,pvalue_ficthitpos,pvalue_ficthitneg]
    
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ### Plot variable data for QBO composites
    plt.rc('text',usetex=True)
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
    MASK = True
    
    ### Set limits for contours and colorbars
    if varnames[v] == 'T1000':
        limit = np.arange(0,10,1)
        barlim = np.arange(0,10,3)
        
    fig = plt.figure()
    for i in range(len(diffruns)):
        var = diffruns[i]
        pvar = pruns[i]
        
        if MASK == True:
            pvar2 = pvar.copy()
            pvar2[np.isnan(pvar2)]=np.nan
            var = var*pvar2
        
        ax1 = plt.subplot(2,2,i+1)
        m = Basemap(projection='ortho',lon_0=0,lat_0=89,resolution='l',
                    area_thresh=10000.)
        
        var, lons_cyclic = addcyclic(var, lon)
        var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
        lon2d, lat2d = np.meshgrid(lons_cyclic, lat)
        x, y = m(lon2d, lat2d)
        
        pvar,lons_cyclic = addcyclic(pvar, lon)
        pvar,lons_cyclic = shiftgrid(180.,pvar,lons_cyclic,start=False)
                  
        m.drawmapboundary(fill_color='white',color='dimgray',linewidth=0.7)
        m.fillcontinents(color='dimgrey',zorder=3)
        
        cs = m.contourf(x,y,var,limit,extend='both',zorder=4)
        cs1 = m.contourf(x,y,pvar,colors='None',hatches=['....'],
                         linewidths=0.4,zorder=5)

        m.drawcoastlines(color='dimgray',linewidth=0.8)
        
        if varnames[v] == 'T1000':
            cmap = ncm.cmap('NCV_blu_red')           
            cs.set_cmap(cmocean.cm.thermal)   
            
        m.drawlsmask(land_color=(0,0,0,0),ocean_color='gainsboro',lakes=True,
                     resolution='c',zorder=5)
                    
        ### Add experiment text to subplot
        if i < 2:
            qbophaseq = [r'QBO-W',r'QBO-E']
            ax1.annotate(r'\textbf{%s}' % qbophaseq[i],xy=(0,0),xytext=(0.5,1.08),
                         textcoords='axes fraction',color='dimgray',
                         fontsize=13,rotation=0,ha='center',va='center')
        if i == 0 or i == 2:
            ax1.annotate(r'%s' % experiments[i],xy=(0,0),xytext=(-0.1,0.5),
                         textcoords='axes fraction',color='k',
                         fontsize=20,rotation=90,ha='center',va='center')
                
    ###########################################################################
    cbar_ax = fig.add_axes([0.312,0.1,0.4,0.03])                
    cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                        extend='max',extendfrac=0.07,drawedges=False)
    
    if varnames[v] == 'T1000':
        cbar.set_label(r'\textbf{Days}',fontsize=11,color='dimgray',labelpad=0.2)  

    cbar.set_ticks(barlim)
    cbar.set_ticklabels(list(map(str,barlim)))
    cbar.ax.tick_params(axis='x', size=.01)
    cbar.outline.set_edgecolor('dimgrey')
    
    plt.subplots_adjust(wspace=-0.40)
    plt.subplots_adjust(hspace=0.01)
    plt.subplots_adjust(bottom=0.15)
    
    plt.savefig(directoryfigure + 'ColdExtremes_December.png',
                dpi=300)

print('Completed: Script done!')

