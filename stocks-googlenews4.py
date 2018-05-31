# coding: utf-8
######################################################
####################################################
######### Imports #####################

import requests
import bs4
from bs4 import BeautifulSoup
import warnings
import time
import datetime
import json
import pandas as pd
import io
import re
import psycopg2
import quandl
from mmduprem import mmduprem

warnings.filterwarnings('ignore')

###########################################################
##########################################################
######## Used QUANDL Functions #########################

quandl.ApiConfig.api_key = 'omQiMysF2NQ1B-xZEJBk'

def quandl_stocks(symbol, start_date=(2010, 1, 1), end_date=None):
    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(11, 12)]
    start_date = datetime.date(*start_date)
    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()
    return quandl.get(query_list,
            returns='pandas',
            start_date=start_date,
            end_date=end_date,
            collapse='daily',
            order='asc'
            )

def quandl_adj_close(ticker):
	if len(ticker)<5:
		data=pd.DataFrame(quandl_stocks(ticker))
		#data=data[len(data)-1:]
		data=data.tail(1)
		data=str(data.max()).split(' ')[7:8]
		data=re.split(r'[`\-=;\'\\/<>?]', str(data))
		data=data[1]
		try:
			data=float(data)
		except:
			data=int(0)
		price=int(round(data,0))
		if price>1:
			return price


###########################################################################
#########Main Barchart Function (ticker puller###############################

def barchart(ticker):
    with requests.Session() as c:
        u='https://www.barchart.com/stocks/quotes/'+ticker
        x=c.get(u)
        x=BeautifulSoup(x.content, "html.parser")
        titles=x.find_all()
        titles=str(titles)
        s=titles[titles.find("dailyLastPrice")+17:titles.find("dailyLastPrice")+17+20].replace('"','').split(",")
        if quandl_adj_close(ticker)>1000:
            s=float(s[0]+s[1])
        else:
            s=float(s[0])
        return s


########################################################################################
##########################################################################################
###############            YAHOO PE and EPS pullers    ##################################
##########################################################################################

def yahoopepuller(ticker):
	with requests.Session() as c:
		u="http://finance.yahoo.com/quote/"+ticker+"?p=" + ticker
		x=c.get(u)
		x=BeautifulSoup(x.content)
		titles=x.find_all()
		titles=str(titles)
		s=titles.find("PE_RATIO-value")
		pe=titles[s:s+1000]
		sn=pe.find("react-text")
		pe=pe[sn+17:sn+24]
		pe=pe.replace(">","").replace("!","").replace("<","")
		try:
			pe=float(pe)
		except:
			pe=0
		return pe

def yahooepspuller(ticker):
	with requests.Session() as c:
		u="http://finance.yahoo.com/quote/"+ticker+"?p=" + ticker
		x=c.get(u)
		x=BeautifulSoup(x.content)
		titles=x.find_all()
		titles=str(titles)
		s=titles.find("EPS_RATIO-value")
		pe=titles[s:s+1000]
		sn=pe.find("reactid")
		pe=pe[sn+13:sn+18]
		pe=pe.replace(">","").replace("!","").replace("<","").replace("/","").replace('"',"")
		try:
			pe=float(pe)
		except:
			pe=0
		return pe

 ############################################################################################
 ############################################################################################
 ############################################################################################
 #############                                                ###############################
 #############                Accenture URLS                    #############################
 #############                                                ###############################
 ############################################################################################
 ############################################################################################
 ############################################################################################
 ############################################################################################
 ############################################################################################
 ############################################################################################
 ############################################################################################
 #############                                                ###############################
 #############                Stock List                       ##############################
 #############                                                ###############################
 ############################################################################################
 ############################################################################################
 ############################################################################################
 ############################################################################################

stocklist=[
##################
###   SnP500    ###
###################

'MMM','AOS','ABT','ABBV','ACN','ATVI','AYI','ADBE','AAP','AMD','AES','AET','AMG','AFL','A','APD','AKAM','ALK','ALB','ARE','ALXN','ALGN','ALLE','AGN','ADS','LNT','ALL','GOOGL','GOOG','MO','AMZN','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','APC','ADI','ANDV','ANSS','ANTM','AON','APA','AIV','AAPL','AMAT','APTV','ADM','ARNC','AJG','AIZ','T','ADSK','ADP','AZO','AVB','AVY','BHGE','BLL','BAC','BAX','BBT','BDX','BRK.B','BBY','BIIB','BLK','HRB','BA','BKNG','BWA','BXP','BSX','BHF','BMY','AVGO','BF.B','CHRW','CA','COG','CDNS','CPB','COF','CAH','KMX','CCL','CAT','CBOE','CBRE','CBS','CELG','CNC','CNP','CTL','CERN','CF','SCHW','CHTR','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','CXO','COP','ED','STZ','GLW','COST','COTY','CCI','CSRA','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','DLR','DFS','DISCA','DISCK','DISH','DG','DLTR','D','DOV','DWDP','DPS','DTE','DUK','DRE','DXC','ETFC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ETR','EVHC','EOG','EQT','EFX','EQIX','EQR','ESS','EL','RE','ES','EXC','EXPE','EXPD','ESRX','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FE','FISV','FLIR','FLS','FLR','FMC','FL','F','FTV','FBHS','BEN','FCX','GPS','GRMN','IT','GD','GE','GGP','GIS','GM','GPC','GILD','GPN','GS','GT','GWW','HAL','HBI','HOG','HRS','HIG','HAS','HCA','HCP','HP','HSIC','HES','HPE','HLT','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','HII','IDXX','INFO','ITW','ILMN','INCY','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JBHT','JEC','SJM','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LLL','LH','LRCX','LEG','LEN','LUK','LLY','LNC','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MRO','MPC','MAR','MMC','MLM','MAS','MA','MAT','MKC','MCD','MCK','MDT','MRK','MET','MTD','MGM','KORS','MCHP','MU','MSFT','MAA','MHK','TAP','MDLZ','MON','MNST','MCO','MS','MSI','MYL','NDAQ','NOV','NAVI','NKTR','NTAP','NFLX','NWL','NFX','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS','NOC','NCLH','NRG','NUE','NVDA','ORLY','OXY','OMC','OKE','ORCL','PCAR','PKG','PH','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE','PCG','PM','PSX','PNW','PXD','PNC','RL','PPG','PPL','PX','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO','QCOM','PWR','DGX','RRC','RJF','RTN','O','RHT','REG','REGN','RF','RSG','RMD','RHI','ROK','COL','ROP','ROST','RCL','SPGI','CRM','SBAC','SCG','SLB','STX','SEE','SRE','SHW','SPG','SWKS','SLG','SNA','SO','LUV','SWK','SBUX','STT','SRCL','SYK','STI','SIVB','SYMC','SYF','SNPS','SYY','TROW','TTWO','TPR','TGT','TEL','FTI','TXN','TXT','BK','CLX','COO','HSY','MOS','TRV','DIS','TMO','TIF','TWX','TJX','TMK','TSS','TSCO','TDG','TRIP','FOXA','FOX','TSN','USB','UDR','ULTA','UAA','UA','UNP','UAL','UNH','UPS','URI','UTX','UHS','UNM','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WMT','WBA','WM','WAT','WEC','WFC','WELL','WDC','WU','WRK','WY','WHR','WMB','WLTW','WYN','WYNN','XEL','XRX','XLNX','XL','XYL','YUM','ZBH','ZION','ZTS','MHLD','ORIT','ALGT','ELY','NTRI','PETS','NVDA','TSLA'

##################
###   NASDAQ   ###
###################
,'AAL','AAPL','ADBE','ADI','ADP','ADSK','AKAM','ALGN','ALXN','AMAT','AMGN','AMZN','ATVI','AVGO','BIDU','BIIB','BMRN','CA','CELG','CERN','CHKP','CHTR','CTRP','CTAS','CSCO','CTXS','CMCSA','COST','CSX','CTSH','DISCA','DISCK','DISH','DLTR','EA','EBAY','ESRX','EXPE','FAST','FB','FISV','FOX','FOXA','GILD','GOOG','GOOGL','HAS','HSIC','HOLX','ILMN','INCY','INTC','INTU','ISRG','JBHT','JD','KLAC','KHC','LBTYK','LILA','LBTYA','QRTEA','MELI','MAR','MAT','MDLZ','MNST','MSFT','MU','MXIM','MYL','NCLH','NFLX','NTES','NVDA','PAYX','BKNG','PYPL','QCOM','REGN','ROST','SHPG','SIRI','SWKS','SBUX','SYMC','TSCO','TXN','TMUS','ULTA','VIAB','VOD','VRTX','WBA','WDC','XRAY','IDXX','LILAK','LRCX','MCHP','ORLY','PCAR','STX','TSLA','VRSK','WYNN','XLNX'

########################
###   Russell 3000  #####
###########################

,'AA','AAL','AAMC','AAN','AAOI','AAON','AAP','AAPL','AAT','AAWW','ABAX','ABBV','ABC','ABCB','ABCO','ABG','ABM','ABMD','ABT','ACAD','ACAT','ACC','ACCO','ACE','ACET','ACGL','ACHC','ACHN','ACI','ACIW','ACLS','ACM','ACN','ACOR','ACRE','ACRX','ACT','ACTG','ACW','ACXM','ADBE','ADC','ADES','ADI','ADM','ADMS','ADNC','ADP','ADS','ADSK','ADT','ADTN','ADUS','ADVS','AE','AEC','AEE','AEGN','AEGR','AEIS','AEL','AEO','AEP','AEPI','AERI','AES','AET','AF','AFAM','AFFX','AFG','AFH','AFL','AFOP','AFSI','AGCO','AGEN','AGII','AGIO','AGM','AGN','AGNC','AGO','AGTC','AGX','AGYS','AHC','AHH','AHL','AHP','AHS','AHT','AI','AIG','AIMC','AIN','AIQ','AIR','AIRM','AIT','AIV','AIZ','AJG','AKAM','AKAO','AKBA','AKR','AKRX','AKS','AL','ALB','ALCO','ALDR','ALE','ALEX','ALG','ALGN','ALGT','ALIM','ALJ','ALK','ALKS','ALL','ALLE','ALLY','ALNY','ALOG','ALR','ALSN','ALTR','ALX','ALXN','AMAG','AMAT','AMBA','AMBC','AMBR','AMC','AMCC','AMCX','AMD','AME','AMED','AMG','AMGN','AMH','AMKR','AMNB','AMP','AMPE','AMRC','AMRE','AMRI','AMRS','AMSF','AMSG','AMSWA','AMT','AMTD','AMTG','AMWD','AMZG','AMZN','AN','ANAC','ANAT','ANDE','ANF','ANGI','ANGO','ANH','ANIK','ANIP','ANN','ANR','ANSS','ANV','AOI','AOL','AON','AOS','AOSL','AP','APA','APAGF','APAM','APC','APD','APEI','APH','APOG','APOL','AR','ARAY','ARC','ARCB','ARCP','ARCW','ARE','AREX','ARG','ARI','ARIA','ARII','ARMK','ARNA','ARO','AROW','ARPI','ARR','ARRS','ARRY','ARTNA','ARUN','ARW','ARWR','ARX','ASBC','ASC','ASCMA','ASEI','ASGN','ASH','ASNA','ASPS','ASPX','ASTE','AT','ATEN','ATHL','ATHN','ATI','ATK','ATLO','ATML','ATNI','ATNM','ATO','ATR','ATRC','ATRI','ATRO','ATRS','ATSG','ATU','ATVI','ATW','AUXL','AVA','AVAV','AVB','AVD','AVG','AVGO','AVHI','AVIV','AVNR','AVP','AVT','AVX','AVY','AWAY','AWH','AWI','AWK','AWR','AXAS','AXDX','AXE','AXL','AXLL','AXP','AXS','AYI','AYR','AZO','AZPN','AZZ','B','BA','BABY','BAC','BAGL','BAH','BALT','BANC','BANF','BANR','BAS','BAX','BBBY','BBCN','BBG','BBNK','BBOX','BBRG','BBSI','BBT','BBW','BBX','BBY','BC','BCC','BCEI','BCO','BCOR','BCOV','BCPC','BCR','BCRX','BDBD','BDC','BDE','BDGE','BDN','BDSI','BDX','BEAT','BEAV','BEBE','BECN','BEE','BELFB','BEN','BERY','BF.B','BFAM','BFIN','BFS','BG','BGC','BGCP','BGFV','BGG','BGS','BH','BHE','BHI','BHLB','BID','BIG','BIIB','BIO','BIOS','BIRT','BJRI','BK','BKD','BKE','BKH','BKMU','BKS','BKU','BKW','BKYF','BLDR','BLK','BLKB','BLL','BLMN','BLOX','BLT','BLUE','BLX','BMI','BMR','BMRC','BMRN','BMS','BMTC','BMY','BNCL','BNCN','BNFT','BNNY','BOBE','BOFI','BOH','BOKF','BONT','BOOM','BPFH','BPI','BPOP','BPTH','BPZ','BR','BRC','BRCD','BRCM','BRDR','BREW','BRK.B','BRKL','BRKR','BRKS','BRLI','BRO','BRS','BRSS','BRX','BSFT','BSRR','BSTC','BSX','BTU','BTX','BURL','BUSE','BV','BWA','BWC','BWINB','BWLD','BWS','BXP','BXS','BYD','BYI','BZH','C','CA','CAB','CAC','CACB','CACC','CACI','CACQ','CAG','CAH','CAKE','CALD','CALL','CALM','CALX','CAM','CAMP','CAP','CAR','CARA','CARB','CAS','CASH','CASS','CASY','CAT','CATM','CATO','CATY','CAVM','CB','CBB','CBEY','CBF','CBG','CBI','CBK','CBL','CBM','CBOE','CBPX','CBR','CBRL','CBS','CBSH','CBSO','CBST','CBT','CBU','CBZ','CCBG','CCC','CCE','CCF','CCG','CCI','CCK','CCL','CCMP','CCNE','CCO','CCOI','CCRN','CCXI','CDE','CDI','CDNS','CDR','CDW','CE','CEB','CECE','CECO','CELG','CEMP','CENTA','CENX','CERN','CERS','CETV','CEVA','CF','CFFN','CFI','CFN','CFNL','CFR','CFX','CGI','CGNX','CHCO','CHD','CHDN','CHDX','CHE','CHEF','CHFC','CHFN','CHGG','CHH','CHK','CHMT','CHRW','CHS','CHSP','CHTR','CHUY','CI','CIA','CIDM','CIE','CIEN','CIFC','CIM','CINF','CIR','CIT','CJES','CKEC','CKH','CKP','CL','CLC','CLCT','CLD','CLDT','CLDX','CLF','CLFD','CLGX','CLH','CLI','CLMS','CLNE','CLNY','CLR','CLVS','CLW','CLX','CMA','CMC','CMCO','CMCSA','CME','CMG','CMI','CMLS','CMN','CMO','CMP','CMRX','CMS','CMTL','CNA','CNBC','CNBKA','CNC','CNK','CNL','CNMD','CNO','CNOB','CNP','CNQR','CNS','CNSI','CNSL','CNVR','CNW','CNX','COB','COBZ','CODE','COF','COG','COH','COHR','COHU','COKE','COL','COLB','COLM','COMM','CONE','CONN','COO','COP','COR','CORE','CORR','CORT','COST','COTY','COUP','COV','COVS','COWN','CPA','CPB','CPE','CPF','CPHD','CPK','CPLA','CPN','CPRT','CPS','CPSI','CPSS','CPST','CPT','CPWR','CQB','CR','CRAI','CRAY','CRCM','CRD.B','CREE','CRI','CRK','CRL','CRM','CRMT','CROX','CRR','CRRS','CRS','CRUS','CRVL','CRWN','CRY','CRZO','CSBK','CSC','CSCD','CSCO','CSFL','CSG','CSGP','CSGS','CSH','CSII','CSL','CSLT','CSOD','CSS','CST','CSU','CSV','CSX','CTAS','CTB','CTBI','CTCT','CTG','CTIC','CTL','CTO','CTRE','CTRL','CTRN','CTRX','CTS','CTSH','CTT','CTWS','CTXS','CUB','CUBE','CUBI','CUDA','CUI','CUNB','CUR','CUZ','CVA','CVBF','CVC','CVCO','CVD','CVEO','CVG','CVGI','CVGW','CVI','CVLT','CVO','CVS','CVT','CVX','CW','CWEI','CWH','CWST','CWT','CXO','CXP','CXW','CY','CYBX','CYH','CYN','CYNI','CYNO','CYS','CYT','CYTK','CYTR','CYTX','CZNC','CZR','D','DAKT','DAL','DAN','DAR','DATA','DAVE','DBD','DCI','DCO','DCOM','DCT','DD','DDD','DDR','DDS','DE','DECK','DEI','DEL','DENN','DEPO','DEST','DF','DFRG','DFS','DFT','DFZ','DG','DGI','DGICA','DGII','DGX','DHI','DHIL','DHR','DHT','DHX','DIN','DIOD','DIS','DISCA','DISH','DJCO','DK','DKS','DLB','DLR','DLTR','DLX','DMD','DMND','DMRC','DNB','DNDN','DNKN','DNOW','DNR','DO','DOC','DOOR','DORM','DOV','DOW','DOX','DPS','DPZ','DRC','DRE','DRH','DRI','DRII','DRIV','DRNA','DRQ','DRTX','DSCI','DSPG','DST','DSW','DTE','DTLK','DTSI','DTV','DUK','DV','DVA','DVAX','DVN','DW','DWA','DWRE','DWSN','DX','DXCM','DXLG','DXM','DXPE','DXYN','DY','DYAX','DYN','EA','EAC','EAT','EBAY','EBF','EBIO','EBIX','EBS','EBSB','EBTC','ECHO','ECL','ECOL','ECOM','ECPG','ECYT','ED','EDE','EDMC','EDR','EE','EEFT','EFII','EFSC','EFX','EGBN','EGHT','EGL','EGLT','EGN','EGOV','EGP','EGY','EHTH','EIG','EIGI','EIX','EL','ELGX','ELLI','ELNK','ELRC','ELS','ELX','ELY','EMC','EMCI','EME','EMN','EMR','ENDP','ENH','ENOC','ENPH','ENR','ENS','ENSG','ENT','ENTA','ENTG','ENTR','ENV','ENVE','ENZ','EOG','EOPN','EOX','EPAM','EPAY','EPE','EPIQ','EPM','EPR','EPZM','EQIX','EQR','EQT','EQU','EQY','ERA','ERIE','ERII','EROS','ESBF','ESC','ESCA','ESE','ESGR','ESI','ESIO','ESL','ESNT','ESPR','ESRT','ESRX','ESS','ETFC','ETH','ETM','ETN','ETR','EV','EVC','EVDY','EVER','EVHC','EVR','EVTC','EW','EWBC','EXAC','EXAM','EXAR','EXAS','EXC','EXEL','EXH','EXL','EXLS','EXP','EXPD','EXPE','EXPO','EXPR','EXR','EXTR','EXXI','EZPW','F','FAF','FANG','FARM','FARO','FAST','FB','FBC','FBHS','FBIZ','FBNC','FBNK','FBP','FBRC','FC','FCBC','FCE.A','FCEL','FCF','FCFS','FCH','FCN','FCNCA','FCS','FCX','FDEF','FDML','FDO','FDP','FDS','FDX','FE','FEIC','FELE','FET','FEYE','FF','FFBC','FFG','FFIC','FFIN','FFIV','FFNW','FGL','FHCO','FHN','FI','FIBK','FICO','FII','FINL','FIO','FIS','FISI','FISV','FITB','FIVE','FIVN','FIX','FIZZ','FL','FLDM','FLIC','FLIR','FLO','FLR','FLS','FLT','FLTX','FLWS','FLXN','FLXS','FMBI','FMC','FMER','FMI','FN','FNB','FNF','FNFG','FNGN','FNHC','FNLC','FNSR','FOE','FOR','FORM','FORR','FOSL','FOXA','FOXF','FPO','FPRX','FR','FRAN','FRBK','FRC','FRED','FRGI','FRM','FRME','FRNK','FRO','FRP','FRSH','FRT','FRX','FSL','FSLR','FSP','FSS','FST','FSTR','FSYS','FTD','FTI','FTK','FTNT','FTR','FUBC','FUEL','FUL','FULT','FUR','FURX','FVE','FWLT','FWM','FWRD','FXCB','FXCM','FXEN','G','GABC','GAIA','GALE','GALT','GAS','GB','GBCI','GBL','GBLI','GBNK','GBX','GCA','GCAP','GCI','GCO','GD','GDOT','GDP','GE','GEF','GEO','GEOS','GERN','GES','GEVA','GFF','GFIG','GFN','GGG','GGP','GHC','GHDX','GHL','GHM','GIFI','GIII','GILD','GIMO','GIS','GK','GLDD','GLF','GLNG','GLOG','GLPI','GLPW','GLRE','GLRI','GLT','GLUU','GLW','GM','GMCR','GME','GMED','GMT','GNC','GNCA','GNCMA','GNMK','GNRC','GNTX','GNW','GOGO','GOOD','GOOG','GOOGL','GORO','GOV','GPC','GPI','GPK','GPN','GPOR','GPRE','GPS','GPT','GPX','GRA','GRC','GRMN','GRPN','GRT','GRUB','GS','GSAT','GSBC','GSIG','GSM','GSOL','GST','GT','GTAT','GTI','GTIV','GTLS','GTN','GTS','GTT','GTY','GUID','GVA','GWR','GWRE','GWW','GXP','GY','H','HA','HAE','HAFC','HAIN','HAL','HALL','HALO','HAR','HAS','HASI','HAWK','HAYN','HBAN','HBHC','HBI','HBNC','HCA','HCBK','HCC','HCCI','HCI','HCKT','HCN','HCOM','HCP','HCSG','HCT','HD','HDS','HE','HEAR','HEES','HEI','HELE','HELI','HEOP','HERO','HES','HF','HFC','HFWA','HGG','HGR','HHC','HHS','HI','HIBB','HIG','HII','HIL','HILL','HITT','HIVE','HIW','HK','HL','HLF','HLIT','HLS','HLSS','HLT','HLX','HME','HMHC','HMN','HMPR','HMST','HMSY','HMTV','HNH','HNI','HNR','HNRG','HNT','HOG','HOLX','HOMB','HON','HOS','HOT','HOV','HP','HPP','HPQ','HPT','HPTX','HPY','HR','HRB','HRC','HRG','HRL','HRS','HRTG','HRTX','HSC','HSH','HSIC','HSII','HSNI','HSP','HST','HSTM','HSY','HT','HTA','HTBI','HTBK','HTH','HTLD','HTLF','HTS','HTWR','HTZ','HUB.B','HUBG','HUM','HUN','HURC','HURN','HVB','HVT','HW','HWAY','HWCC','HWKN','HXL','HY','HZNP','HZO','I','IACI','IART','IBCP','IBKC','IBKR','IBM','IBOC','IBP','IBTX','ICE','ICEL','ICFI','ICGE','ICON','ICPT','ICUI','IDA','IDCC','IDIX','IDRA','IDT','IDTI','IDXX','IEX','IFF','IG','IGT','IGTE','IHC','IHS','III','IIIN','IILG','IIVI','IL','ILMN','IM','IMGN','IMKTA','IMMR','IMMU','IMPV','IMS','INAP','INCY','INDB','INFA','INFI','INFN','INGN','INGR','ININ','INN','INO','INSM','INSY','INT','INTC','INTL','INTU','INVN','INWK','IO','IOSP','IP','IPAR','IPCC','IPCM','IPG','IPGP','IPHI','IPHS','IPI','IPXL','IQNT','IR','IRBT','IRC','IRDM','IRET','IRF','IRG','IRM','IRWD','ISBC','ISCA','ISH','ISIL','ISIS','ISLE','ISRG','ISRL','ISSI','IT','ITC','ITCI','ITG','ITMN','ITRI','ITT','ITW','IVAC','IVC','IVR','IVZ','IXYS','JACK','JAH','JAKK','JAZZ','JBHT','JBL','JBLU','JBSS','JBT','JCI','JCOM','JCP','JDSU','JEC','JGW','JIVE','JJSF','JKHY','JLL','JMBA','JNJ','JNPR','JNS','JOE','JONE','JOUT','JOY','JPM','JRN','JW.A','JWN','K','KAI','KALU','KAMN','KAR','KATE','KBALB','KBH','KBR','KCG','KCLI','KEG','KELYA','KEM','KERX','KEX','KEY','KEYW','KFRC','KFX','KFY','KIM','KIN','KIRK','KKD','KLAC','KMB','KMG','KMI','KMPR','KMT','KMX','KN','KND','KNL','KNX','KO','KODK','KOG','KOP','KOPN','KORS','KOS','KPTI','KR','KRA','KRC','KRFT','KRG','KRNY','KRO','KS','KSS','KSU','KTOS','KTWO','KVHI','KW','KWK','KWR','KYTH','L','LABL','LAD','LADR','LAMR','LANC','LAYN','LAZ','LB','LBAI','LBMH','LBY','LCI','LCUT','LDL','LDOS','LDR','LDRH','LE','LEA','LEAF','LECO','LEE','LEG','LEN','LF','LFUS','LG','LGF','LGIH','LGND','LH','LHCG','LHO','LII','LINTA','LION','LIOX','LKFN','LKQ','LL','LLL','LLNW','LLTC','LLY','LM','LMCA','LMIA','LMNR','LMNX','LMOS','LMT','LNC','LNCE','LNDC','LNG','LNKD','LNN','LNT','LO','LOCK','LOGM','LOPE','LORL','LOW','LPG','LPI','LPLA','LPNT','LPSN','LPT','LPX','LQ','LQDT','LRCX','LRN','LSCC','LSTR','LTC','LTM','LTS','LUK','LUV','LVLT','LVNTA','LVS','LWAY','LXFT','LXK','LXP','LXRX','LXU','LYB','LYTS','LYV','LZB','M','MA','MAA','MAC','MACK','MAN','MANH','MANT','MAR','MAS','MASI','MAT','MATW','MATX','MBFI','MBI','MBII','MBUU','MBVT','MBWM','MC','MCBC','MCD','MCF','MCHP','MCHX','MCK','MCO','MCP','MCRI','MCRL','MCRS','MCS','MCY','MD','MDAS','MDC','MDCA','MDCO','MDLZ','MDP','MDR','MDRX','MDSO','MDT','MDU','MDVN','MDXG','MEAS','MED','MEG','MEI','MENT','MET','METR','MFA','MFLX','MFRM','MG','MGAM','MGEE','MGI','MGLN','MGM','MGNX','MGRC','MHFI','MHGC','MHK','MHLD','MHO','MHR','MIDD','MIG','MILL','MIND','MINI','MITT','MJN','MKC','MKL','MKSI','MKTO','MKTX','MLAB','MLHR','MLI','MLM','MLNK','MLR','MM','MMC','MMI','MMM','MMS','MMSI','MN','MNI','MNK','MNKD','MNR','MNRO','MNST','MNTA','MNTX','MO','MOD','MODN','MOFG','MOG.A','MOH','MON','MORN','MOS','MOV','MOVE','MPAA','MPC','MPO','MPW','MPWR','MPX','MRC','MRCY','MRGE','MRH','MRIN','MRK','MRLN','MRO','MRTN','MRTX','MRVL','MS','MSA','MSCC','MSCI','MSEX','MSFG','MSFT','MSG','MSI','MSL','MSM','MSO','MSTR','MTB','MTD','MTDR','MTG','MTGE','MTH','MTN','MTOR','MTRN','MTRX','MTSC','MTSI','MTW','MTX','MTZ','MU','MUR','MUSA','MVNR','MW','MWA','MWIV','MWV','MWW','MXIM','MXL','MXWL','MYCC','MYE','MYGN','MYL','MYRG','N','NADL','NANO','NASB','NAT','NATH','NATI','NATL','NATR','NAV','NAVB','NAVG','NAVI','NBBC','NBCB','NBHC','NBIX','NBL','NBR','NBS','NBTB','NC','NCFT','NCI','NCLH','NCMI','NCR','NCS','NDAQ','NDLS','NDSN','NEE','NEM','NEOG','NES','NEU','NEWM','NEWP','NEWS','NFBK','NFG','NFLX','NFX','NGHC','NGS','NGVC','NHC','NHI','NI','NICK','NILE','NJR','NKE','NKSH','NKTR','NL','NLNK','NLS','NLSN','NLY','NM','NMBL','NMIH','NMRX','NNA','NNBR','NNI','NNN','NNVC','NOC','NOG','NOR','NOV','NOW','NP','NPBC','NPK','NPO','NPSP','NR','NRCIA','NRF','NRG','NRIM','NRZ','NSC','NSIT','NSM','NSP','NSR','NSTG','NTAP','NTCT','NTGR','NTK','NTLS','NTRI','NTRS','NU','NUAN','NUE','NUS','NUTR','NUVA','NVAX','NVDA','NVEC','NVR','NWBI','NWBO','NWE','NWHM','NWL','NWLI','NWN','NWPX','NWSA','NWY','NX','NXST','NXTM','NYCB','NYLD','NYMT','NYNY','NYRT','NYT','O','OABC','OAS','OB','OC','OCFC','OCLR','OCN','OCR','ODC','ODFL','ODP','OEH','OFC','OFG','OFIX','OFLX','OGE','OGS','OHI','OHRP','OI','OII','OIS','OKE','OKSB','OLBK','OLED','OLN','OLP','OMC','OMCL','OME','OMED','OMER','OMG','OMI','OMN','ONB','ONE','ONNN','ONTY','ONVO','OPB','OPEN','OPHT','OPK','OPLK','OPWR','OPY','ORA','ORB','ORBC','ORCL','OREX','ORI','ORIT','ORLY','ORM','ORN','OSIR','OSIS','OSK','OSTK','OSUR','OTTR','OUTR','OVAS','OVTI','OWW','OXFD','OXM','OXY','OZRK','P','PACB','PACW','PAG','PAH','PAHC','PANW','PATK','PATR','PAY','PAYC','PAYX','PB','PBCT','PBF','PBH','PBI','PBPB','PBY','PBYI','PCAR','PCBK','PCCC','PCG','PCH','PCL','PCLN','PCO','PCP','PCRX','PCTY','PCYC','PCYG','PDCE','PDCO','PDFS','PDLI','PDM','PE','PEB','PEBO','PEG','PEGA','PEGI','PEI','PEIX','PENN','PEP','PERY','PES','PETM','PETS','PETX','PF','PFBC','PFE','PFG','PFIE','PFIS','PFMT','PFPT','PFS','PFSI','PG','PGC','PGEM','PGI','PGNX','PGR','PGTI','PH','PHH','PHIIK','PHM','PHMD','PHX','PICO','PII','PIKE','PINC','PIR','PJC','PKD','PKE','PKG','PKI','PKOH','PKT','PKY','PL','PLAB','PLCE','PLCM','PLD','PLKI','PLL','PLMT','PLOW','PLPC','PLT','PLUG','PLUS','PLXS','PLXT','PM','PMC','PMCS','PMT','PNC','PNFP','PNK','PNM','PNR','PNRA','PNW','PNX','PNY','PODD','POL','POM','POOL','POR','POST','POWI','POWL','POWR','POZN','PPBI','PPC','PPG','PPHM','PPL','PPO','PPS','PQ','PRA','PRAA','PRE','PRFT','PRGO','PRGS','PRGX','PRI','PRIM','PRK','PRKR','PRLB','PRO','PRSC','PRTA','PRU','PRXL','PSA','PSB','PSEM','PSIX','PSMI','PSMT','PSTB','PSUN','PSX','PTC','PTCT','PTEN','PTIE','PTLA','PTP','PTRY','PTSI','PTX','PVA','PVH','PVTB','PWOD','PWR','PX','PXD','PZN','PZZA','Q','QADA','QCOM','QCOR','QDEL','QEP','QGEN','QLGC','QLIK','QLTY','QLYS','QNST','QRHC','QSII','QTM','QTS','QTWO','QUAD','QUIK','R','RAD','RAI','RAIL','RALY','RARE','RAS','RATE','RAVN','RAX','RBC','RBCAA','RBCN','RCAP','RCII','RCL','RCPT','RDC','RDEN','RDI','RDN','RDNT','RE','RECN','REG','REGI','REGN','REI','REIS','REMY','REN','RENT','RES','RESI','REV','REX','REXI','REXR','REXX','RF','RFMD','RFP','RGA','RGC','RGDO','RGEN','RGLD','RGLS','RGR','RGS','RH','RHI','RHP','RHT','RICE','RIGL','RJET','RJF','RKT','RKUS','RL','RLD','RLGY','RLI','RLJ','RLOC','RLYP','RM','RMAX','RMBS','RMD','RMTI','RNDY','RNET','RNG','RNR','RNST','RNWK','ROC','ROCK','ROG','ROIAK','ROIC','ROK','ROL','ROLL','ROP','ROSE','ROST','ROVI','RP','RPAI','RPM','RPRX','RPT','RPTP','RPXC','RRC','RRD','RRGB','RRTS','RS','RSE','RSG','RSO','RSPP','RST','RSTI','RT','RTEC','RTI','RTIX','RTK','RTN','RTRX','RUBI','RUSHA','RUTH','RVBD','RVLT','RVNC','RWT','RXN','RYL','RYN','S','SAAS','SABR','SAFM','SAFT','SAH','SAIA','SAIC','SALE','SALM','SALT','SAM','SAMG','SANM','SAPE','SASR','SATS','SAVE','SB','SBAC','SBCF','SBGI','SBH','SBNY','SBRA','SBSI','SBUX','SBY','SC','SCAI','SCBT','SCCO','SCG','SCHL','SCHN','SCHW','SCI','SCL','SCLN','SCMP','SCOR','SCS','SCSC','SCSS','SCTY','SCVL','SD','SDRL','SE','SEAC','SEAS','SEB','SEE','SEIC','SEM','SEMG','SENEA','SF','SFBS','SFE','SFG','SFL','SFLY','SFM','SFNC','SFXE','SFY','SGA','SGBK','SGEN','SGI','SGK','SGM','SGMO','SGMS','SGNT','SGY','SGYP','SHEN','SHLD','SHLM','SHLO','SHO','SHOO','SHOR','SHOS','SHW','SIAL','SIF','SIG','SIGI','SIMG','SIR','SIRI','SIRO','SIVB','SIX','SJI','SJM','SJW','SKH','SKT','SKUL','SKX','SKYW','SLAB','SLB','SLCA','SLG','SLGN','SLH','SLM','SLXP','SM','SMA','SMCI','SMG','SMP','SMRT','SMTC','SN','SNA','SNAK','SNBC','SNCR','SNDK','SNH','SNHY','SNI','SNMX','SNOW','SNPS','SNSS','SNTA','SNV','SNX','SO','SON','SONC','SONS','SP','SPA','SPAR','SPB','SPDC','SPF','SPG','SPLK','SPLS','SPN','SPNC','SPNS','SPPI','SPR','SPSC','SPTN','SPW','SPWH','SPWR','SQBG','SQBK','SQI','SQNM','SRC','SRCE','SRCL','SRDX','SRE','SREV','SRI','SRPT','SSD','SSI','SSNC','SSNI','SSP','SSS','SSTK','SSYS','STAA','STAG','STAR','STBA','STBZ','STC','STCK','STE','STFC','STI','STJ','STL','STLD','STML','STMP','STNG','STNR','STR','STRA','STRL','STRT','STRZA','STT','STWD','STZ','SUBK','SUI','SUNE','SUP','SUPN','SUSQ','SUSS','SVU','SWAY','SWC','SWFT','SWHC','SWI','SWK','SWKS','SWM','SWN','SWS','SWX','SWY','SXC','SXI','SXT','SYA','SYBT','SYK','SYKE','SYMC','SYNA','SYNT','SYRG','SYUT','SYX','SYY','SZMK','SZYM','T','TAHO','TAL','TAM','TAP','TASR','TAST','TAT','TAX','TAYC','TBBK','TBI','TBNK','TBPH','TCB','TCBI','TCBK','TCO','TCS','TDC','TDG','TDS','TDW','TDY','TE','TECD','TECH','TEG','TEN','TER','TESO','TESS','TEX','TFM','TFSL','TFX','TG','TGH','TGI','TGT','TGTX','THC','THFF','THG','THLD','THO','THOR','THR','THRM','THRX','THS','TIBX','TIF','TILE','TIME','TIPT','TIS','TISI','TITN','TIVO','TJX','TK','TKR','TLMR','TLYS','TMH','TMHC','TMK','TMO','TMP','TMUS','TNAV','TNC','TNDM','TNET','TNGO','TNK','TOL','TOWN','TOWR','TPC','TPH','TPLM','TPRE','TPX','TQNT','TR','TRAK','TRC','TREC','TREE','TREX','TRGP','TRI','TRIP','TRIV','TRK','TRLA','TRMB','TRMK','TRMR','TRN','TRNO','TRNX','TROW','TROX','TRS','TRST','TRUE','TRV','TRW','TRXC','TSC','TSCO','TSLA','TSN','TSO','TSRA','TSRE','TSRO','TSS','TSYS','TTC','TTEC','TTEK','TTGT','TTI','TTMI','TTPH','TTS','TTWO','TUES','TUMI','TUP','TW','TWC','TWI','TWIN','TWO','TWOU','TWTC','TWTR','TWX','TXI','TXMD','TXN','TXRH','TXT','TXTR','TYC','TYL','TYPE','TZOO','UA','UACL','UAL','UAM','UBA','UBNK','UBNT','UBSH','UBSI','UCBI','UCFC','UCP','UCTT','UDR','UEIC','UFCS','UFI','UFPI','UFPT','UFS','UGI','UHAL','UHS','UHT','UIHC','UIL','UIS','ULTA','ULTI','ULTR','UMBF','UMH','UMPQ','UNF','UNFI','UNH','UNIS','UNM','UNP','UNS','UNT','UPIP','UPL','UPS','URBN','URI','URS','USAK','USAP','USB','USCR','USG','USLM','USM','USMO','USNA','USPH','USTR','UTEK','UTHR','UTI','UTIW','UTL','UTMD','UTX','UVE','UVSP','UVV','V','VAC','VAL','VAR','VASC','VC','VCRA','VCYT','VDSI','VECO','VEEV','VFC','VG','VGR','VHC','VIAB','VIAS','VICR','VITC','VIVO','VLCCF','VLGEA','VLO','VLY','VMC','VMEM','VMI','VMW','VNCE','VNDA','VNO','VNTV','VOLC','VOXX','VOYA','VPFG','VPG','VPRT','VR','VRA','VRNG','VRNS','VRNT','VRSK','VRSN','VRTS','VRTU','VRTX','VSAR','VSAT','VSB','VSEC','VSH','VSI','VSTM','VTG','VTL','VTNR','VTR','VTSS','VVC','VVI','VVTV','VVUS','VZ','WAB','WABC','WAC','WAFD','WAG','WAGE','WAIR','WAL','WASH','WAT','WBC','WBMD','WBS','WCC','WCG','WCIC','WCN','WD','WDAY','WDC','WDFC','WDR','WEC','WEN','WERN','WETF','WEX','WEYS','WFC','WFM','WG','WGL','WGO','WHG','WHR','WIBC','WIFI','WIN','WINA','WIRE','WIX','WLB','WLH','WLK','WLL','WLP','WLT','WM','WMAR','WMB','WMC','WMGI','WMK','WMT','WNC','WNR','WOOF','WOR','WPC','WPG','WPP','WPX','WR','WRB','WRE','WRES','WRI','WRLD','WSBC','WSBF','WSFS','WSM','WSO','WSR','WST','WSTC','WTBA','WTFC','WTI','WTM','WTR','WTS','WTW','WU','WWAV','WWD','WWE','WWW','WWWW','WY','WYN','WYNN','X','XCO','XCRA','XEC','XEL','XL','XLNX','XLRN','XLS','XNCR','XNPT','XOM','XOMA','XON','XONE','XOOM','XOXO','XPO','XRAY','XRM','XRX','XXIA','XXII','XYL','Y','YDKN','YELP','YHOO','YORW','YRCW','YUM','YUME','Z','ZBRA','ZEN','ZEP','ZEUS','ZGNX','ZINC','ZION','ZIOP','ZIXI','ZLTQ','ZMH','ZNGA','ZOES','ZQK','ZTS','ZU','ZUMZ'


]


now=datetime.datetime.now()

def contentfilter():
    with requests.Session() as c:
        map=['']
        stocks=stocklist
        for u in stocks:
            try:
                time.sleep(1)
                url='htt'+'ps://news.google.com/news/rss/search/section/q/'+u+'/'+u+'?hl=en&gl=US&ned=us'
                x=c.get(url)
                x=BeautifulSoup(x.content)
                titles=x.find_all('title')
                pubdate=x.find_all('lastbuilddate')+x.find_all('pubdate')
                for p,t in zip(pubdate,titles):
                    """Assemble our Output Variable"""
                    """Data may be nil/missing or error prone. Going to TRY this step"""
                    pub=str(p.text)
                    info=str(t.text)
                    if info.find(';')>0:
                        info=info[:info.find(';')]



    				###Dynamically determining stock based on text. Assuming results may not match original search keyword
                    stock=info[info.find('(')+1:info.find(')')].replace('NYSE:','').replace('NASDAQ:','').replace('NYSE ','').replace(':','').replace(' ','')
                    grab=info

    				# Save Initial Data to Raw File

    				# f = open('rawmarketmentions.txt'+str(now.month)+'-'+str(now.day)+'-'+str(now.year)+'-UnSelected.txt', 'a')
    				# f.write(grab+' | ' + pub +'\n')
    				# f.close()

    				## Begin filtering the data for model output
    				## First find $$$$
                    if grab.count('$') > 0:
                        targ=int(0)
                        targ=grab.find('$')
                        value=grab[targ+1:targ+5]######## now you have the targeted value

                        try:
                            value=float(value)
                            price=barchart(stock)####### now you have the stock price from quandl
                            if price == None:
    							price=0
                        except:
                            value=0
                            price=0

                        if price>1 and value>0:

                            epsreference=yahooepspuller(stock)

                            if grab.find('EPS') >0 or grab.find('eps') > 0:

                                qpe=round(price/float(value),2)
                                ape=round(price/float(epsreference),2)
                                targetprice=price*((value*4-epsreference)/epsreference) #using marget P/E here insteead of individual stock's p/e to avoid -p/e erro
                                epsexpreturn=(targetprice-price)/price

    							#########################################################
    							##############  Database Connection   ###################
                                conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
                                cur = conn.cursor()
    							# execute a statement
                                cur.execute("INSERT INTO fmi.marketmentions (target, price, returns, ticker, note, date, q_eps, a_eps, q_pe,a_pe report) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)", (targetprice,price,epsexpreturn,stock,grab,pub,value,qpe,ape,epsreference,'earnings'))
                                print("inserted value")
                                conn.commit()
    							# close the communication with the PostgreSQL
                                cur.close()
                                conn.close()


                            if grab.find('arget') > 0:
                                predreturn=(value-price)/price
                                #########################################################
                                ##############  Database Connection   ###################
                                conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
                                cur = conn.cursor()
                                # execute a statement
                                cur.execute("INSERT INTO fmi.marketmentions (target, price, returns, ticker, note, date, q_eps, a_eps, report) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (value,price,predreturn,stock,grab,pub,None,epsreference,'analyst'))
                                print("inserted value")
                                conn.commit()
                                # close the communication with the PostgreSQL
                                cur.close()
                                conn.close()
            except:
                pass


#run for 100 cycles of 6 hours each

mmduprem()
contentfilter()
mmduprem()
print('end')
