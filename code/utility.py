import pandas as pd
import logging
from datetime import datetime


class LOB_utility:
	logging.basicConfig(filename='transact.log',level=logging.DEBUG)
	askbook=pd.read_csv("ask.csv")
	bidbook=pd.read_csv("bid.csv")
	askbook=askbook.sort_values(by=['price'],ignore_index=True)
	bidbook=bidbook.sort_values(by=['price'],ascending=False,ignore_index=True)
	
	def showlob(self):
		print("Ask Book \n")
		print(self.askbook)
		print("\n---------------------\n")
		print("Bid Book \n")
		print(self.bidbook)

	def limitorder_ask(self):
		shares=int(input("Number of Shares : "))
		lp=float(input("Limit price : "))
		while True:
			if(self.bidbook.iloc[0,1] >= lp and shares <  self.bidbook.iloc[0,2]):
				logging.debug('sellLimit , {} , {} , {}'.format(self.bidbook.iloc[0,1],shares,datetime.now()))
				self.bidbook.at[0,'ask size']=self.bidbook.iloc[0,2]-shares
				shares=0
			elif self.bidbook.iloc[0,1] < lp:

				logging.debug('selllimit , {} , {} , {}'.format(lp,shares,datetime.now()))
				new={'id':id,'price':lp,'ask size':int(shares)}
				self.askbook=self.askbook.append(new,ignore_index = True)
				self.askbook=self.askbook.sort_values(by=['price'],ignore_index=True)
				shares=0
			else:
				logging.debug('sellLimit , {} , {} , {}'.format(self.bidbook.iloc[0,1],shares,datetime.now()))
				self.bidbook.at[0,'bid size']=self.bidbook.iloc[0,2]-shares
				shares=shares-self.bidbook.iloc[0,1]
				self.bidbook.drop([0],inplace=True)
				self.bidbook=self.bidbook.reset_index(drop=True)
			if shares==0:
				return 1



	def ask(self):
		shares=int(input("Number of Shares : "))
		while True:
			print(self.askbook.iloc[0,2])
			if self.askbook.iloc[0,2] > shares:
				logging.debug('buy , {} , {} , {}'.format(self.askbook.iloc[0,1],shares,datetime.now()))
				self.askbook.at[0,'ask size']=self.askbook.iloc[0,2]-shares
				shares=0
			else:
				logging.debug('buy , {} , {} , {}'.format(self.askbook.iloc[0,1],self.askbook.iloc[0,2],datetime.now()))
				shares=shares-self.askbook.iloc[0,2]
				self.askbook.drop([0],inplace=True)
				self.askbook=self.askbook.reset_index(drop=True)
			if shares==0:
				return 1

	def limitorder_bid(self):
		shares=int(input("Number of Shares : "))
		lp=float(input("Limit price : "))
		while True:
			if(self.askbook.iloc[0,1] <= lp and shares <  self.askbook.iloc[0,2]):
				logging.debug('BuyLimit , {} , {} , {}'.format(self.askbook.iloc[0,1],shares,datetime.now()))
				self.askbook.at[0,'ask size']=self.askbook.iloc[0,2]-shares
				shares=0
			elif self.askbook.iloc[0,1] > lp:

				logging.debug('Buylimit , {} , {} , {}'.format(lp,shares,datetime.now()))
				new={'id':id,'price':lp,'bid size':shares}
				self.bidbook=self.bidbook.append(new,ignore_index = True)
				self.bidbook=self.bidbook.sort_values(by=['price'],ascending=False,ignore_index=True)
				shares=0
			else:
				logging.debug('BuyLimit , {} , {} , {}'.format(self.bidbook.iloc[0,1],shares,datetime.now()))
				self.askbook.at[0,'ask size']=self.bidbook.iloc[0,2]-shares
				shares=shares-self.askbook.iloc[0,2]
				self.askbook.drop([0],inplace=True)
				self.askbook=self.askbook.reset_index(drop=True)
			if shares==0:
				return 1
				
	def bid(self):
		shares=int(input("Number of Shares : "))
		while True:
			print(self.bidbook.iloc[0,2])
			if self.bidbook.iloc[0,2] > shares:
				logging.debug('sell , {} , {} , {}'.format(self.bidbook.iloc[0,1],shares,datetime.now()))
				self.bidbook.at[0,'bid size']=self.bidbook.iloc[0,2]-shares
				shares=0
			else:
				logging.debug('sell , {} , {} , {}'.format(self.bidbook.iloc[0,1],self.bidbook.iloc[0,2],datetime.now()))
				shares=shares-self.bidbook.iloc[0,2]
				self.bidbook.drop([0],inplace=True)
				self.bidbook=self.bidbook.reset_index(drop=True)
			if shares==0:
				return 1

	def CancelOrder(self,id):
		if id in self.askbook.values:
			logging.debug('cancelask , {} , {}'.format(id,datetime.now()))
			self.askbook.drop(self.askbook[self.askbook['id']==id].index,inplace=True)
			self.askbook=self.askbook.reset_index(drop=True)
			if id in self.bidbook.values:
				logging.debug('cancelbid , {} , {}'.format(id,datetime.now()))
				self.bidbook.drop(self.bidbook[self.bidbook['id']==id].index,inplace=True)
				self.bidbook=self.bidbook.reset_index(drop=True)
		else:
			print("\nOrder Not Found \n")
		