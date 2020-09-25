if __name__ == '__main__':
	import pandas as pd
	import logging
	from datetime import datetime

	logging.basicConfig(filename='transact.log',level=logging.DEBUG)
	id=0
	askbook=pd.read_csv("ask.csv")
	bidbook=pd.read_csv("bid.csv")
	askbook=askbook.sort_values(by=['price'],ignore_index=True)
	bidbook=bidbook.sort_values(by=['price'],ascending=False,ignore_index=True)
	#orders=pd.read_csv("orders.csv");
	#print(askbook.iloc[0])
	def showlob(askbook,bidbook):
		print("Ask Book \n")
		print(askbook)
		print("\n---------------------\n")
		print("Bid Book \n")
		print(bidbook)

	def limitorder_ask(askbook,bidbook):
		shares=int(input("Number of Shares : "))
		lp=float(input("Limit price : "))
		while True:
			if(bidbook.iloc[0,1] >= lp and shares <  bidbook.iloc[0,2]):
				logging.debug('sellLimit , {} , {} , {}'.format(bidbook.iloc[0,1],shares,datetime.now()))
				bidbook.at[0,'ask size']=bidbook.iloc[0,2]-shares
				shares=0
			elif bidbook.iloc[0,1] < lp:

				logging.debug('selllimit , {} , {} , {}'.format(lp,shares,datetime.now()))
				new={'id':id,'price':lp,'ask size':int(shares)}
				askbook=askbook.append(new,ignore_index = True)
				askbook=askbook.sort_values(by=['price'],ignore_index=True)
				shares=0
			else:
				logging.debug('sellLimit , {} , {} , {}'.format(bidbook.iloc[0,1],shares,datetime.now()))
				bidbook.at[0,'bid size']=bidbook.iloc[0,2]-shares
				shares=shares-bidbook.iloc[0,1]
				bidbook.drop([0],inplace=True)
				bidbook=bidbook.reset_index(drop=True)
			if shares==0:
				return askbook,bidbook



	def ask(askbook):
		shares=int(input("Number of Shares : "))
		while True:
			print(askbook.iloc[0,2])
			if askbook.iloc[0,2] > shares:
				logging.debug('buy , {} , {} , {}'.format(askbook.iloc[0,1],shares,datetime.now()))
				askbook.at[0,'ask size']=askbook.iloc[0,2]-shares
				shares=0
			else:
				logging.debug('buy , {} , {} , {}'.format(askbook.iloc[0,1],askbook.iloc[0,2],datetime.now()))
				shares=shares-askbook.iloc[0,2]
				askbook.drop([0],inplace=True)
				askbook=askbook.reset_index(drop=True)
			if shares==0:
				return askbook

	def limitorder_bid(askbook,bidbook):
		shares=int(input("Number of Shares : "))
		lp=float(input("Limit price : "))
		while True:
			if(askbook.iloc[0,1] <= lp and shares <  askbook.iloc[0,2]):
				logging.debug('BuyLimit , {} , {} , {}'.format(askbook.iloc[0,1],shares,datetime.now()))
				askbook.at[0,'ask size']=askbook.iloc[0,2]-shares
				shares=0
			elif askbook.iloc[0,1] > lp:

				logging.debug('Buylimit , {} , {} , {}'.format(lp,shares,datetime.now()))
				new={'id':id,'price':lp,'bid size':shares}
				bidbook=bidbook.append(new,ignore_index = True)
				bidbook=bidbook.sort_values(by=['price'],ascending=False,ignore_index=True)
				shares=0
			else:
				logging.debug('BuyLimit , {} , {} , {}'.format(bidbook.iloc[0,1],shares,datetime.now()))
				askbook.at[0,'ask size']=bidbook.iloc[0,2]-shares
				shares=shares-askbook.iloc[0,2]
				askbook.drop([0],inplace=True)
				askbook=askbook.reset_index(drop=True)
			if shares==0:
				return askbook,bidbook
				
	def bid(bidbook):
		shares=int(input("Number of Shares : "))
		while True:
			print(bidbook.iloc[0,2])
			if bidbook.iloc[0,2] > shares:
				logging.debug('sell , {} , {} , {}'.format(bidbook.iloc[0,1],shares,datetime.now()))
				bidbook.at[0,'bid size']=bidbook.iloc[0,2]-shares
				shares=0
			else:
				logging.debug('sell , {} , {} , {}'.format(bidbook.iloc[0,1],bidbook.iloc[0,2],datetime.now()))
				shares=shares-bidbook.iloc[0,2]
				bidbook.drop([0],inplace=True)
				bidbook=bidbook.reset_index(drop=True)
			if shares==0:
				return bidbook

	def CancelOrder(askbook,bidbook,id):
		if id in askbook.values:
			logging.debug('cancelask , {} , {}'.format(id,datetime.now()))
			askbook.drop(askbook[askbook['id']==id].index,inplace=True)
			askbook=askbook.reset_index(drop=True)
			if id in bidbook.values:
				logging.debug('cancelbid , {} , {}'.format(id,datetime.now()))
				bidbook.drop(bidbook[bidbook['id']==id].index,inplace=True)
				bidbook=bidbook.reset_index(drop=True)
		else:
			print("\nOrder Not Found \n")
		return askbook,bidbook

	id=int(input("Enter You id : "))
	while (True):
		print(" 1.Show Limit Order Book\n 2.Place Market Order \n 3.Place Limit Order \n 4.Cancel Order \n 5.exit \n")
		select=input()
		if(select=='1'):
			showlob(askbook,bidbook)
		elif select=='2':
			print("\n 1.Buy\n2.Sell\n")
			if int(input())==1:
				askbook=ask(askbook)
			else:
				bidbook=bid(bidbook)
		elif select=='3':
			print("\n 1.Buy\n2.Sell\n")
			if int(input())==1:
				askbook,bidbook=limitorder_bid(askbook,bidbook)
			else:
				askbook,bidbook=limitorder_ask(askbook,bidbook)
		elif select=='4':
			askbook,bidbook=CancelOrder(askbook,bidbook,id)
		elif select=='5':
			exit()
		else:
			print("OOPS...")
		print("\n-----------------------------------------------------\n")
