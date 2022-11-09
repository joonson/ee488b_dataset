import torch
import zipfile
import pdb
import glob
import os

prefix = '/mnt/work4/datasets/ee488b'

files = glob.glob('{}/정홍*.zip'.format(prefix))

for file in files:
	studentname = os.path.splitext(os.path.basename(file))[0]
	with zipfile.ZipFile(file, 'r') as zip_ref:
	    zip_ref.extractall('{}/extracted3/{}'.format(prefix,studentname))
	print('Extracted {}'.format(studentname))
	if not os.path.exists('{}/extracted3/{}/face_dataset'.format(prefix,studentname)):
		print('Check {} for data'.format(studentname))