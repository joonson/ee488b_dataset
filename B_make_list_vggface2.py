import glob, pdb

files = glob.glob('/mnt/work4/datasets/vggface2/train_cropped/*/*.jpg')

with open('train_list.txt','w') as f:

	for file in files:
		
		fname = file.split('/',6)[-1]
		idn = fname.split('/')[0]

		f.write('{} {}\n'.format(idn,fname))