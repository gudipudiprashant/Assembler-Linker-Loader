opttab={'LDA':[1,'00111010',3],'ADI':[1,'11000110',2],'STA':[1,'00110010',3],'LXI':[1,'00100001',3],'ADD':[1,'10000110',1]}


opttab['DB']=[2,]
opttab['DA']=[2,]

opttab['HLT'] =[3,'01110110',1]
opttab['DCR'] =[1,'00DDD101',1]
opttab['PUSH']=[1,'11010101',1]
opttab['MOV'] =[1,'01DDD110',1]
opttab['MVI'] =[1,'00DDD110',2]
opttab['JNZ'] =[1,'11000010',3]
opttab['POP'] =[1,'11010001',1]
opttab['CALL']=[1,'11001101',3]
opttab['SUI'] =[1,'11010110',2]
opttab['SUB'] =[1,'10010110',1]
opttab['JMP'] =[1,'11000011',3]
opttab['JM'] = [1,'11111010',3]
opttab['JP'] = [1,'11110010',3]
opttab['RET'] =[1,'11001001',1]
# CHECK push and pop

# we can add double words in our language using shl in assembly

reg_tab={'A':'111','B':'000','C':'001','D':'010'}
reg_tab['E']='011'
reg_tab['H']='100'
reg_tab['L']='101'


def to_bin(x,num):
	x=int(x)
	ans=str('')
	for i in range(num):
		ans=str(x%2)+ans
		x=int(x/2)

	return ans	