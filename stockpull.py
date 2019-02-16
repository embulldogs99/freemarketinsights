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
import random

warnings.filterwarnings('ignore')
today=datetime.date.today()

###########################################################
##########################################################
######## Used QUANDL Functions #########################

quandl.ApiConfig.api_key = 'omQiMysF2NQ1B-xZEJBk'

def quandl_stocks(symbol, start_date=(2018, 1, 1), end_date=None):
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
			price=float(data)
		except:
			price=None
		return price




def quandl_stocks_5_year(symbol, start_date=(today.year-5, today.month, today.day), end_date=None):
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

def quandl_five_yr_low(ticker):
    if len(ticker)<5:
        data=pd.DataFrame(quandl_stocks_5_year(ticker))
        min=data.min()
        try:
            min=float(min)
            return min
        except:
            pass

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
        try:
            price=float(s[0])
        except:
            price=None
        return price


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


##############################################################
############ Robinhood API Fucntions #####################
def robinhooddivyield(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['dividend_yield'])

def robinhoodpe(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['pe_ratio'])

def robinhood52high(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['high_52_weeks'])

def robinhood52low(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['low_52_weeks'])

def robinhoodmarketcap(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['market_cap'])

def robinhoodprice(ticker):
    url = "https://api.robinhood.com/quotes/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['ask_price'])


################################################################
############ Google API Functions  ##############################

def googlefinancepricepull(ticker):
    url="https://finance.google.com/finance?q="+ticker+"&output=json"
    with requests.Session() as c:
        x=c.get(url)
        time.sleep(120)
        x=BeautifulSoup(x.content)
        d=x.find_all()
        d=str(d)
        if d.find("The block will expire shortly after those requests stop"):
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("-------------------------    Gooogle  SHUDOWN  -----------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            print("----------------------------------------------------------------------")
            time.sleep(120)
            return 0
        else:
            s=d.find("<b>")
            short=d[s+20:s+2000]
            s2=short.find("<b>")
            short=short[s2:s2+2000]
            s3=short.find("</b>")
            price=short[3:s3]
            try:
                price=float(price)
            except:
                price=0
            return (price)



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
#
# 'MMM','AOS','ABT','ABBV','ACN','ATVI','AYI','ADBE','AAP','AMD','AES','AET','AMG','AFL','A','APD','AKAM','ALK','ALB','ARE','ALXN','ALGN','ALLE','AGN','ADS','LNT','ALL','GOOGL','GOOG','MO','AMZN','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','APC','ADI','ANDV','ANSS','ANTM','AON','APA','AIV','AAPL','AMAT','APTV','ADM','ARNC','AJG','AIZ','T','ADSK','ADP','AZO','AVB','AVY','BHGE','BLL','BAC','BAX','BBT','BDX','BRK.B','BBY','BIIB','BLK','HRB','BA','BKNG','BWA','BXP','BSX','BHF','BMY','AVGO','BF.B','CHRW','CA','COG','CDNS','CPB','COF','CAH','KMX','CCL','CAT','CBOE','CBRE','CBS','CELG','CNC','CNP','CTL','CERN','CF','SCHW','CHTR','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','CXO','COP','ED','STZ','GLW','COST','COTY','CCI','CSRA','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','DLR','DFS','DISCA','DISCK','DISH','DG','DLTR','D','DOV','DWDP','DPS','DTE','DUK','DRE','DXC','ETFC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ETR','EVHC','EOG','EQT','EFX','EQIX','EQR','ESS','EL','RE','ES','EXC','EXPE','EXPD','ESRX','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FE','FISV','FLIR','FLS','FLR','FMC','FL','F','FTV','FBHS','BEN','FCX','GPS','GRMN','IT','GD','GE','GGP','GIS','GM','GPC','GILD','GPN','GS','GT','GWW','HAL','HBI','HOG','HRS','HIG','HAS','HCA','HCP','HP','HSIC','HES','HPE','HLT','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','HII','IDXX','INFO','ITW','ILMN','INCY','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JBHT','JEC','SJM','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LLL','LH','LRCX','LEG','LEN','LUK','LLY','LNC','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MRO','MPC','MAR','MMC','MLM','MAS','MA','MAT','MKC','MCD','MCK','MDT','MRK','MET','MTD','MGM','KORS','MCHP','MU','MSFT','MAA','MHK','TAP','MDLZ','MON','MNST','MCO','MS','MSI','MYL','NDAQ','NOV','NAVI','NKTR','NTAP','NFLX','NWL','NFX','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS','NOC','NCLH','NRG','NUE','NVDA','ORLY','OXY','OMC','OKE','ORCL','PCAR','PKG','PH','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE','PCG','PM','PSX','PNW','PXD','PNC','RL','PPG','PPL','PX','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO','QCOM','PWR','DGX','RRC','RJF','RTN','O','RHT','REG','REGN','RF','RSG','RMD','RHI','ROK','COL','ROP','ROST','RCL','SPGI','CRM','SBAC','SCG','SLB','STX','SEE','SRE','SHW','SPG','SWKS','SLG','SNA','SO','LUV','SWK','SBUX','STT','SRCL','SYK','STI','SIVB','SYMC','SYF','SNPS','SYY','TROW','TTWO','TPR','TGT','TEL','FTI','TXN','TXT','BK','CLX','COO','HSY','MOS','TRV','DIS','TMO','TIF','TWX','TJX','TMK','TSS','TSCO','TDG','TRIP','FOXA','FOX','TSN','USB','UDR','ULTA','UAA','UA','UNP','UAL','UNH','UPS','URI','UTX','UHS','UNM','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WMT','WBA','WM','WAT','WEC','WFC','WELL','WDC','WU','WRK','WY','WHR','WMB','WLTW','WYN','WYNN','XEL','XRX','XLNX','XL','XYL','YUM','ZBH','ZION','ZTS','MHLD','ORIT','ALGT','ELY','NTRI','PETS','NVDA','TSLA'
#
# ##################
# ###   NASDAQ   ###
# ###################
# ,'AAL','AAPL','ADBE','ADI','ADP','ADSK','AKAM','ALGN','ALXN','AMAT','AMGN','AMZN','ATVI','AVGO','BIDU','BIIB','BMRN','CA','CELG','CERN','CHKP','CHTR','CTRP','CTAS','CSCO','CTXS','CMCSA','COST','CSX','CTSH','DISCA','DISCK','DISH','DLTR','EA','EBAY','ESRX','EXPE','FAST','FB','FISV','FOX','FOXA','GILD','GOOG','GOOGL','HAS','HSIC','HOLX','ILMN','INCY','INTC','INTU','ISRG','JBHT','JD','KLAC','KHC','LBTYK','LILA','LBTYA','QRTEA','MELI','MAR','MAT','MDLZ','MNST','MSFT','MU','MXIM','MYL','NCLH','NFLX','NTES','NVDA','PAYX','BKNG','PYPL','QCOM','REGN','ROST','SHPG','SIRI','SWKS','SBUX','SYMC','TSCO','TXN','TMUS','ULTA','VIAB','VOD','VRTX','WBA','WDC','XRAY','IDXX','LILAK','LRCX','MCHP','ORLY','PCAR','STX','TSLA','VRSK','WYNN','XLNX'

########################
###   Russell 3000  #####
###########################

'AA','AAL','AAMC','AAN','AAOI','AAON','AAP','AAPL','AAT','AAWW','ABAX','ABBV','ABC','ABCB','ABCO','ABG','ABM','ABMD','ABT','ACAD','ACAT','ACC','ACCO','ACE','ACET','ACGL','ACHC','ACHN','ACI','ACIW','ACLS','ACM','ACN','ACOR','ACRE','ACRX','ACT','ACTG','ACW','ACXM','ADBE','ADC','ADES','ADI','ADM','ADMS','ADNC','ADP','ADS','ADSK','ADT','ADTN','ADUS','ADVS','AE','AEC','AEE','AEGN','AEGR','AEIS','AEL','AEO','AEP','AEPI','AERI','AES','AET','AF','AFAM','AFFX','AFG','AFH','AFL','AFOP','AFSI','AGCO','AGEN','AGII','AGIO','AGM','AGN','AGNC','AGO','AGTC','AGX','AGYS','AHC','AHH','AHL','AHP','AHS','AHT','AI','AIG','AIMC','AIN','AIQ','AIR','AIRM','AIT','AIV','AIZ','AJG','AKAM','AKAO','AKBA','AKR','AKRX','AKS','AL','ALB','ALCO','ALDR','ALE','ALEX','ALG','ALGN','ALGT','ALIM','ALJ','ALK','ALKS','ALL','ALLE','ALLY','ALNY','ALOG','ALR','ALSN','ALTR','ALX','ALXN','AMAG','AMAT','AMBA','AMBC','AMBR','AMC','AMCC','AMCX','AMD','AME','AMED','AMG','AMGN','AMH','AMKR','AMNB','AMP','AMPE','AMRC','AMRE','AMRI','AMRS','AMSF','AMSG','AMSWA','AMT','AMTD','AMTG','AMWD','AMZG','AMZN','AN','ANAC','ANAT','ANDE','ANF','ANGI','ANGO','ANH','ANIK','ANIP','ANN','ANR','ANSS','ANV','AOI','AOL','AON','AOS','AOSL','AP','APA','APAGF','APAM','APC','APD','APEI','APH','APOG','APOL','AR','ARAY','ARC','ARCB','ARCP','ARCW','ARE','AREX','ARG','ARI','ARIA','ARII','ARMK','ARNA','ARO','AROW','ARPI','ARR','ARRS','ARRY','ARTNA','ARUN','ARW','ARWR','ARX','ASBC','ASC','ASCMA','ASEI','ASGN','ASH','ASNA','ASPS','ASPX','ASTE','AT','ATEN','ATHL','ATHN','ATI','ATK','ATLO','ATML','ATNI','ATNM','ATO','ATR','ATRC','ATRI','ATRO','ATRS','ATSG','ATU','ATVI','ATW','AUXL','AVA','AVAV','AVB','AVD','AVG','AVGO','AVHI','AVIV','AVNR','AVP','AVT','AVX','AVY','AWAY','AWH','AWI','AWK','AWR','AXAS','AXDX','AXE','AXL','AXLL','AXP','AXS','AYI','AYR','AZO','AZPN','AZZ','B','BA','BABY','BAC','BAGL','BAH','BALT','BANC','BANF','BANR','BAS','BAX','BBBY','BBCN','BBG','BBNK','BBOX','BBRG','BBSI','BBT','BBW','BBX','BBY','BC','BCC','BCEI','BCO','BCOR','BCOV','BCPC','BCR','BCRX','BDBD','BDC','BDE','BDGE','BDN','BDSI','BDX','BEAT','BEAV','BEBE','BECN','BEE','BELFB','BEN','BERY','BF.B','BFAM','BFIN','BFS','BG','BGC','BGCP','BGFV','BGG','BGS','BH','BHE','BHI','BHLB','BID','BIG','BIIB','BIO','BIOS','BIRT','BJRI','BK','BKD','BKE','BKH','BKMU','BKS','BKU','BKW','BKYF','BLDR','BLK','BLKB','BLL','BLMN','BLOX','BLT','BLUE','BLX','BMI','BMR','BMRC','BMRN','BMS','BMTC','BMY','BNCL','BNCN','BNFT','BNNY','BOBE','BOFI','BOH','BOKF','BONT','BOOM','BPFH','BPI','BPOP','BPTH','BPZ','BR','BRC','BRCD','BRCM','BRDR','BREW','BRK.B','BRKL','BRKR','BRKS','BRLI','BRO','BRS','BRSS','BRX','BSFT','BSRR','BSTC','BSX','BTU','BTX','BURL','BUSE','BV','BWA','BWC','BWINB','BWLD','BWS','BXP','BXS','BYD','BYI','BZH','C','CA','CAB','CAC','CACB','CACC','CACI','CACQ','CAG','CAH','CAKE','CALD','CALL','CALM','CALX','CAM','CAMP','CAP','CAR','CARA','CARB','CAS','CASH','CASS','CASY','CAT','CATM','CATO','CATY','CAVM','CB','CBB','CBEY','CBF','CBG','CBI','CBK','CBL','CBM','CBOE','CBPX','CBR','CBRL','CBS','CBSH','CBSO','CBST','CBT','CBU','CBZ','CCBG','CCC','CCE','CCF','CCG','CCI','CCK','CCL','CCMP','CCNE','CCO','CCOI','CCRN','CCXI','CDE','CDI','CDNS','CDR','CDW','CE','CEB','CECE','CECO','CELG','CEMP','CENTA','CENX','CERN','CERS','CETV','CEVA','CF','CFFN','CFI','CFN','CFNL','CFR','CFX','CGI','CGNX','CHCO','CHD','CHDN','CHDX','CHE','CHEF','CHFC','CHFN','CHGG','CHH','CHK','CHMT','CHRW','CHS','CHSP','CHTR','CHUY','CI','CIA','CIDM','CIE','CIEN','CIFC','CIM','CINF','CIR','CIT','CJES','CKEC','CKH','CKP','CL','CLC','CLCT','CLD','CLDT','CLDX','CLF','CLFD','CLGX','CLH','CLI','CLMS','CLNE','CLNY','CLR','CLVS','CLW','CLX','CMA','CMC','CMCO','CMCSA','CME','CMG','CMI','CMLS','CMN','CMO','CMP','CMRX','CMS','CMTL','CNA','CNBC','CNBKA','CNC','CNK','CNL','CNMD','CNO','CNOB','CNP','CNQR','CNS','CNSI','CNSL','CNVR','CNW','CNX','COB','COBZ','CODE','COF','COG','COH','COHR','COHU','COKE','COL','COLB','COLM','COMM','CONE','CONN','COO','COP','COR','CORE','CORR','CORT','COST','COTY','COUP','COV','COVS','COWN','CPA','CPB','CPE','CPF','CPHD','CPK','CPLA','CPN','CPRT','CPS','CPSI','CPSS','CPST','CPT','CPWR','CQB','CR','CRAI','CRAY','CRCM','CRD.B','CREE','CRI','CRK','CRL','CRM','CRMT','CROX','CRR','CRRS','CRS','CRUS','CRVL','CRWN','CRY','CRZO','CSBK','CSC','CSCD','CSCO','CSFL','CSG','CSGP','CSGS','CSH','CSII','CSL','CSLT','CSOD','CSS','CST','CSU','CSV','CSX','CTAS','CTB','CTBI','CTCT','CTG','CTIC','CTL','CTO','CTRE','CTRL','CTRN','CTRX','CTS','CTSH','CTT','CTWS','CTXS','CUB','CUBE','CUBI','CUDA','CUI','CUNB','CUR','CUZ','CVA','CVBF','CVC','CVCO','CVD','CVEO','CVG','CVGI','CVGW','CVI','CVLT','CVO','CVS','CVT','CVX','CW','CWEI','CWH','CWST','CWT','CXO','CXP','CXW','CY','CYBX','CYH','CYN','CYNI','CYNO','CYS','CYT','CYTK','CYTR','CYTX','CZNC','CZR','D','DAKT','DAL','DAN','DAR','DATA','DAVE','DBD','DCI','DCO','DCOM','DCT','DD','DDD','DDR','DDS','DE','DECK','DEI','DEL','DENN','DEPO','DEST','DF','DFRG','DFS','DFT','DFZ','DG','DGI','DGICA','DGII','DGX','DHI','DHIL','DHR','DHT','DHX','DIN','DIOD','DIS','DISCA','DISH','DJCO','DK','DKS','DLB','DLR','DLTR','DLX','DMD','DMND','DMRC','DNB','DNDN','DNKN','DNOW','DNR','DO','DOC','DOOR','DORM','DOV','DOW','DOX','DPS','DPZ','DRC','DRE','DRH','DRI','DRII','DRIV','DRNA','DRQ','DRTX','DSCI','DSPG','DST','DSW','DTE','DTLK','DTSI','DTV','DUK','DV','DVA','DVAX','DVN','DW','DWA','DWRE','DWSN','DX','DXCM','DXLG','DXM','DXPE','DXYN','DY','DYAX','DYN','EA','EAC','EAT','EBAY','EBF','EBIO','EBIX','EBS','EBSB','EBTC','ECHO','ECL','ECOL','ECOM','ECPG','ECYT','ED','EDE','EDMC','EDR','EE','EEFT','EFII','EFSC','EFX','EGBN','EGHT','EGL','EGLT','EGN','EGOV','EGP','EGY','EHTH','EIG','EIGI','EIX','EL','ELGX','ELLI','ELNK','ELRC','ELS','ELX','ELY','EMC','EMCI','EME','EMN','EMR','ENDP','ENH','ENOC','ENPH','ENR','ENS','ENSG','ENT','ENTA','ENTG','ENTR','ENV','ENVE','ENZ','EOG','EOPN','EOX','EPAM','EPAY','EPE','EPIQ','EPM','EPR','EPZM','EQIX','EQR','EQT','EQU','EQY','ERA','ERIE','ERII','EROS','ESBF','ESC','ESCA','ESE','ESGR','ESI','ESIO','ESL','ESNT','ESPR','ESRT','ESRX','ESS','ETFC','ETH','ETM','ETN','ETR','EV','EVC','EVDY','EVER','EVHC','EVR','EVTC','EW','EWBC','EXAC','EXAM','EXAR','EXAS','EXC','EXEL','EXH','EXL','EXLS','EXP','EXPD','EXPE','EXPO','EXPR','EXR','EXTR','EXXI','EZPW','F','FAF','FANG','FARM','FARO','FAST','FB','FBC','FBHS','FBIZ','FBNC','FBNK','FBP','FBRC','FC','FCBC','FCE.A','FCEL','FCF','FCFS','FCH','FCN','FCNCA','FCS','FCX','FDEF','FDML','FDO','FDP','FDS','FDX','FE','FEIC','FELE','FET','FEYE','FF','FFBC','FFG','FFIC','FFIN','FFIV','FFNW','FGL','FHCO','FHN','FI','FIBK','FICO','FII','FINL','FIO','FIS','FISI','FISV','FITB','FIVE','FIVN','FIX','FIZZ','FL','FLDM','FLIC','FLIR','FLO','FLR','FLS','FLT','FLTX','FLWS','FLXN','FLXS','FMBI','FMC','FMER','FMI','FN','FNB','FNF','FNFG','FNGN','FNHC','FNLC','FNSR','FOE','FOR','FORM','FORR','FOSL','FOXA','FOXF','FPO','FPRX','FR','FRAN','FRBK','FRC','FRED','FRGI','FRM','FRME','FRNK','FRO','FRP','FRSH','FRT','FRX','FSL','FSLR','FSP','FSS','FST','FSTR','FSYS','FTD','FTI','FTK','FTNT','FTR','FUBC','FUEL','FUL','FULT','FUR','FURX','FVE','FWLT','FWM','FWRD','FXCB','FXCM','FXEN','G','GABC','GAIA','GALE','GALT','GAS','GB','GBCI','GBL','GBLI','GBNK','GBX','GCA','GCAP','GCI','GCO','GD','GDOT','GDP','GE','GEF','GEO','GEOS','GERN','GES','GEVA','GFF','GFIG','GFN','GGG','GGP','GHC','GHDX','GHL','GHM','GIFI','GIII','GILD','GIMO','GIS','GK','GLDD','GLF','GLNG','GLOG','GLPI','GLPW','GLRE','GLRI','GLT','GLUU','GLW','GM','GMCR','GME','GMED','GMT','GNC','GNCA','GNCMA','GNMK','GNRC','GNTX','GNW','GOGO','GOOD','GOOG','GOOGL','GORO','GOV','GPC','GPI','GPK','GPN','GPOR','GPRE','GPS','GPT','GPX','GRA','GRC','GRMN','GRPN','GRT','GRUB','GS','GSAT','GSBC','GSIG','GSM','GSOL','GST','GT','GTAT','GTI','GTIV','GTLS','GTN','GTS','GTT','GTY','GUID','GVA','GWR','GWRE','GWW','GXP','GY','H','HA','HAE','HAFC','HAIN','HAL','HALL','HALO','HAR','HAS','HASI','HAWK','HAYN','HBAN','HBHC','HBI','HBNC','HCA','HCBK','HCC','HCCI','HCI','HCKT','HCN','HCOM','HCP','HCSG','HCT','HD','HDS','HE','HEAR','HEES','HEI','HELE','HELI','HEOP','HERO','HES','HF','HFC','HFWA','HGG','HGR','HHC','HHS','HI','HIBB','HIG','HII','HIL','HILL','HITT','HIVE','HIW','HK','HL','HLF','HLIT','HLS','HLSS','HLT','HLX','HME','HMHC','HMN','HMPR','HMST','HMSY','HMTV','HNH','HNI','HNR','HNRG','HNT','HOG','HOLX','HOMB','HON','HOS','HOT','HOV','HP','HPP','HPQ','HPT','HPTX','HPY','HR','HRB','HRC','HRG','HRL','HRS','HRTG','HRTX','HSC','HSH','HSIC','HSII','HSNI','HSP','HST','HSTM','HSY','HT','HTA','HTBI','HTBK','HTH','HTLD','HTLF','HTS','HTWR','HTZ','HUB.B','HUBG','HUM','HUN','HURC','HURN','HVB','HVT','HW','HWAY','HWCC','HWKN','HXL','HY','HZNP','HZO','I','IACI','IART','IBCP','IBKC','IBKR','IBM','IBOC','IBP','IBTX','ICE','ICEL','ICFI','ICGE','ICON','ICPT','ICUI','IDA','IDCC','IDIX','IDRA','IDT','IDTI','IDXX','IEX','IFF','IG','IGT','IGTE','IHC','IHS','III','IIIN','IILG','IIVI','IL','ILMN','IM','IMGN','IMKTA','IMMR','IMMU','IMPV','IMS','INAP','INCY','INDB','INFA','INFI','INFN','INGN','INGR','ININ','INN','INO','INSM','INSY','INT','INTC','INTL','INTU','INVN','INWK','IO','IOSP','IP','IPAR','IPCC','IPCM','IPG','IPGP','IPHI','IPHS','IPI','IPXL','IQNT','IR','IRBT','IRC','IRDM','IRET','IRF','IRG','IRM','IRWD','ISBC','ISCA','ISH','ISIL','ISIS','ISLE','ISRG','ISRL','ISSI','IT','ITC','ITCI','ITG','ITMN','ITRI','ITT','ITW','IVAC','IVC','IVR','IVZ','IXYS','JACK','JAH','JAKK','JAZZ','JBHT','JBL','JBLU','JBSS','JBT','JCI','JCOM','JCP','JDSU','JEC','JGW','JIVE','JJSF','JKHY','JLL','JMBA','JNJ','JNPR','JNS','JOE','JONE','JOUT','JOY','JPM','JRN','JW.A','JWN','K','KAI','KALU','KAMN','KAR','KATE','KBALB','KBH','KBR','KCG','KCLI','KEG','KELYA','KEM','KERX','KEX','KEY','KEYW','KFRC','KFX','KFY','KIM','KIN','KIRK','KKD','KLAC','KMB','KMG','KMI','KMPR','KMT','KMX','KN','KND','KNL','KNX','KO','KODK','KOG','KOP','KOPN','KORS','KOS','KPTI','KR','KRA','KRC','KRFT','KRG','KRNY','KRO','KS','KSS','KSU','KTOS','KTWO','KVHI','KW','KWK','KWR','KYTH','L','LABL','LAD','LADR','LAMR','LANC','LAYN','LAZ','LB','LBAI','LBMH','LBY','LCI','LCUT','LDL','LDOS','LDR','LDRH','LE','LEA','LEAF','LECO','LEE','LEG','LEN','LF','LFUS','LG','LGF','LGIH','LGND','LH','LHCG','LHO','LII','LINTA','LION','LIOX','LKFN','LKQ','LL','LLL','LLNW','LLTC','LLY','LM','LMCA','LMIA','LMNR','LMNX','LMOS','LMT','LNC','LNCE','LNDC','LNG','LNKD','LNN','LNT','LO','LOCK','LOGM','LOPE','LORL','LOW','LPG','LPI','LPLA','LPNT','LPSN','LPT','LPX','LQ','LQDT','LRCX','LRN','LSCC','LSTR','LTC','LTM','LTS','LUK','LUV','LVLT','LVNTA','LVS','LWAY','LXFT','LXK','LXP','LXRX','LXU','LYB','LYTS','LYV','LZB','M','MA','MAA','MAC','MACK','MAN','MANH','MANT','MAR','MAS','MASI','MAT','MATW','MATX','MBFI','MBI','MBII','MBUU','MBVT','MBWM','MC','MCBC','MCD','MCF','MCHP','MCHX','MCK','MCO','MCP','MCRI','MCRL','MCRS','MCS','MCY','MD','MDAS','MDC','MDCA','MDCO','MDLZ','MDP','MDR','MDRX','MDSO','MDT','MDU','MDVN','MDXG','MEAS','MED','MEG','MEI','MENT','MET','METR','MFA','MFLX','MFRM','MG','MGAM','MGEE','MGI','MGLN','MGM','MGNX','MGRC','MHFI','MHGC','MHK','MHLD','MHO','MHR','MIDD','MIG','MILL','MIND','MINI','MITT','MJN','MKC','MKL','MKSI','MKTO','MKTX','MLAB','MLHR','MLI','MLM','MLNK','MLR','MM','MMC','MMI','MMM','MMS','MMSI','MN','MNI','MNK','MNKD','MNR','MNRO','MNST','MNTA','MNTX','MO','MOD','MODN','MOFG','MOG.A','MOH','MON','MORN','MOS','MOV','MOVE','MPAA','MPC','MPO','MPW','MPWR','MPX','MRC','MRCY','MRGE','MRH','MRIN','MRK','MRLN','MRO','MRTN','MRTX','MRVL','MS','MSA','MSCC','MSCI','MSEX','MSFG','MSFT','MSG','MSI','MSL','MSM','MSO','MSTR','MTB','MTD','MTDR','MTG','MTGE','MTH','MTN','MTOR','MTRN','MTRX','MTSC','MTSI','MTW','MTX','MTZ','MU','MUR','MUSA','MVNR','MW','MWA','MWIV','MWV','MWW','MXIM','MXL','MXWL','MYCC','MYE','MYGN','MYL','MYRG','N','NADL','NANO','NASB','NAT','NATH','NATI','NATL','NATR','NAV','NAVB','NAVG','NAVI','NBBC','NBCB','NBHC','NBIX','NBL','NBR','NBS','NBTB','NC','NCFT','NCI','NCLH','NCMI','NCR','NCS','NDAQ','NDLS','NDSN','NEE','NEM','NEOG','NES','NEU','NEWM','NEWP','NEWS','NFBK','NFG','NFLX','NFX','NGHC','NGS','NGVC','NHC','NHI','NI','NICK','NILE','NJR','NKE','NKSH','NKTR','NL','NLNK','NLS','NLSN','NLY','NM','NMBL','NMIH','NMRX','NNA','NNBR','NNI','NNN','NNVC','NOC','NOG','NOR','NOV','NOW','NP','NPBC','NPK','NPO','NPSP','NR','NRCIA','NRF','NRG','NRIM','NRZ','NSC','NSIT','NSM','NSP','NSR','NSTG','NTAP','NTCT','NTGR','NTK','NTLS','NTRI','NTRS','NU','NUAN','NUE','NUS','NUTR','NUVA','NVAX','NVDA','NVEC','NVR','NWBI','NWBO','NWE','NWHM','NWL','NWLI','NWN','NWPX','NWSA','NWY','NX','NXST','NXTM','NYCB','NYLD','NYMT','NYNY','NYRT','NYT','O','OABC','OAS','OB','OC','OCFC','OCLR','OCN','OCR','ODC','ODFL','ODP','OEH','OFC','OFG','OFIX','OFLX','OGE','OGS','OHI','OHRP','OI','OII','OIS','OKE','OKSB','OLBK','OLED','OLN','OLP','OMC','OMCL','OME','OMED','OMER','OMG','OMI','OMN','ONB','ONE','ONNN','ONTY','ONVO','OPB','OPEN','OPHT','OPK','OPLK','OPWR','OPY','ORA','ORB','ORBC','ORCL','OREX','ORI','ORIT','ORLY','ORM','ORN','OSIR','OSIS','OSK','OSTK','OSUR','OTTR','OUTR','OVAS','OVTI','OWW','OXFD','OXM','OXY','OZRK','P','PACB','PACW','PAG','PAH','PAHC','PANW','PATK','PATR','PAY','PAYC','PAYX','PB','PBCT','PBF','PBH','PBI','PBPB','PBY','PBYI','PCAR','PCBK','PCCC','PCG','PCH','PCL','PCLN','PCO','PCP','PCRX','PCTY','PCYC','PCYG','PDCE','PDCO','PDFS','PDLI','PDM','PE','PEB','PEBO','PEG','PEGA','PEGI','PEI','PEIX','PENN','PEP','PERY','PES','PETM','PETS','PETX','PF','PFBC','PFE','PFG','PFIE','PFIS','PFMT','PFPT','PFS','PFSI','PG','PGC','PGEM','PGI','PGNX','PGR','PGTI','PH','PHH','PHIIK','PHM','PHMD','PHX','PICO','PII','PIKE','PINC','PIR','PJC','PKD','PKE','PKG','PKI','PKOH','PKT','PKY','PL','PLAB','PLCE','PLCM','PLD','PLKI','PLL','PLMT','PLOW','PLPC','PLT','PLUG','PLUS','PLXS','PLXT','PM','PMC','PMCS','PMT','PNC','PNFP','PNK','PNM','PNR','PNRA','PNW','PNX','PNY','PODD','POL','POM','POOL','POR','POST','POWI','POWL','POWR','POZN','PPBI','PPC','PPG','PPHM','PPL','PPO','PPS','PQ','PRA','PRAA','PRE','PRFT','PRGO','PRGS','PRGX','PRI','PRIM','PRK','PRKR','PRLB','PRO','PRSC','PRTA','PRU','PRXL','PSA','PSB','PSEM','PSIX','PSMI','PSMT','PSTB','PSUN','PSX','PTC','PTCT','PTEN','PTIE','PTLA','PTP','PTRY','PTSI','PTX','PVA','PVH','PVTB','PWOD','PWR','PX','PXD','PZN','PZZA','Q','QADA','QCOM','QCOR','QDEL','QEP','QGEN','QLGC','QLIK','QLTY','QLYS','QNST','QRHC','QSII','QTM','QTS','QTWO','QUAD','QUIK','R','RAD','RAI','RAIL','RALY','RARE','RAS','RATE','RAVN','RAX','RBC','RBCAA','RBCN','RCAP','RCII','RCL','RCPT','RDC','RDEN','RDI','RDN','RDNT','RE','RECN','REG','REGI','REGN','REI','REIS','REMY','REN','RENT','RES','RESI','REV','REX','REXI','REXR','REXX','RF','RFMD','RFP','RGA','RGC','RGDO','RGEN','RGLD','RGLS','RGR','RGS','RH','RHI','RHP','RHT','RICE','RIGL','RJET','RJF','RKT','RKUS','RL','RLD','RLGY','RLI','RLJ','RLOC','RLYP','RM','RMAX','RMBS','RMD','RMTI','RNDY','RNET','RNG','RNR','RNST','RNWK','ROC','ROCK','ROG','ROIAK','ROIC','ROK','ROL','ROLL','ROP','ROSE','ROST','ROVI','RP','RPAI','RPM','RPRX','RPT','RPTP','RPXC','RRC','RRD','RRGB','RRTS','RS','RSE','RSG','RSO','RSPP','RST','RSTI','RT','RTEC','RTI','RTIX','RTK','RTN','RTRX','RUBI','RUSHA','RUTH','RVBD','RVLT','RVNC','RWT','RXN','RYL','RYN','S','SAAS','SABR','SAFM','SAFT','SAH','SAIA','SAIC','SALE','SALM','SALT','SAM','SAMG','SANM','SAPE','SASR','SATS','SAVE','SB','SBAC','SBCF','SBGI','SBH','SBNY','SBRA','SBSI','SBUX','SBY','SC','SCAI','SCBT','SCCO','SCG','SCHL','SCHN','SCHW','SCI','SCL','SCLN','SCMP','SCOR','SCS','SCSC','SCSS','SCTY','SCVL','SD','SDRL','SE','SEAC','SEAS','SEB','SEE','SEIC','SEM','SEMG','SENEA','SF','SFBS','SFE','SFG','SFL','SFLY','SFM','SFNC','SFXE','SFY','SGA','SGBK','SGEN','SGI','SGK','SGM','SGMO','SGMS','SGNT','SGY','SGYP','SHEN','SHLD','SHLM','SHLO','SHO','SHOO','SHOR','SHOS','SHW','SIAL','SIF','SIG','SIGI','SIMG','SIR','SIRI','SIRO','SIVB','SIX','SJI','SJM','SJW','SKH','SKT','SKUL','SKX','SKYW','SLAB','SLB','SLCA','SLG','SLGN','SLH','SLM','SLXP','SM','SMA','SMCI','SMG','SMP','SMRT','SMTC','SN','SNA','SNAK','SNBC','SNCR','SNDK','SNH','SNHY','SNI','SNMX','SNOW','SNPS','SNSS','SNTA','SNV','SNX','SO','SON','SONC','SONS','SP','SPA','SPAR','SPB','SPDC','SPF','SPG','SPLK','SPLS','SPN','SPNC','SPNS','SPPI','SPR','SPSC','SPTN','SPW','SPWH','SPWR','SQBG','SQBK','SQI','SQNM','SRC','SRCE','SRCL','SRDX','SRE','SREV','SRI','SRPT','SSD','SSI','SSNC','SSNI','SSP','SSS','SSTK','SSYS','STAA','STAG','STAR','STBA','STBZ','STC','STCK','STE','STFC','STI','STJ','STL','STLD','STML','STMP','STNG','STNR','STR','STRA','STRL','STRT','STRZA','STT','STWD','STZ','SUBK','SUI','SUNE','SUP','SUPN','SUSQ','SUSS','SVU','SWAY','SWC','SWFT','SWHC','SWI','SWK','SWKS','SWM','SWN','SWS','SWX','SWY','SXC','SXI','SXT','SYA','SYBT','SYK','SYKE','SYMC','SYNA','SYNT','SYRG','SYUT','SYX','SYY','SZMK','SZYM','T','TAHO','TAL','TAM','TAP','TASR','TAST','TAT','TAX','TAYC','TBBK','TBI','TBNK','TBPH','TCB','TCBI','TCBK','TCO','TCS','TDC','TDG','TDS','TDW','TDY','TE','TECD','TECH','TEG','TEN','TER','TESO','TESS','TEX','TFM','TFSL','TFX','TG','TGH','TGI',
# 'TGT',
# 'TGTX',
'THC','THFF','THG','THLD','THO','THOR','THR','THRM','THRX','THS','TIBX','TIF','TILE','TIME','TIPT','TIS','TISI','TITN','TIVO','TJX','TK','TKR','TLMR','TLYS','TMH','TMHC','TMK','TMO','TMP','TMUS','TNAV','TNC','TNDM','TNET','TNGO','TNK','TOL','TOWN','TOWR','TPC','TPH','TPLM','TPRE','TPX','TQNT','TR','TRAK','TRC','TREC','TREE','TREX','TRGP','TRI','TRIP','TRIV','TRK','TRLA','TRMB','TRMK','TRMR','TRN','TRNO','TRNX','TROW','TROX','TRS','TRST','TRUE','TRV','TRW','TRXC','TSC','TSCO','TSLA','TSN','TSO','TSRA','TSRE','TSRO','TSS','TSYS','TTC','TTEC','TTEK',
#'TTGT',
'TTI','TTMI','TTPH','TTS','TTWO','TUES','TUMI','TUP','TW','TWC','TWI','TWIN','TWO','TWOU','TWTC','TWTR','TWX','TXI','TXMD','TXN','TXRH','TXT','TXTR','TYC','TYL','TYPE','TZOO','UA','UACL','UAL','UAM','UBA','UBNK','UBNT','UBSH','UBSI','UCBI','UCFC','UCP','UCTT','UDR','UEIC','UFCS','UFI','UFPI','UFPT','UFS','UGI','UHAL','UHS','UHT','UIHC','UIL','UIS','ULTA','ULTI','ULTR','UMBF','UMH','UMPQ','UNF','UNFI','UNH','UNIS','UNM','UNP','UNS','UNT','UPIP','UPL','UPS','URBN','URI','URS','USAK','USAP','USB','USCR','USG','USLM','USM','USMO','USNA','USPH','USTR','UTEK','UTHR','UTI','UTIW','UTL','UTMD','UTX','UVE','UVSP','UVV','V','VAC','VAL','VAR','VASC','VC','VCRA','VCYT','VDSI','VECO','VEEV','VFC','VG','VGR','VHC','VIAB','VIAS','VICR','VITC','VIVO','VLCCF','VLGEA','VLO','VLY','VMC','VMEM','VMI','VMW','VNCE','VNDA','VNO','VNTV','VOLC','VOXX','VOYA','VPFG','VPG','VPRT','VR','VRA','VRNG','VRNS','VRNT','VRSK','VRSN','VRTS','VRTU','VRTX','VSAR','VSAT','VSB','VSEC','VSH','VSI','VSTM','VTG','VTL','VTNR','VTR','VTSS','VVC','VVI','VVTV','VVUS','VZ','WAB','WABC','WAC','WAFD','WAG','WAGE','WAIR','WAL','WASH','WAT','WBC','WBMD','WBS','WCC','WCG','WCIC','WCN','WD','WDAY','WDC','WDFC','WDR','WEC','WEN','WERN','WETF','WEX','WEYS','WFC','WFM','WG','WGL','WGO','WHG','WHR','WIBC','WIFI','WIN','WINA','WIRE','WIX','WLB','WLH','WLK','WLL','WLP','WLT','WM','WMAR','WMB','WMC','WMGI','WMK','WMT','WNC','WNR','WOOF','WOR','WPC','WPG','WPP','WPX','WR','WRB','WRE','WRES','WRI','WRLD','WSBC','WSBF','WSFS','WSM','WSO','WSR','WST','WSTC','WTBA','WTFC','WTI','WTM','WTR','WTS','WTW','WU','WWAV','WWD','WWE','WWW','WWWW','WY','WYN','WYNN','X','XCO','XCRA','XEC','XEL','XL','XLNX','XLRN','XLS','XNCR','XNPT','XOM','XOMA','XON','XONE','XOOM','XOXO','XPO','XRAY','XRM','XRX','XXIA','XXII','XYL','Y','YDKN','YELP','YHOO','YORW','YRCW','YUM','YUME','Z','ZBRA','ZEN','ZEP','ZEUS','ZGNX','ZINC','ZION','ZIOP','ZIXI','ZLTQ','ZMH','ZNGA','ZOES','ZQK','ZTS','ZU','ZUMZ'


###########################
###   All NYSE Stocks  #####
###########################
,'DDD','MMM','WBAI','WUBA','EGHT','AHC','ATEN','AAC','AIR','AAN','ABB','ABT','ABBV','ANF','AGD','AWP','ACP','JEQ','AOD','ABM','AKR','ACN','ACCO','ATV','ATU','AYI','GOLF','ADX','PEO','AGRO','ADNT','ADT','ATGE','AAP','ADSW','WMS','ASIX','AAV','AVK','AGC','LCM','ACM','ANW','AEB','AED','AEG','AEH','AER','HIVE','AJRD','AET','AMG','AFL','MITT',
# 'MITT^A','MITT^B',
'AGCO','A','AEM','ADC','AL','APD','AYR','AKS',
# 'ALP^Q',
'ALG','AGI','ALK','AIN','ALB','AA','ALEX','ALX','ARE',
# 'ARE^D',
'AQN','BABA','Y','ATI','ALLE','AGN','ALE','AKP','ADS','AFB','AOI','AWF','AB','LNT','CBH','NCV','NCZ','ACV','NIE','NFJ','ALSN','ALL',
# 'ALL^A','ALL^B','ALL^C','ALL^D','ALL^E','ALL^F','ALL^G','ALLY','ALLY^A',
'AYX','ATUS','ATUS$','MO','ACH','AMBR','ABEV','AMC','AEE','AMRC','AMOV','AMX','AAT','AXL','ACC','AEO','AEP','AEL','AXP','AFG','AFGE','AFGH','AMH',
# 'AMH^D','AMH^E','AMH^F','AMH^G',
'AIG','AIG.WS','AMID','ARL','ARA','AWR','AMT','AVD','AWK','COLD','APU','AMP','ABC','ANFI','AMN','AMRX','AP','APH','AXR','AME',
# 'AFSI^A','AFSI^B','AFSI^C','AFSI^D','AFSI^E','AFSI^F',
'AFSS','AFST','AEUA','APC','ANDV','ANDX','AU','BUD','AXE','NLY',
# 'NLY^C','NLY^D','NLY^F','NLY^G',
'AMGP','AM','AR','ANTM','ANH',
# 'ANH^A','ANH^B','ANH^C',
'AON','APA','AIV',
# 'AIV^A',
'APY','ARI',
# 'ARI^C',
'APO',
# 'APO^A','APO^B',
'AIY','AFT','AIF','APLE','AIT','ATR','APTV','WTR','AQ','WAAS','ARMK','ABR',
# 'ABR^A','ABR^B','ABR^C',
'ARC','MT','ARCH','ADM','AROC','ARNC','ARCO','RCUS','ARD','ASC','AFC','ACRE','ARDC','ARES','ARES^A','AGX','ARGD','ARGO','ANET','AI','AI^B','AIC','AIW','AHH','ARR',
# 'ARR^A','ARR^B',
'AFI','AWI','ARW','AJG','APAM','ASA','ABG','ASX','ASGN','AHT',
# 'AHT^D','AHT^F','AHT^G','AHT^H','AHT^I',
'ASH','APB','ASPN','AHL',
# 'AHL^C','AHL^D',
'ASB','ASB^C','ASB^D','AC','AIZ','AIZP','AGO',
# 'AGO^B','AGO^E','AGO^F',
'AZN','HOME','T','TBB','ATTO','ATH','ATKR','AT','ATO','AUO','ATHM','ALV','AN','AZO','AVB','AGR','AVYA','AVY','AVH','AVA','AVP','AVX','EQH','AXTA','AXS',
# 'AXS^D','AXS^E',
'AZUL','AZRE','AZZ','BGS','BW','BGH','BMI','BHGE','BBN','BLL','BANC',
# 'BANC^C','BANC^D','BANC^E',
'BBVA','BBD','BBDO','BCH','BLX','BSMX','BSBR','BSAC','SAN',
# 'SAN^B','SAN^I.CL',
'CIB','BXS','BAC',
# 'BAC.WS.A','BAC.WS.B','BAC^A','BAC^B','BAC^C','BAC^D','BAC^E','BAC^I.CL','BAC^L','BAC^W','BAC^Y','BML^G','BML^H','BML^I','BML^J','BML^L',
'BOH','BMO','NTB','BK',
# 'BK^C',
'BNS','BKU','BCS',
# 'BCS^D',
'MCI','MPV','BNED','BKS','B','ABX','BAS','BAX','BTE','BBT',
# 'BBT^D','BBT^E','BBT^F','BBT^G','BBT^H',
'BFR','BBX','BCE','BZH','BDX','BDXA','BDC',
# 'BDC^B',
'BXE','BEL','BMS','BHE','BRK.A','BRK.B','BHLB','BERY','BBY','BSTI','BGCA','BHP','BBL','BIG','BH','BH.A','BHVN','BIO','BIO.B','BITA','BKH','BKHU','BKI','BSM','BB','BGIO','BJZ','BFZ','CII','BHK','HYT','BTZ','DSU','BGR','BDJ','EGF','FRA','BFO','BGT','BOE','BME','BAF','BKT','BGY','BKN','BTA','BIT','MUI','MNE','MUA','BPK','BKK','BBK','BBF','BYM','BFK','BTT','MEN','MUC','MUH','MHD','MFL','MUJ','MHN','MUE','MUS','MVT','MYC','MCA','MYD','MYF','MFT','MIY','MYJ','MYN','MPA','MQT','MYI','MQY','BNJ','BNY','BLH','BQH','BSE','BCX','BST','BSD','BUI','BLK','BGB','BGX','BSL','APRN','BCRH','BXG','BXC','BWP','BA','BCC','BCEI','BOOT','BAH','BWA','SAM','BXP','BXP^B','BSX','BOX','BYD','BPMP','BP','BPT','BRC','BHR','BHR^B','BDN','BWG','LND','BAK','BRFS','BPI','BGG','BFAM','BEDU','BSA','BSIG','EAT','BCO','BMY','BRS','BTI','BRX','BR','BKD','BAM','BBU','DTLA^','INF','BIP','RA','BEP','BRO','BF.A','BF.B','BRT','BC','BT','BPL','BKE','BVN','BBW','BG','BURL','BWXT','BY','CJ','GYB','PFH','CABO','CBT','COG','CACI','WHD','CADE','CAE','CAI',
# 'CAI^A',
'CAL','CRC','CWT','CALX','ELY','CPE',
# 'CPE^A',
'CBM','CPT','CCJ','CPB','CWH','GOOS','CM','CNI','CNQ','CP','CNNE','CAJ','CGC','CMD','COF',
# 'COF.WS','COF^C','COF^D','COF^F','COF^G','COF^H','COF^P',
'CSU','BXMT','CIC','CIC.U','CIC.WS','CMO','CMO^E','CRR','CAH','CRCM','CSL','KMX','CCL','CUK','CRS','CSV','CARS','CRI','CVNA','CSLT','CTLT','CTT','CAT','CATO','CBZ','CBL',
# 'CBL^D','CBL^E',
'CBO','IGR','CBRE','CBS','CBS.A','CBX','FUN','CDR',
# 'CDR^B','CDR^C',
'CE','CLS','CEL','CPAC','CX','CVE','CNC','CEN','CNP','EBR','EBR.B','CEPU','CCS','CTL','CDAY','CF','CGG','GIB','ECOM','CRL','CLDT','CMCM','CHGG','CHE','CC','CHMI',
# 'CHMI^A',
'CHK',
# 'CHK^D',
'CHKR','CHSP','CPK','CVX','CHS','CIM','CIM^A','CIM^B','DL','CEA','CHN','CGA','LFC','CHL','BORN','COE','SNP','XRF','ZNH','CHA','CHU','CYD','ZX','CMG','CHH','CBK','CB','CHT','CHD','CIEN','CI','XEC','CBB','CBB^B','CNK','CINR','CIR','CISN','CIT','BLW','C','C.WS.A',
# 'C^C','C^J','C^K','C^L','C^N','C^S',
'CFG','CIA','CIO','CIO^A','CVEO','CIVI','CLH','CCO','CBA           ','CEM','EMO','CTR','CLW','CLF','CLPR','CLX','CLD','CLDR','CMS',
'CMS^B',
'CMSA','CNA','CNHI','CNO','CEO','CNXM','CEIX','CNX','KOF','KO','CCE','CDE','FOF','INB','CNS','UTF','LDP','MIE','RQI','RNP','PSF','RFI','CFX','CL','CXE','CIF','CXH','CMU','CLNC','CLNS',
'CLNS^B','CLNS^D','CLNS^E','CLNS^G','CLNS^H','CLNS^I','CLNS^J',
'CXP','STK','CCZ','CMA','CMA.WS','FIX','CMC','CBU','CYH','CHCT','CIG','CIG.C','CBD','SBS','ELP','CCU','CODI',
# 'CODI^A','CODI^B',
'CMP','CRK','CAG','CXO','CCM','CNDT','COP','CCR','ED','STZ','STZ.B','CSTM','TCS','CBPX','CLR','VLRS','CVG','CTB','CPS','CPA','CLB','CXW','CLGX','CORR','CORR^A','CPLG$','COR','GLW','CAAP','GYC','CCT','OFC','CZZ','CMRE',
# 'CMRE^B','CMRE^C','CMRE^D','CMRE^E',
'COTV','COT','COTY',
# 'CFC^B.CL',
'CUZ','CVA','CPF','CPL','CR','CRD.A','CRD.B','BAP','CS','CPG','CEQP','CRH','CRT','CAPL','CCI',
# 'CCI^A',
'CCK','CRY','CSS','CTS','CUBE','CUB','CFR',
# 'CFR^A',
'CULP','CMI','CURO','CW','SRF','SRV','SZC','CUBI',
# 'CUBI^C','CUBI^D','CUBI^E','CUBI^F',
'CUBS','CVI','UAN','CVRR','CVS','CELP','CYS',
# 'CYS^A','CYS^B',
'DHI','DAN','DHR','DAC','DQ','DRI','DAR','DVA','DCP',
# 'DCP^B',
'DCT','DDR',
# 'DDR^A','DDR^J','DDR^K',
'DF','DECK','DE','DEX','DDF','DKL','DK','DVMT','DLPH','DAL','DLX','DNR','DESP','DKT','DB','DXB','DVN','DHX','DHT','DEO','DO','DRH','DSX','DSX^B','DSXN','DKS','DBD','DLR',
# 'DLR^C','DLR^G','DLR^H','DLR^I','DLR^J',
'DDS','DDT','DIN','DPLO','DFS','DHCP','DNI','DLB','DG','DM','D','DCUD','DRUA','DPZ','UFS','DCI','DFIN','LPG','DSL','DBL','PLOW','DEI','DOV','DDE','DVD','DWDP','DPS','RDY','DRD','DCF','DHF','DMB','DSM','LEO','DRQ','DS',
# 'DS^B','DS^C','DS^D',
'DSW','DTE','DTJ','DTQ','DTV','DTW','DTY','DCO','DPG','DSE','DNP','DTF','DUC','DUK','DUKH','DRE','DNB','DXC','DXC$','DY','DLNG',
# 'DLNG^A',
'DX',
# 'DX^A','DX^B','DD^A','DD^B',
'ELF','SSP','EGIF','EXP','ECC','ECCA','ECCB','ECCX','ECCY','ESTE','DEA','EGP','EMN','KODK','KODK.WS','KODK.WS.A','ETN','ETV','ETW','EV','EOI','EOS','EFT','EFL','EFF','EHT','ETX           ','EOT','EVN','ETJ','EFR','EVF','EVG','EVT','ETO','EXD','ETG','ETB','ETY','EXG','ECT','ECR','ECL','EC','EIX','EDR','EW','EHIC',
'EP^C',
'EE','EGO','ELVT','LLY','ELLI','EFC','EARN','AKO.A','AKO.B','ERJ','EME','EEX','EMES','EBS','EMR','ESRT','EIG','EDN','ENBL','EEQ','EEP','ENB','ENBA','ECA','EHC','EXK','NDRO','ENIA','ENIC','EOCC','EGN','ENR','EPC','ETE','ETP','ETP^C','ERF','ENS','EGL','E','ENLK','ENLC','EBF','ENVA','NPO','ESV','ETM','EAB','EAE','EAI','ETR','ELC','ELJ','ELU','EMP','ENJ','ENO','EZT','EPD','EVC','ENV','EVHC','EVA','ENZ','EOG','EPE','EPAM','EPR','EPR^C','EPR^E','EPR^G','EQT','EQGP','EQM','EFX','EQNR','EQC','EQC^D','ELS','EQR','EQS','ERA','EROS','ESE','ESNT','ESS','EL','ESL','ETH','EURN','EEA','EVR','RE','EVRI','ES','EVTC','EVH','AQUA','XAN','XAN^C','EXC','EXPR','STAY','EXTN','EXR','XOM','FNB','FNB^E','FN','FDS','FICO','FMSA','SFUN','FPI','FPI^B','FBK','FFG','FCB','AGM',
# 'AGM.A','AGM^A','AGM^B','AGM^C',
'FRT',
# 'FRT^C',
'FSS','FII','FMN','FDX','RACE','FGP','FOE','FG','FG.WS','FCAU','FBR','FNF','FIS','FMO','FAF','FBP','FCFS','FCF','FDC','FHN','FHN^A','FR','AG','FRC',
'FRC^D','FRC^E','FRC^F','FRC^G','FRC^H',
'FFA','FMY','FDEU','FIF','FSD','FPF','FEI           ','FPL','FIV','FCT','FGB','FHY','FEO','FAM','FE','FIT','FPH','FBC','DFP','PFD','PFO','FFC','FLC','FLT','FND','FTK','FLO','FLS','FLR','FLY','FMC','FMX','FL','F','FELP','FCE.A','FOR','FTS','FTV','FTAI','FSM','FBHS','FET','FBM','FCPT','FEDU','FNV','FC','FSB','BEN','FT','FI','FCX','FMS','FDP','RESI','FRO','FSIC','FCN','FTSI','FF','GCV',
# 'GCV^B','GDV','GDV^A','GDV^D','GDV^G',
'GAB',
# 'GAB^D','GAB^G','GAB^H','GAB^J',
'GGZ','GGZ^A','GGT','GGT^B','GGT^E','GUT','GUT^A','GUT^C','GFA','GCAP','GBL','GNT','GNT^A','GME','GPS','GDI','IT','GLOG','GLOG^A','GLOP','GLOP^A','GLOP^B','GTES','GATX','GMTA','GZT','GCP','GNK','GNRT','GNRC','GAM','GAM^B','BGC','GD','GE','GIS','GM','GM.WS.B','GCO','GWR','GEL','GEN','GNE','GNE^A','G','GPC','GNW','GEO','GPRK','GPJA','GGB','GTY','GGP','GGP^A','GIG','GIL','GLT','GKOS','GSK','BRSS','CO','GMRE','GMRE^A','GNL','GNL^A','GLP','GPN','GSL','GSL^B','GLOB','GMED','GMS','GNC','GDDY','GOL','GFI','GG','GSBD','GS',
# 'GS^A','GS^B','GS^C','GS^D','GS^J','GS^K','GS^N',
'GER','GMZ','GRC','GPX','GGG','EAF','GHM','GHC','GPT','GPT^A','GVA','GPMT','GRP.U','GPK','GTN','GTN.A','AJX','AJXA','GXP','GWB','GDOT','GBX','GHL','GHG','GEF','GEF.B','GFF','GPI','GRUB','PAC','ASR','AVAL','SUPV','TV','GTT','GSH','GES','GGM','GPM','GOF','GBAB','GWRE','HRB','FUL','HAE','HK','HK.WS','HAL','HYH','HBB','HBI','HASI','HOG','HMY','HRS','HSC','HHS','HGH','HIG','HIG.WS','HVT','HVT.A','HE','HE^U','HCHC','HCA','HCI','HCP','HDB','HR','HTA','HL','HL^B','HEI','HEI.A','HLX','HP','HLF','HRI','HCXZ','HTGC','HTGX','HRTG','HT','HT^C','HT^D','HT^E','HSY','HTZ','HES','HES^A','HESM','HPE','HXL','HF','HCLP','HFRO','HPR','HIW','HIL','HI','HRC','HTH','HGV','HLT','HNI','HMLP','HMLP^A','HEP','HFC','HD','HMC','HON','HMN','HZN','HTFA','HRL','HOS','HST','HLI','HOV','HHC','HPQ','HRG','HSBC','HSBC^A','HSEA.CL','HSEB.CL','HMI','HNP','HUBB','HUBS','HBM','HBM.WS','HUD','HPP','HGT','HUM','HCFT','HCFT^A','HII','HUN','HUYA','H','HY','IAG','IBN','IDA','IEX','IDT','ITW','IMAX','ICD','IHC','IRT','IFN','IBA','INFY','HIFR','ING','ISF','ISG','IR','NGVT','INGR','IIPR','IIPR^A','IPHI','INSI','NSP','INSP','IBP','INST','ITGR','I','ICE','IHG','IBM','IFF','IGT','IP','INSW','IPG','IPL^D','INXN','IPI','XON','IVC','VBF','VCV','VTA','IHIT','IHTA','VLT','IVR',
# 'IVR^B','IVR^C','IVR^A',
'OIA','VMO','VKQ','VPV','IVZ','IQI','VVR','VTN','VGM','IIM','ITG','IRET','IRET^C','NVTA','INVH','IO','IQV','IRM','IRS','ICL','STAR',
# 'STAR^D','STAR^G','STAR^I',
'ITCB','ITUB','ITT','IVH','JPM',
# 'JPM.WS','JPM^A','JPM^B','JPM^E','JPM^F','JPM^G','JPM^H',
'JAX','JILL','JCP','SJM','JBL','JEC','JAG','JHX','JHG','JOF','JBGS','JEF','JELD','JCAP',
# 'JCAP^B',
'JT','JKS','JMP','JMPB','JMPD','JBT','BTO','HEQ','JHS','JHI','HPF','HPI','HPS','PDT','HTD','HTY','JW.A','JW.B','JNJ','JCI','JONE','JLL','JMEI','JNPR','JP','JE',
# 'JE^A',
'LRN','KAI','KDMN','KAMN','KSU',
# 'KSU^',
'KS','KAR','KED','KYE','KMF','KYN','KYN^F','KB','KBH','KBR','KAP','FRAC','K','KEM','KMPA','KMPR','KMT','KW','KEN','KEG','KEY','KEY^I','KEYS','KRC','KRP','KMB','KIM',
# 'KIM^I','KIM^J','KIM^K','KIM^L','KIM^M',
'KMI',
# 'KMI^A',
'KND','KFS','KGC','KEX','KL','KRG','KKR','KKR^A','KKR^B','KIO','KREF','KMG','KNX','KNL','KNOP','KN','KSS','PHG','KOP','KEP','KF','KFY','KOS','KRA','KR','KRO','KT','KYO','LB','SCX','LLL','LQ','LH','LADR','LW','LCI','LPI','LVS','LHO','LHO^I','LHO^J','LTM','LDF','LGI','LAZ','LOR','LZB','LCII','LFGR','LEA','LEE','LGC',
# 'LGC.U','LGC.WS',
'LM','LMHA','LMHB','LEG','JBK','KTH','KTN','KTP','LDOS','LEJU','LC','LEN','LEN.B','LII','LHC','LHC.U','LHC.WS','LXP','LXP^C','LPL','USA','ASG','LBRT','LPT','LSI','LITB','LNC','LNC.WS','LNN','LN','LKM','LGF.A','LGF.B','LAD','LAC','LYV','LYG','SCD','LMT','L','LOMA','LPX','LOW','LXU','LKSD','LTC','LUB','LL','LXFR','LXFT','LDL','WLH','LYB','MTB','MTB.WS','MTB^','MTB^C','MDC','MHO','MAC','CLI','MFD','MGU','MIC','BMA','M','MCN','MSP','MMP','MGA','MX',
# 'MH^A','MH^C','MH^D',
'MHLA','MHNC','MAIN','MMD','MNK','MZF','MANU','MTW','MN','MAN','MFC','MRO','MPC','MMI','MCS','MRIN','MPX','HZO','MKL','VAC','MMC','MLM','MAS','DOOR','MTZ','MA','MTDR','MTRN','MATX','MLP','MAXR','MMS','MXL','MBI','MKC','MKC.V','MDR','MCD','MUX','MCK','MDU','MTL','MTL^','MRT','MPW','MED','MCC','MCV','MCX','MDLQ','MDLX','MDLY','MD','MDT','MRK','MCY','MDP','MTH','MTOR',
# 'MER^K','MER^P.CL',
'PIY','MTR','MSB','MEI','MET','MET^A','MCB','MTD','MXE','MXF','MFA','MFA^B','MFO','MFCB','MCR','MGF','MIN','MMT','MFM','MFV','MTG','MGP','MGM','KORS','MFGP','MAA','MAA^I','MSL','MPO','MCRN','MLR','HIE','MTX','MP^D','MG','MUFG','MIXT','MFG','MBT','MODN','MOD','MC','MHK','MOH','TAP','TAP.A','MNR','MNR^C','MON','MCO','MOG.A','MOG.B','MS',
# 'MS^A','MS^E','MS^F','MS^G','MS^I','MS^K',
'APF','CAF','MSD','EDD','MSF','IIF','MOSC','MOSC.U','MOSC.WS','MOS','MSI','MOV','MPLX','MRC','ICB','HJV','MSA','MSM','MSCI','MSGN','MLI','MWA','MUR','MUSA','MVO','MVC','MVCD','MYE','MYOV','NBR',
# 'NBR^A',
'NC','NTP','NTEST',
# 'NTEST.A','NTEST.B','NTEST.C',
'NBHC','NFG','NGG','NHI','NOV','NPK','NNN','NNN^E','NNN^F','SID','NSA',
# 'NSA^A',
'NSM','NGS','NGVC','NRP','NTZ','NLS','NCI','NVGS','NNA','NM','NM^G','NM^H','NAP','NMM','NAV','NAV^D','NCS','NCR','NP','NNI','NPTN','NETS','NVRO','HYB','GF','NWHM','IRL','NEWM','NMFC','EDU','NEWR','NRZ','SNR','NWY','NYCB','NYCB^A','NYCB^U','NYRT','NYT','NWL','NFX','NJR','NEU','NEM','NR','NEXA','NXRT','NHF','NEP','NEE',
# 'NEE^I','NEE^J','NEE^K','NEE^Q','NEE^R',
'NGL',
# 'NGL^B','NMK^B','NMK^C',
'NLSN','NKE','NINE','NI','NL','NOAH','NE','NBL','NBLX','NOK','NOMD','NMR','OSB','NAO','NAT','JWN','NSC','NOA','NRT','NOC','NRE','NWN','NWE','NCLH','NVS','NVO','DNOW','NRG','NYLD','NYLD.A','NUS','NUE','NS','NS^A','NS^B','NS^C','NSH','NSS','NTR','JMLP','NVG','NUV','NUW','NEA','NAZ','NBB','NBD','NKX','NCB','NCA','NAC','NTC','JCE','JCO','JQC','JDD','DIAX','JEMD','JMF','NEV','JFR','JRO','NKG','JGH','JHA','JHY','JHD','JHB','NXC','NXN','NID','NMY','NMT','NUM','NMS','NOM','JLS','JMM','NHA','NZF','NMZ','NMI','NJV','NXJ','NRK','NYV','NNY','NAN','NNC','NUO','NPN','NQP','JPC','JPS','JPT','JPI','NAD','JRI','JRS','BXMX','SPXX','NIM','NXP','NXQ','NXR','NSL','JSD','JTD','JTA','NTX','NPV','NIQ','JMT','NVT','NVR','OAK','OAK^A','OSLE','OMP','OAS','OBE','OXY','OII','OZM','OCIP','OCN','OFG','OFG^A','OFG^B','OFG^D','OGE','OIBR.C','OIS','ODC','ORI','OLN','OHI','OMC','OMN','ONDK','OGS','OLP','OMAD','OMAD.U','OMAD.WS','OMF','OKE','ONE','OOMA','OPY','ORCL','ORAN','OA','ORC','OEC','ORN','IX','ORA','OSK','OR','OUT','OSG','OMI','OC','OI','OXM','ROYT','PCG','PKG','PAGS','PANW','PAM','P','PHX','PARR','PAR','PGRE','PKE','PK','PKD','PH','PE',
# 'PRE^F','PRE^G','PRE^H','PRE^I',
'PRTY','PAYC','PBF','PBFX','BTU','PSO','PEB','PEB^C','PEB^D','PBA','PGH','PEI','PEI^B','PEI^C','PEI^D','PFSI','PMT','PMT^A','PMT^B','PAG','PNR','PEN','PFGC','PKI','PBT','PRT','PRGO','PRSP$','PTR','PBR','PBR.A','PFE','PGTI','PHH','PM','PSX','PSXP','FENG','DOC','PDM','PIR','PCQ','PCK','PZC','PCM','PTY','PCN','PCI','PDI','PGP','PHK','PKO','PFL','PFN','PMF','PML','PMX','PNF','PNI','PYN','RCS','PF','PNW','PES','PHD','PHT','MAV','MHI','PXD','PJC','PBI','PBI^B','PVTL','PJT','PAA','PAGP','PLNT','PLT','PAH','AGS','PHI','PNC','PNC.WS','PNC^P','PNC^Q','PNM','PII','POL','POR','PKX','POST','PPDF','PPG','PPX','PPL','PYS','PYT','PQG','PX','PDS','APTS','PBH','PVG','PRI','PGZ','PRA','PG','PGR','PLD','PUMP','PRO','PBB','PB','PRLB','PFS','PJH','PRH','PRU','GHY','PUK','PUK^','PUK^A','ISD','PSB',
# 'PSB^U','PSB^V','PSB^W','PSB^X','PSB^Y',
'TLK','PEG','PSA',
# 'PSA^A','PSA^B','PSA^C','PSA^D','PSA^E','PSA^F','PSA^G','PSA^U','PSA^V','PSA^W','PSA^X','PSA^Y','PSA^Z',
'PHM','PSTG','PCF','PMM','PIM','PMO','PPT','PVH','PZN','QTWO','QEP','QGEN','QTS','QTS^A','QUAD','KWR','QCP','NX','PWR','QTM','QD','DGX','QES','QHC','QUOT','CTAA','CTBB','CTDD','CTU','CTV','CTW','CTX','CTY','CTZ','RRD','RDN','RL','RPT','RPT^D','RRC','RNGR','RJF','RYAM','RYAM^A','RYN','RTN','RMAX','RLGY','O','RHT','RLH','RWT','RBC','RWGE','RWGE.U','RWGE.WS','REG','RM','RF',
# 'RF^A','RF^B',
'RGS','RGA','RZA','RZB','RS','RENX','RELX','RNR',
# 'RNR^C','RNR^E',
'SOL','RENN','RSG','RMD','REN           ','RFP','QSR','RPAI','REVG','REV','REX','REXR','REXR^A','REXR^B','RXN','RXN^A','RH','RMP','RNG','RIO','RBA','RAD',
# 'RMPL^',
'RIV','OPP','RLI','RLJ','RLJ^A','RRTS','RHI','ROK','COL','RCI','ROG','ROL','ROP','RST','RDC','RY','RY^T','RBS','RBS^S','RCL','RDS.A','RDS.B','RGT','RMT','RVT','RES','RPM','RSPP','RTEC','RYB','R','RYI','RHP','SPGI','SBR','SB','SB^C','SB^D','SFE','SAFE','SAIL','CRM','SMM','SBH','SJT','SN','SD','SDT','SDR','PER','SNY','SC','SOV^C','SAP','SAB','SAR','SSL','BFS','BFS^C','BFS^D','SCG','SLB','SNDR','SWM','SAIC','SALT','SLTB','SBBC','SBNA','STNG','SMG','KMM','KTF','KST','KSM','SE','SA','CKH','SMHI','SDRL','SDLP','SEE','SSW',
# 'SSW^D','SSW^E','SSW^G','SSW^H',
'SSWA','SSWN','SEAS','JBN','JBR','WTTR','SEM','SGZA','SEMG','SMI','SRE',
# 'SRE^A',
'SEND','ST','SXT','SQNS','SRG','SRG^A','SCI','SERV','NOW','SHAK','SJR','SHLX','SHW','SHG','SFL','SHOP','SSTK','SBGL','SIG','SBOW','SPG','SPG^J','SSD','SHI','SITE','SIX','SJW','SKM','SKX','SLG','SLG^I','SM','SFS','SMAR','SNN','AOS','SNAP','SNA','IPOA','IPOA.U','IPOA.WS','SQM','SOGO','SOI','SAH','SON','SNE','BID','SOR','SJI','SJIU','SXE',
# 'SCE^G','SCE^H','SCE^J','SCE^K','SCE^L',
'SO','SOJA','SOJB','SOJC','SCCO','LUV','SWX','SWN','SPA','SPE','SPE^B','SEP','SPB           ','TRK','SR','SPR','SAVE','SMTA$','SRC','SRC$','SRC^A','SPOT','SRLP','S','SPXC','FLOW','SQ','JOE','STAG','STAG^B','STAG^C','SSI','SMP','SXI','SWJ','SWK','SWP','STN','SGU','SRT','STWD','STT',
# 'STT^C','STT^D','STT^E','STT^G','SPLP','SPLP^A',
'SCS','SCA','SCM','SCL','STE','STL','STL^A','STC','SF','SF^A','SFB','STM','EDF','EDI','STON','SRI','STOR','GJH','GJO','GJS','SYK','RGR','SPH','SMFG','INN','INN^D','INN^E','SUM','SMLP','SUI','SLF','SXCP','SXC','SU','STG','SUN','SHO','SHO^E','SHO^F','STI','STI.WS.A','STI.WS.B','STI^A','SPN','SUP','SVU','SLD','SLDA','SLDD','SWZ','SWCH','SYF','SNX','SNV','SNV^C','GJP','GJR','GJT','GJV','SYY','SYX','DATA','TAHO','TLRD','TWN','TSM','TAL','TEGP','TEP','TALO','SKT','TPR','NGLS^A','TRGP','TGT','TARO','TTM','TCO','TCO^J','TCO^K','TMHC','TCP','TCF','TCF.WS','TCF^D','TSI','TEL','TISI','FTI','TECK','TK','TGP',
# 'TGP^A','TGP^B','TOO','TOO^A','TOO^B','TOO^E',
'TNK','GCI','TGNA','TRC','HQH','THQ','HQL','THW','TDOC','TLRA','TEO','TI','TI.A','TDY','TFX','VIV','TEF','TDA','TDE','TDI','TDJ','TDS','TU','TDF','EMF','TEI','GIM','TPX','TS','THC','TNC','TEN','TVC','TVE','TDC','TER','TEX','TX','TRNO','TTI','TEVA','TPL','TGH','TXT','AES','BX','CEE','SCHW','SCHW^C','SCHW^D','COO','GRX','GRX^A','GRX^B','GDL','GDL^C','THG','THGA','MSG','RUBI','TRV','VAM','TMO','THR','TPRE','TSLF','TCRX','TCRZ','TRI','THO','TDW','TDW.WS.A','TDW.WS.B','TIER','TIF','TLYS','TSU','TWX','TKR','TMST','TWI','TJX','TOL','TR','BLD','TMK','TMK^C','TTC','TD','NDP','TYG','NTG','TTP','TPZ','TOT','TSS','TOWR','TSQ','TM','TPGE','TPGE.U','TPGE.WS','TPGH',
# 'TPGH.U','TPGH.WS',
'TRTX','TSLX','TAC','TRP','TCI','TDG','TLP','RIG','TGS','TRU','TVPT','TREC','TG','THS','TREX','TY','TY^','TPH','TCAP','TCCA','TCCB','TRCO','TNET','TRN','TSE','TPVG','TPVY','GTS','TRTN','TGI','TROX','TBI','TNP',
# 'TNP^B','TNP^C','TNP^D','TNP^E',
'TUP','TKC','TPB','TRQ','TPC','TWLO','TWTR','TWO',
# 'TWO^A','TWO^B','TWO^C',
'TYL','TSN','USB',
# 'USB^A','USB^H','USB^M','USB^O',
'USPH','SLCA','UBS','UDR','UGI','UGP','UMH',
# 'UMH^B','UMH^C','UMH^D',
'UA','UAA','UFI','UNF','UN','UL','LTN',
# 'LTN.U','LTN.WS','LTN~',
'UNP','UIS','UNT','UAL','UMC','UPS','URI','USM','UZA','UZB','UZC','X','UTX','UNH','UTL','UNVR','UVV','UHT','UHS','UVE','UTI','UNM','UE','UBA','UBP',
# 'UBP^G','UBP^H',
'USFD','USAC','USNA','USDP','USG','BIF','VFC','EGY','MTN','VALE','VRX','VLO','VLP','VHI','VR',
# 'VR^A','VR^B',
'VLY','VLY.WS','VLY^A','VLY^B','VMI','VVV','VAR','VGR','VVC','VEC','VEDL','VEEV','VNTR','VTRB','VTR','VER','VER^F','PAY','VRTV','VZ','VZA','VET','VRS','VSM','VVI','VICI','VCO','VNCE','VIPS','ZTR','VGI','ZF','V','VSH','VPG','VSTO','DYNC','VST','VST.WS.A','VSI','VSLR','VMW','VOC','VCRA','VG','VNO',
# 'VNO^K','VNO^L','VNO^M',
'VJET','IAE','IHD','VOYA','IGA','IGD','IDE','IID','IRR','PPR','VMC','WTI','WPC','WRB',
# 'WRB^B','WRB^C','WRB^D','WRB^E',
'GRA','GWW','WNC','WBC','WDR','WAGE','WD','WMT','DIS','HCC','WPG',
# 'WPG^H','WPG^I',
'WRE','WCN','WM','WAT','WSO','WSO.B','WTS','W','WFT','WBS',
# 'WBS^F',
'WEC','WTW','WRI','WMK','WBT','WCG','WFC',
# 'WFC.WS','WFC^J','WFC^L','WFC^N','WFC^O','WFC^P','WFC^Q','WFC^R','WFC^T','WFC^V','WFC^W','WFC^X','WFC^Y','WFE^A',
'EOD','WELL',
# 'WELL^I',
'WAIR','WCC','WST','WR','WAL','WALA','WEA','TLI','EMD','GDO','EHI','HIX','HIO','HYI','SBI','IGI','PAI','MMU','WMC','DMO','MTT','MHF','MNP','GFY','WIW','WIA','WGP','WES','WU','WAB','WLK','WLKP','WMLP','WBK','WRK','WHG','WEX','WY','WGL','WPM','WHR','WTM','WSR','WLL','WOW','WRD','WMB','WPZ','WSM','WGO','WIT','WNS','WWW','WF','WK','INT','WWE','WP','WOR','WPP','WPX','WPXP','WH$','WYN','WYND$','XFLT','XHR','XRM','XRX','XIN','XL','XOXO','XPO','XYL','AUY','YELP','YEXT','YGE','YRD','YPF','YUMC','YUM','ZAYO','ZEN','ZBH',
# 'ZB^A',
# 'ZB^G',
# 'ZB^H',
'ZBK','ZOES','ZTS','ZTO','ZUO','ZYME',

##########################################
# Index Stocks
'SPY','IWM','QQQ','ASHR','INDA'


]


now=datetime.datetime.now()

def contentfilter():
    timer=datetime.datetime.now()
    with requests.Session() as c:
        map=['']
        stocks=stocklist

        for u in stocks:
            u=random.choice(stocks)
            try:
                time.sleep(60)
                url='htt'+'ps://news.google.com/news/rss/search/section/q/'+u+'/'+u+'?hl=en&gl=US&ned=us'
                x=c.get(url)
                x=BeautifulSoup(x.content)
                titles=x.find_all('title')
                pubdate=x.find_all('lastbuilddate')+x.find_all('pubdate')
                for p,t in zip(pubdate,titles):
                    # Assemble our Output Variable
                    pub=str(p.text)
                    info=str(t.text)
                    if info.find(';')>0:
                        info=info[:info.find(';')]

    				###Dynamically determining stock based on text. Assuming results may not match original search keyword
                    stock=info[info.find('(')+1:info.find(')')].replace('NYSE:','').replace('NASDAQ:','').replace('NYSE ','').replace(':','').replace(' ','')
                    grab=info


                    # Define which bank is making the comment

                    # Generic Cases
                    bank='Other'
                    if 'Analysts' in grab:
                        bank='Analysts'
                    if 'Brokerages' in grab:
                        bank='Brokerages'
                    if 'Price Target Outlook:' in grab:
                        bank='Price Target Outlook:'
                    if 'Avg. Price Target Review:' in grab:
                        bank='Avg. Price Target Review:'
                    if 'Avg. Price Target Recap:' in grab:
                        bank='Avg. Price Target Recap:'
                    if 'Avg. Price Target Opinion:' in grab:
                        bank='Avg. Price Target Opinion:'
                    if 'Consensus Target Price' in grab:
                        bank='Consensus Target Price'
                    if 'Price Target Recommendation:' in grab:
                        bank='Price Target Recommendation:'
                    if 'Price Target Summary:' in grab:
                        bank='Price Target Summary:'

                # Specific Banks or Data Market Information Sites
                    if 'Barclays' in grab:
                        bank='Barclays'
                    if 'Goldman Sachs' in grab:
                        bank='Goldman Sachs'
                    if 'Och-Ziff' in grab:
                        bank='Och-Ziff'
                    if 'Jeffries' in grab:
                        bank='Jeffries'
                    if 'Bank of America' in grab:
                        bank='Bank of America'
                    if 'Piper Jaffray' in grab:
                        bank='Piper Jaffray'
                    if 'Royal Bank of Canada' in grab:
                        bank='Royal Bank of Canada'
                    if 'Cantor Fitzgerald' in grab:
                        bank='Cantor Fitzgerald'
                    if 'Citigroup' in grab:
                        bank='Citigroup'
                    if 'Zacks:' in grab:
                        bank='Zacks:'
                    if 'Wells Fargo' in grab:
                        bank='Wells Fargo & Co'
                    if 'Wolfe Research' in grab:
                        bank='Wolfe Research'
                    if 'UBS' in grab:
                        bank='UBS'
                    if 'Telsey Advisory Group' in grab:
                        bank='Telsey Advisory Group'
                    if 'SunTrust Banks' in grab:
                        bank='SunTrust Banks'
                    if 'Stifel Nicolaus' in grab:
                        bank='Stifel Nicolaus'
                    if 'Oppenheimer' in grab:
                        bank='Oppenheimer'
                    if 'Morgan Stanley' in grab:
                        bank='Morgan Stanley'
                    if 'JPMorgan' in grab:
                        bank='JPMorgan'
                    if 'Credit Suisse' in grab:
                        bank='Credit Suisse'
                    if 'Baird' in grab:
                        bank='Baird'
                    if 'Susquehanna Banc' in grab:
                        bank='Susquehanna Banc'
                    if 'Canaccord Genuity' in grab:
                        bank='Canaccord Genuity'
                    if 'B. Riley' in grab:
                        bank='B. Riley'
                    if 'BMO Capital Markets' in grab:
                        bank='BMO Capital Markets'
                    if 'Raymond James' in grab:
                        bank='Raymond James'
                    if 'Deutsche Bank' in grab:
                        bank='Deutsche Bank'
                    if 'Scotiabank' in grab:
                        bank='Scotiabank'
                    if 'BWS Financial' in grab:
                        bank='BWS Financial'
                    if 'HC Wainwright' in grab:
                        bank='HC Wainwright'


    				# Save Initial Data to Raw File

    				# f = open('rawmarketmentions.txt'+str(now.month)+'-'+str(now.day)+'-'+str(now.year)+'-UnSelected.txt', 'a')
    				# f.write(grab+' | ' + pub +'\n')
    				# f.close()

    				## Begin filtering the data for model output
    				## First find $$$$
                    if grab.count('$') > 0:
                        targ=int(0)
                        targ=grab.find('$')
                        value=grab[targ+1:targ+5]
                        ######## now you have the targeted value, time to clean up
                        if value[2:len(value)].count('-')>0:
                            value=value.replace('-','')
                        if value.endswith('.'):
                            value=value.replace('.','')
                        value=value.replace(' ','')
                        value=value.replace(',','')
                        value=value.replace('k','000')
                        value=value.replace('m','000000')
                        value=value.replace('M','000000')
                        value=value.replace('b','000000000')
                        value=value.replace('B','000000000')
                        value=value.replace('T','')
                        value=value.replace(' ','')
                        value=value.replace('in','')
                        value=value.replace('i','')
                        # rhprice=float(robinhoodprice(u))
                        # if bcprice == None:
                        #     bcprice=0
                        # if rhprice == None:
                        #     rhprice=0
                        #     bcprice=0
                        # if value == None:
                        #     value=0
                        #
                        # if bcprice*.9 <= rhprice <= bcprice*1.1:
                        #     price=rhprice
                        # else:
                        #     price=0

                        try:
                            value=float(value)

                            # Only selecting stocks whose price is available and consistent between Barchart, Quandl, and Robinhood

                        except Exception as e:
                            print("------------------------------------")
                            print(e)
                            print(u)
                            print("failed to convert value to float with value of:")
                            print(value)
                            print("and grab:")
                            print(grab)
                            print()
                            print("------------------------------------")

                            value=0

                        # Only selecting stocks we have a very specific and defined price for
                        if value>0 and len(stock)<6:

                            try:
                                epsreference=yahooepspuller(stock)
                            except:
                                epsreference=None
                            try:
                                divyield=robinhooddivyield(stock)
                            except:
                                divyield=None
                            try:
                                yrlow=robinhood52low(stock)
                            except:
                                yrlow=None
                            try:
                                yrhigh=robinhood52high(stock)
                            except:
                                yrhigh=None
                            try:
                                fiveyrlow=quandl_five_yr_low(stock)
                            except:
                                fiveyrlow=None




                            # Find EPS callouts
                            if grab.find('EPS') >0 or grab.find('eps')>0 or grab.find('Earnings')>0 or grab.find('earnings') > 0:

                                qpe=round(price/float(value),2)
                                ape=round(price/float(epsreference),2)

                                ######Calling prices to ensure they are available upon fail
                                price=barchart(u)

                                #determine EPS growth rate
                                epsgrowth=(qpe*4-ape)/abs(ape)
                                targetprice=price+price*epsgrowth/8

                                # determine target price based on EPS growth ranges
                                if epsgrowth>=2:
                                    targetprice=price*2
                                if epsgrowth>=1 and epsgrowth<2:
                                    targetprice=price*1.2
                                if epsgrowth<1 and epsgrowth>=0:
                                    targetprice=price+(price*epsgrowth/8)
                                if epsgrowth>-1 and epsgrowth<0:
                                    targetprice=price*.8
                                if epsgrowth<=-1:
                                    targetprice=price/2

                                epsexpreturn=(targetprice-price)/price



                                if price*.1 < targetprice and price*10>targetprice:
        							#########################################################
        							##############  Database Connection   ###################
                                    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
                                    cur = conn.cursor()
        							# execute a statement
                                    cur.execute("INSERT INTO fmi.marketmentions (target, price, returns, ticker, note, date, q_eps, a_eps, report, q_pe,a_pe, divyield,bank,yrlow,yrhigh,fiveyrlow) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)", (targetprice,price,epsexpreturn,stock,grab,pub,value,epsreference,'earnings',qpe,ape,divyield,bank,yrlow,yrhigh,fiveyrlow))
                                    print("----------------------------")
                                    print("inserted value")
                                    conn.commit()
        							# close the communication with the PostgreSQL
                                    cur.close()
                                    conn.close()
                                    currenttime=datetime.datetime.now()-timer
                                    print("Stock "+str(stock)+" Occurred After "+str(currenttime)+" seconds")
                                    print("----------------------------")

                            # Find price target callouts
                            if grab.find('arget') > 0:
                                price=barchart(u)
                                predreturn=(value-price)/price
                                if predreturn>1 or predreturn<-.8:
                                    price=quandl_adj_close(u)
                                    predreturn=(value-price)/price
                                    if predreturn>1 or predreturn<-.8:
                                        price=googlefinancepricepull(u)
                                        predreturn=(value-price)/price

                                if price*.1 < value and price*10>value:
                                    #########################################################
                                    ##############  Database Connection   ###################
                                    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
                                    cur = conn.cursor()
                                    # execute a statement
                                    cur.execute("INSERT INTO fmi.marketmentions (target, price, returns, ticker, note, date, q_eps, a_eps, report, divyield,bank,yrlow,yrhigh,fiveyrlow) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)", (value,price,predreturn,stock,grab,pub,None,epsreference,'analyst',divyield,bank,yrlow,yrhigh,fiveyrlow))
                                    print("----------------------------")
                                    print("inserted value")
                                    conn.commit()
                                    # close the communication with the PostgreSQL
                                    cur.close()
                                    conn.close()
                                    currenttime=datetime.datetime.now()-timer
                                    print("Stock"+str(stock)+" Occurred After "+str(currenttime)+" seconds")
                                    print("----------------------------")

            except Exception as e:
                print("------------------------------------")
                print(e)
                print("Original Stock Name: "+u)
                print("Dynamic Stock Ticker: "+stock)
                print("failed with value of:")
                print(value)
                print("and grab of:")
                print(grab)
                print()
                print("------------------------------------")
                pass




contentfilter()
print('end')
