mylist = input('enter your list separated by comma')
mylist1 = [float(mylist.strip()) for mylist in mylist.split(',')]
mylist1.sort()
print(mylist1[-2])
