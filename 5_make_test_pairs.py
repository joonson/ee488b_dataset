import os, pdb, random, itertools, glob

files = glob.glob('/mnt/work4/datasets/ee488b/release/val/*/*.jpg')

fnames = []

ftree = {}
for file in files:

	fname = file.split('/',7)[-1]

	if file.split('/')[-2] not in ftree:
		ftree[file.split('/')[-2]] = []
	ftree[file.split('/')[-2]].append(fname)
	fnames.append(fname)

identities = list(ftree.keys())

entries = []

with open('val_pairs.txt','w') as f:

	for idx, fname in enumerate(fnames):
		idn = fname.split('/')[0]

		negidn = identities.copy()
		negidn.remove(idn)

		lln = list(itertools.chain.from_iterable([ftree[x] for x in negidn]))

		

		for ii in range(0,2):

			pos = random.choice(ftree[idn])
			entry = '+'.join(sorted([fname,pos]))
			if entry not in entries:
				entries.append(entry)
				f.write('1,%s,%s\n'%(fname,pos))
			else:
				print('{} pos already seen'.format(entry))
			
			neg = random.choice(lln)
			entry = '+'.join(sorted([fname,neg]))
			if entry not in entries:
				entries.append(entry)
				f.write('0,%s,%s\n'%(fname,neg))
			else:
				print('{} neg already seen'.format(entry))

			print(idx)