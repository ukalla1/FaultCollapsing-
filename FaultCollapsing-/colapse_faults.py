import re

def init_refine(sample):
	PIECES = re.split('[ ]|[\n]|[;]', sample)
	return list(filter(None, PIECES))

def net_refine(sample):
	PIECES = re.split('[,]', sample)
	return list(filter(None, PIECES))

def sub_net_refine(sample):
	ret_lst = []
	PIECES = re.split("[)]|[(]|[ ]|,|;|[.]Y\d{2}|[.]Y\d{1}.|[\n]|[.]Y|[.]A|[.]B", sample)
	return list(filter(None, PIECES))

def collapse(saf_af, net):
	idfier = net[0]
	mnet = net[1:]

	if 'NAND' in idfier:
		if mnet[0] in saf_af['Sa1']:
			nl = saf_af['Sa0']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			if mnet[2] in nl:
				nl.remove(mnet[2])
			saf_af['Sa0'] = nl
	elif 'NOR' in idfier:
		if mnet[0] in saf_af['Sa0']:
			nl = saf_af['Sa1']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			if mnet[2] in nl:
				nl.remove(mnet[2])
			saf_af['Sa1'] = nl
	elif 'AND' in idfier:
		if mnet[0] in saf_af['Sa0']:
			nl = saf_af['Sa0']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			if mnet[2] in nl:
				nl.remove(mnet[2])
			saf_af['Sa0'] = nl
	elif 'OR' in idfier:
		if mnet[0] in saf_af['Sa1']:
			nl = saf_af['Sa1']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			if mnet[2] in nl:
				nl.remove(mnet[2])
			saf_af['Sa1'] = nl
	elif 'INV' in idfier:
		if mnet[0] in saf_af['Sa1']:
			nl = saf_af['Sa0']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			saf_af['Sa0'] = nl
		elif mnet[0] in saf_af['Sa0']:
			nl = saf_af['Sa1']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			saf_af['Sa1'] = nl
		if mnet[1] in saf_af['Sa1']:
			nl = saf_af['Sa0']
			if mnet[0] in nl:
				nl.remove(mnet[0])
			saf_af['Sa0'] = nl
		elif mnet[1] in saf_af['Sa0']:
			nl = saf_af['Sa1']
			if mnet[0] in nl:
				nl.remove(mnet[0])
			saf_af['Sa0'] = nl
	elif 'BUFX' in idfier:
		if mnet[0] in saf_af['Sa1']:
			nl = saf_af['Sa1']
			nln = saf_af['Sa1']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			saf_af['Sa1'] = nl
		elif mnet[0] in saf_af['Sa0']:
			nl = saf_af['Sa0']
			if mnet[1] in nl:
				nl.remove(mnet[1])
			saf_af['Sa0'] = nl
		if mnet[1] in saf_af['Sa1']:
			nl = saf_af['Sa1']
			if mnet[0] in nl:
				nl.remove(mnet[0])
			saf_af['Sa1'] = nl
		elif mnet[1] in saf_af['Sa0']:
			nl = saf_af['Sa0']
			if mnet[0] in nl:
				nl.remove(mnet[0])
			saf_af['Sa0'] = nl
	else:
		pass
	return saf_af


def main():
	file_under_use = "c880.v"
	netlist_location = "./input/Benchmark/"

	output_location = "./"
	op1 = "output_bf.txt"
	op2 = "output_af.txt"

	netlist = open(netlist_location+file_under_use, 'r')
	netlist_lines = netlist.readlines()
	init_netlist = []
	for i in range (0, len(netlist_lines)):
		tmp = init_refine(netlist_lines[i])
		init_netlist.append(tmp)

	saf_bf = {'Sa0': [], 'Sa1': []}
	for i in range (1, ((len(init_netlist))-1)):
		if (len(init_netlist[i])) > 1:
			if len(init_netlist[i]) > 2:
				del init_netlist[i][1]
			elif (init_netlist[i][0] == 'input' or init_netlist[i][0] == 'output' or init_netlist[i][0] == 'wire'):
				tmp = net_refine(init_netlist[i][-1])
				saf_bf['Sa0'] += tmp
				saf_bf['Sa1'] += tmp
			else:
				pass

	nets = []
	for i in range (4, ((len(init_netlist))-1)):
		if ('wire' not in init_netlist[i] and 'input' not in init_netlist[i] and 'output' not in init_netlist[i]):
			if (len(init_netlist[i])) > 1:
				tmp = sub_net_refine(init_netlist[i][-1])	
				nets.append([init_netlist[i][0]] + tmp)

	l0 = saf_bf['Sa0']
	l1 = saf_bf['Sa1']
	for i in nets:
		for k in i[1:]:
			if k not in l0:
				l0.append(k)
			if k not in l1:
				l1.append(k)
	saf_bf['Sa0'] = l0
	saf_bf['Sa1'] = l1

	cnt_bf = 0
	op_l1 = open(output_location+op1, 'w')
	for (k,v) in saf_bf.items():
		for i in v:
			cnt_bf += 1
			op_l1.write("{}\t\t\t\t{}\n".format(k,i))
	op_l1.write("totalfaults BF = {}\n".format(cnt_bf))
	op_l1.close()

	saf_af = saf_bf

	for i in nets:
		if ('NAND' in i[0] or 'NOR' in i[0] or 'AND' in i[0] or 'OR' in i[0] or 'INV' in i[0] or 'BUFX' in i[0]):
			saf_af = collapse(saf_af, i)
		else:
			pass

	cnt_af = 0
	op_l2 = open(output_location+op2, 'w')
	for (k,v) in saf_af.items():
		for i in v:
			cnt_af += 1
			op_l2.write("{}\t\t\t\t{}\n".format(k,i))

	op_l2.write("Total Faults_AF = {}\n".format(cnt_af))
	op_l2.write("the collapse ratio is = {}/{} = {}\n".format(cnt_af,cnt_bf,float(cnt_af/cnt_bf)))
	op_l2.close()

	return 0

name = "__main__"
if name == "__main__":
	main()