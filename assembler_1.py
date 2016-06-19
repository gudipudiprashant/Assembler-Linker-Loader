from codes import *


def pass1(filename):
	f=open(filename+'_tr','r')
	fw=open(filename+'_p1','w')
	sym_tab={}
	lc=0
	for line in f:
		temp=line.split()
	# storing the label in the sym_table	
		if(':' in temp[0]):
			temp[0]=temp[0].replace(':','')
			sym_tab[temp[0]]=lc
			temp=temp[1:3]
	# making temp smaller to not write separate code for labeled statements

		if( opttab[temp[0]][0] == 1 ):
			
			res=(opttab[temp[0]][1])+' '
			operands=temp[1].split(',')
			for op in operands:

				if op in ['A','B','C','D','E','H','L']:
					if 'DDD' in res:
						res=res.replace('DDD',reg_tab[op])

				elif op.isdigit():
					res+=to_bin(op,8)

				elif op is 'M':
					res+=' '

				else:
					res+=op+' '

			lc+=opttab[temp[0]][2]
			res+='\n'
			fw.write(res)


		elif( opttab[temp[0]][0] == 2 ):
			if(temp[0]=='DB'):
				res='DL#1 '+to_bin(temp[1],8)
	# temp[1] may not exist so make declarations like var a part of DA			
				lc+=1
	# tell prashant about eq assembler directive
			
			elif(temp[0]=='DA'):
				res='DL#2 '+temp[1]
				lc+=int(temp[1])

			res+='\n'
			fw.write(res)

		else:

			lc+=1
			res=opttab[temp[0]][1]
			fw.write(res)

	f.close()
	fw.close()
	return sym_tab,lc



def pass2(filename,sym_tab):
	f=open(filename+'_p1','r')
	fw=open(filename+'_p2','w')
	lc=0

	reloc_tab={}
	link_tab={}
	for line in f:

		temp=line.split()
		res=str(lc)+'   '
		if('DL' in temp[0]):
			if '#1' in temp[0]:
				res+=temp[1]
				lc+=1
				fw.write(res+'\n')

			elif '#2' in temp[0]:
				for i in range(int(temp[1])):
					fw.write(str(lc)+'\n')
					lc+=1

		else:
			res+=temp[0]+'\n'
			lc+=1
			if(len(temp)>1):
				if temp[1].isdigit():
	# implies temp[1] is a literal			 
					res+=str(lc)+'   '+temp[1]+'\n'
					lc+=1

				else:
	# when temp[1] is not a literal		
					temp2=temp[1].split('+')
					temp[1]=temp2[0]
					#print(temp[1])
					if len(temp2)>1:
						extra=temp2[1]
					else:
						extra=0
					if (temp[1] in sym_tab.keys()  ):
	# here the address of the symbol might change due to relocation
						reloc_tab[str(lc)]=sym_tab[temp[1]]+int(extra)					
						bin_=to_bin(sym_tab[temp[1]]+int(extra),16)
						res+=str(lc)+'   '+bin_[8:16]+'\n'
						lc+=1
						res+=str(lc)+'   '+bin_[0:8]+'\n'
						lc+=1

					else:
						link_tab[str(lc)]=temp[1]
						res+=str(lc)+'   '+'00000000'+'\n'
						lc+=1
						res+=str(lc)+'   '+'00000000'+'\n'
						lc+=1


			fw.write(res)

		fw.write('\n')
	f.close()
	fw.close()
	#print(link_tab)
	return reloc_tab,link_tab



