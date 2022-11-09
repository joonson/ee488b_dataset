import glob, pdb, os
import pandas as pd
import shutil

xlfiles = glob.glob('/mnt/work4/datasets/ee488b/extracted3/정홍*/face_dataset/sim_results.xlsx')

for folder in glob.glob('/mnt/work4/datasets/ee488b/extracted3/정홍*/'):

	if not os.path.exists(folder+'/face_dataset/sim_results.xlsx'):

		print(folder)

prefix = '/mnt/work4/datasets/ee488b/cropped_img'
tgtfix = '/mnt/work4/datasets/ee488b/cropped_img_filtered'

for xlfile in xlfiles:

	print('Opening',xlfile)

	studentname = xlfile.split('/')[-3]

	data = pd.read_excel(xlfile) 
	df = pd.DataFrame(data)

	filenames = df['File'].tolist()
	accepts	  = df['Accept'].tolist()

	assert len(accepts) == len(filenames)

	for iidx, imgfile in enumerate(filenames):

		imgpath = os.path.join(prefix,studentname,imgfile.split('/',2)[-1])

		tgtpath = os.path.join(tgtfix,studentname,imgfile.split('/',2)[-1])

		if not os.path.exists(imgpath):

			print('Error found {}'.format(imgpath))

		elif accepts[iidx] == 'Y':

			os.makedirs(os.path.dirname(tgtpath),exist_ok=True)
			shutil.copyfile(imgpath,tgtpath)
