if __name__ == '__main__':
	from utility import LOB_utility

	ob=LOB_utility()
	id=int(input("Enter You id : "))
	
	while (True):
		print(" 1.Show Limit Order Book\n 2.Place Market Order \n 3.Place Limit Order \n 4.Cancel Order \n 5.exit \n")
		select=input()
		if(select=='1'):
			ob.showlob()
		elif select=='2':
			print("\n 1.Buy\n2.Sell\n")
			if int(input())==1:
				ob.ask()
			else:
				ob.bid()
		elif select=='3':
			print("\n 1.Buy\n2.Sell\n")
			if int(input())==1:
				ob.limitorder_bid()
			else:
				ob.limitorder_ask()
		elif select=='4':
			ob.CancelOrder(id)
		elif select=='5':
			exit()
		else:
			print("OOPS...")
		print("\n-----------------------------------------------------\n")
