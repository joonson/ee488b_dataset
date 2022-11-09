import glob, pdb, os
import zipfile


files = glob.glob('/mnt/work4/datasets/ee488b/extracted3/정홍*/face_dataset/v1_cropped_data.zip')

prefix = '/mnt/work4/datasets/ee488b'

for file in files:
	studentname = file.split('/')[-3]
	with zipfile.ZipFile(file, 'r') as zip_ref:
	    zip_ref.extractall('{}/cropped_img/{}'.format(prefix,studentname))

	print('Extracted {}'.format(studentname))

