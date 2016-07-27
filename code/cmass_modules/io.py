#import easyaccess as ea
import esutil
import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import numpy.lib.recfunctions as rf
#import seaborn as sns
import fitsio
from fitsio import FITS, FITSHDR



def getDEScatalogs( file = '/n/des/huff.791/Projects/CMASS/Data/DES_Y1_S82.fits', size = 50000, bigSample = False):
    print "don't use for DES cat!!"


    if bigSample is True:
        
        filepath = '/n/des/lee.5922/data/y1a1_coadd/'
        des_files = [filepath+'des_st82_310_330_000001.fits',
                    filepath+'des_st82_310_330_000002.fits',
                    filepath+'des_st82_310_330_000003.fits',
                    filepath+'des_st82_310_330_000004.fits',
                    filepath+'des_st82_310_330_000005.fits',
                    filepath+'des_st82_310_330_000006.fits',
                    filepath+'des_st82_330_335_000001.fits',
                    filepath+'des_st82_330_335_000002.fits',
                    filepath+'des_st82_335_340_000001.fits',
                    filepath+'des_st82_335_340_000002.fits',
                    filepath+'des_st82_340_350_000001.fits',
                    filepath+'des_st82_340_350_000002.fits',
                    filepath+'des_st82_340_350_000003.fits',
                    filepath+'des_st82_340_350_000004.fits',
                    filepath+'des_st82_350_360_000001.fits',
                    filepath+'des_st82_350_360_000002.fits',
                    filepath+'des_st82_350_360_000003.fits',
                    filepath+'des_st82_350_360_000004.fits']
            
    
        """
        if file is False :
            
            #get file from server and save
            connection=ea.connect()
            query=connection.loadsql('../query/stripe82_des_cut.sql')

            #data = connection.query_to_pandas(query)
            data = connection.query_and_save(query,'../data/stripe82_des_cut.fits')
            data = fitsio.read(file)
        
        else:
        """
        data = esutil.io.read(des_files,combine=True)
        #data = fitsio.read(filename, rows=[0,10], ext=2)
        #data,thing = esutil.io.read_header(cfile,ext=1,rows=rows)

    else:
        #if rows is not None:
        
        #sample = np.arange(139142161)
        #rows = np.random.choice( sample, size=size , replace = False)
        #rows = np.arange(500000)
        data = fitsio.read(file, rows=None)
        #data = fitsio.read(file)
    
    data.dtype.names = tuple([ data.dtype.names[i].upper() for i in range(len(data.dtype.names))])
    #data.sort(order = 'COADD_OBJECTS_ID')
    return data



def getSDSScatalogs(  file = '/n/des/huff.791/Projects/CMASS/Data/s82_350_355_emhuff.fit', bigSample = False):
    
    
    if bigSample is True:
        filepath = '/n/des/lee.5922/data/'
        #file = filepath+'sdss_ra330_10.fit'
        
        sdss_files = [filepath+'sdss_ra340_345_dec1_0_sjlee_0.fit',
                      filepath+'sdss_ra340_345_decm1_0_sjlee_0.fit',
                      filepath+'sdss_ra345_350_decm1_0_sjlee_0.fit',
                      filepath+'sdss_ra345_350_dec1_0_sjlee_0.fit',
                      filepath+'sdss_ra355_360_decm1_0_sjlee.fit',
                      filepath+'sdss_ra355_360_dec1_0_sjlee.fit',
                      #filepath +'st82_355_360_SujeongLee_0.fit',
                      '/n/des/huff.791/Projects/CMASS/Data/s82_350_355_emhuff.fit',
                      '/n/des/huff.791/Projects/CMASS/Data/S82_SDSS_0_10.fit'
                      ]
        sdss_data = esutil.io.read(sdss_files,combine=True)
        
        #esutil.io.write('sdss_ra330_10.fit',sdss_data)
        #sdss_data = fitsio.read(file)
    
    else:
    
        #file1 = '/n/des/huff.791/Projects/CMASS/Data/s82_350_355_emhuff.fit'
        #file1 = '/Users/SJ/Dropbox/repositories/CMASS/data/test_emhuff.fit'
        #file3 = '../data/sdss_clean_galaxy_350_360_m05_0.fits'
        #file4 = '../data/sdss_clean_galaxy_350_351_m05_0.fits'
        sdss_data = fitsio.read(file)
        #data = esutil.io.read_header(file1,ext=1)
        
    sdss_data.dtype.names = tuple([ sdss_data.dtype.names[i].upper() for i in range(len(sdss_data.dtype.names))])
    
    return sdss_data


def getDESY1A1catalogs(keyword = 'Y1A1', size = None, sdssmask=True, im3shape=None):
    
    import time
    import os
    
    colortags = ['FLUX_MODEL', 'FLUX_DETMODEL', 'FLUXERR_MODEL', 'FLUXERR_DETMODEL', 'FLAGS', 'MAG_MODEL', 'MAG_DETMODEL', 'MAG_APER_3', 'MAG_APER_4', 'MAG_APER_5','MAG_APER_6', 'XCORR_SFD98', 'MAGERR_DETMODEL', 'MAG_AUTO', 'MAG_PETRO', 'MAG_PSF' ]
    filters = ['G', 'R', 'I', 'Z']
    colortags = [ colortag + '_'+filter for colortag in colortags for filter in filters ]

    sdssmasktags = ['bad_field_mask', 'unphot_mask', 'bright_star_mask', 'rykoff_bright_star_mask','collision_mask', 'centerpost_mask']

    if sdssmask is False : sdssmasktags=[]
    
    tags = ['RA', 'DEC', 'COADD_OBJECTS_ID', 'SPREAD_MODEL_I', 'SPREADERR_MODEL_I' ,'CLASS_STAR_I', 'MAGERR_MODEL_I', 'MAGERR_MODEL_R'] + colortags + sdssmasktags
    path = '/n/des/lee.5922/data/y1a1_coadd/'
    #path = '/n/des/huff.791/Projects/CMASS/Data/Stripe82/' # path for sdss veto masked cat
    tables = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and keyword in i:
            tables.append(path+i)
            print i

    rows = None
    if size is not None:
        sample = np.arange(152160)
        rows = np.random.choice( sample, size=size , replace = False)

    des_data = esutil.io.read( tables, combine=True, columns = tags, rows = rows)
    
    return des_data



def LoadBalrog(user = 'JELENA', truth = None):

    import time
    import os

    colortags = ['FLUX_MODEL', 'FLAGS', 'MAG_MODEL', 'MAG_DETMODEL', 'MAG_APER_3', 'MAG_APER_4', 'MAG_APER_5','MAG_APER_6', 'MAGERR_MODEL', 'MAGERR_DETMODEL']
    filters = ['G', 'R', 'I', 'Z']
    colortags = [ colortag + '_'+filter for colortag in colortags for filter in filters ]

    if truth is True:
        kind = 'TRUTH'
        tags = ['RA', 'DEC', 'ID', 'Z', ]

    elif truth is None:
        kind = 'SIM'
        tags = ['ALPHAWIN_J2000_DET', 'DELTAWIN_J2000_DET', 'SPREAD_MODEL_I', 'SPREADERR_MODEL_I', 'MAG_AUTO_I','CLASS_STAR_I','MAG_PSF_I'] + colortags

    path = '/n/des/lee.5922/data/balrog_cat/'
    tables = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and user.upper() in i and kind in i:
            print i
            tables.append(path+i)

    balrog_data = esutil.io.read( tables, combine=True, columns = tags)
    """
    print "alphaJ2000, deltaJ2000  -->  ra, dec"
    balrogname = list( balrog_data.dtype.names)
    alphaInd = balrogname.index('ALPHAWIN_J2000_DET')
    deltaInd = balrogname.index('DELTAWIN_J2000_DET')
    balrogname[alphaInd], balrogname[deltaInd] = 'RA', 'DEC'
    balrog_data.dtype.names = tuple(balrogname)
    """
    return balrog_data

