import shutil, glob, pdb, os

prefix = '/mnt/work4/datasets/ee488b'

folders = glob.glob('{}/cropped_img_filtered/*/'.format(prefix))

sets = ['train','val','test']
for dset in sets:
	os.makedirs('{}/release/{}'.format(prefix,dset),exist_ok=True)

valstud = ['정채영']
teststud = ['김선규']

for folder in folders:

	if folder.split('/')[-2] in teststud:
		cmd = "cp -r {}/* {}/release/test/".format(folder,prefix)
		os.system(cmd)
		print(cmd)
	elif folder.split('/')[-2] in valstud:
		cmd = "cp -r {}/* {}/release/val/".format(folder,prefix)
		os.system(cmd)
		print(cmd)
	else:
		cmd = "cp -r {}/* {}/release/train/".format(folder,prefix)
		os.system(cmd)
		print(cmd)