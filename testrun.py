import urllib2, json, time, thread, sys
CUR1name = 'LTC'# name of first currency.
CUR2name = 'BTC'# "	  second	"
CUR1amount = 10
CUR2amount = 0.1
lowerlimit = 0
scalefactor = 25
debug = True
def getjson():
	while 1:
	    try:
		jsondata = urllib2.urlopen("https://btc-e.com/api/2/" + CUR1name.lower() + "_" + CUR2name.lower() +  "/ticker").read()
		break
	    except:
		    print "Server Error"
		    time.sleep(10)
	return json.loads(jsondata) 
def getoption():
	while 1:
		try:
			option = raw_input()
			if option == 'scale':
				scalefactor = input("Change scale factor: ")
			elif option == 'debug':
				debug = input("New debug value: ")
			elif option == 'help':
				print "scale  - sets the sensitivity that controls how much to buy/sell"
				print "debug - Turns debug on or off. Must be 'True', 'False' or other python boolean"
			else:
				print "Invalid option"
		except:
			print "NaN"

def info():
	while 1:
		sys.stdout.write(updatetext)
		time.sleep(1)
		sys.stdout.write('\r')
		sys.stdout.flush()
def sellprice():
	return float(getjson()['ticker']["sell"]) 

def buyprice():
	return float(getjson()['ticker']["buy"])

def buy(wallet, amount, bprice):
	wallet[CUR1name] += amount
	wallet[CUR2name] -= amount * bprice
	return wallet    
def sell(wallet, amount, sprice):
	wallet[CUR1name] -= amount
	wallet[CUR2name] += amount * sprice
	return wallet
def getwallet():
	wallet = {}
	wallet[CUR1name] = CUR1amount
	wallet[CUR2name] = CUR2amount
	return wallet
    
def textbetween(str1,str2,text):# returns the text between str1 and str2 in text. This is usefull for parsing data.
	posstr1 = text.find(str1)
	posstr2 = text.find(str2)
	between = text[posstr1 + len(str1):posstr2]
	return between

def clearstd():
	sys.stdout.write('\r')
	sys.stdout.flush()

#setup the last prices
lastsale = buyprice()
lastbuy = sellprice()
lastdo = [lastbuy,lastsale] 
#define the wallet
wallet = getwallet()
#get the riskfactor all the time:
updatetext = ''
#thread.start_new_thread( getoption, () )
thread.start_new_thread( info, () )
#get initial total for reference
sprice = sellprice()
fetotal = wallet[CUR2name] + wallet[CUR1name] * sprice
while 1:
	bprice = buyprice()
	sprice = sellprice()
	donestuff = 0
	if bprice < lastdo[0] and bprice < lastdo[1]:
		#calculate decimal price drop
		decdown = abs(lastbuy / bprice) / 100
		#buy cur1 in relation to the price drop scale
		if (decdown * scalefactor) < 1:
			tobuy = (wallet[CUR2name] / bprice) * (decdown * scalefactor)

	    	else:
	        	tobuy = (wallet[CUR2name] / bprice) * 1

		#make sure we have enough
		if tobuy <= wallet[CUR2name] / bprice and tobuy >= lowerlimit:
			#and get new wallet values
			wallet = buy(wallet, tobuy, bprice)
			clearstd()
			print "[BUY] %.3f %s for %.6f %s."% (tobuy, CUR1name, bprice * tobuy, CUR2name)
			print "%s: %.3f\n%s: %.6f."% (CUR1name,  float(wallet[CUR1name]), CUR2name, float(wallet[CUR2name]))
			print "Total %s: %.6f"% (CUR2name, float(wallet[CUR2name]) + float(wallet[CUR1name]) * sprice)
			print "==========="# since TJ seems to love this so much.
			donestuff = 1
			lastbuy = bprice

		elif debug:
			clearstd()
			print "[DEBUG] Tried to buy %.3f %s for %.6f"%(tobuy, CUR1name, tobuy * bprice)

		lastdo = [bprice,sprice]
		if debug:
			clearstd()
			print "[DEBUG]Old buy price: \t%.6f Old sell price: \t%.6f"%(bpriceold,spriceold)
			print "[DEBUG]Last buy price: \t%.6f Last sell price: \t%.6f"%(lastbuy,lastsale)
			print "[DEBUG]Do buy price: \t%.6f Do sell price:\t%.6f"%(lastdo[0],lastdo[1])
			print "[DEBUG]Buy price: \t%.6f Sell price: \t%.6f"%(bprice,sprice)
        		print "[DEBUG] Fall: %.6f"% (decdown)

	if sprice > lastdo[1] and sprice > lastdo[0]:
		#calculate decimal price raise
		decraise = abs(lastsale / sprice) / 100
		#sell cur1 in relation to price raise scale
		if wallet[CUR1name] * (decraise * scalefactor) < 1:
			tosell = wallet[CUR1name] * (decraise * scalefactor)

	    	else:
	        	tosell = wallet[CUR1name] * 1

		if tosell <= wallet[CUR1name] and tosell >= lowerlimit:
			#and get new wallet values
			wallet = sell(wallet, tosell, sprice)
			lastsale = sprice
			print "[SELL] %.3f %s for %.6f %s."% (tosell, CUR1name, sprice * tosell, CUR2name)
			print "%s: %.3f\n%s: %.6f."% (CUR1name,  float(wallet[CUR1name]), CUR2name, float(wallet[CUR2name]))
			print "Total %s: %.6f"% (CUR2name, float(wallet[CUR2name]) + float(wallet[CUR1name]) * sprice)
			print "==========="# since TJ seems to love this so much.
			donestuff = 2

		elif debug:
			print "[DEBUG] Tried to sell %.3f %s for %.6f"%(tosell, CUR1name, tosell * sprice)

		lastdo = [bprice,sprice]
		if debug:
			print "[DEBUG]Old buy price:\t%.6f Old sell price:\t%.6f"%(bpriceold,spriceold)
			print "[DEBUG]Last buy price:\t%.6f Last sell price:\t%.6f"%(lastbuy,lastsale)
			print "[DEBUG]Do buy price:\t%.6f Do sell price:\t%.6f"%(lastdo[0],lastdo[1])
			print "[DEBUG]Buy price:\t%.6f Sell price:\t%.6f"%(bprice,sprice)
			print "[DEBUG] Raise: %.6f"% (decraise)

	bpriceold = bprice
	spriceold = sprice
	f = open ("moneylog.csv","a")
	if donestuff == 1:
		f.write("%s, %s, %s, %s, %s, %s\n"% (sprice, bprice, wallet[CUR1name], wallet[CUR2name], tobuy, '0'))

	elif donestuff == 2:
		f.write("%s, %s, %s, %s, %s, %s\n"% (sprice, bprice, wallet[CUR1name], wallet[CUR2name], '0', tosell))
	else:
		f.write("%s, %s, %s, %s, %s, %s\n"% (sprice, bprice, wallet[CUR1name], wallet[CUR2name], '0', '0'))
	totald = wallet[CUR2name] + (wallet[CUR1name] * sprice)# update totald
	nowTotal = CUR2amount + (CUR1amount * sprice)
	updatetext = " Profit: %.6f"% (totald - nowTotal)
	time.sleep(10)


