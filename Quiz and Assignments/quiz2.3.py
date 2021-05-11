mylist = input('enter your list separated by comma: ')
mylist1 = [float(mylist.strip()) for mylist in mylist.split(',')]
myset=set(mylist1)
mylist2 = list(myset)
if len(mylist1)>len(mylist2):
    print('The list provided contains duplicate values, here is the list without duplicate values:', mylist2)12
else: print('The list provided does not contain duplicate values')
