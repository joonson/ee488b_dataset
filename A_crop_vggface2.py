from zipfile import ZipFile
from tqdm import tqdm
import os, glob, sys, shutil, time
import numpy as np
import torch
import cv2

# suppress warnings
import warnings
warnings.filterwarnings("ignore")


# The following lines are the only parts of the code that you need to change. You can simply run the rest.
detector_path   = os.path.join('models/s3fd_facedet.zip') # Location of the face detector
orig_path       = '/mnt/work4/datasets/vggface2/train'
temp_path       = '/mnt/work4/datasets/vggface2/train_cropped' # Location to temporarily store your cropped images. No need to change this. 


files = glob.glob('{}/*/*.jpg'.format(orig_path))
print(len(files),'files found')


sys.path.append('detectors')
from detectors import S3FD

# Load the face detector (you can ignore this part)
DET = S3FD(device='cuda')


class your_dataset(torch.utils.data.Dataset):
    def __init__(self, files):

        self.data   = files

        print('{:d} files in the dataset'.format(len(self.data)))

    def __getitem__(self, index):

      fname = self.data[index]
    
      try:
        # return image if read is successful
        image = cv2.imread(fname)
        image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image, image_np, fname
      except:
        # return empty if not successful
        return np.array([]), np.array([]), fname

    def __len__(self):
      return len(self.data)

dataset = your_dataset(files)
loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False, num_workers=10)



pbar = tqdm(loader)

for data in pbar:

    try:

      # skip if there is read error
      if len(data[0].shape) != 4:
        print('Skipping {} - read error'.format(data[2]))
        continue
      
      image     = data[0][0].numpy()
      image_np  = data[1][0].numpy()
      fname     = data[2][0]

      bboxes = DET.detect_faces(image_np, conf_th=0.9, scales=[0.5])

      # pbar.set_description("{:d} faces detected in {}".format(len(bboxes),fname))

      ## this removes all images with no face detection or two or more face detections
      if len(bboxes) == 1:

        # padding value
        bsi = 300

        # find center and square size
        sx = int((bboxes[0][0]+bboxes[0][2])/2) + bsi
        sy = int((bboxes[0][1]+bboxes[0][3])/2) + bsi
        ss = int(max((bboxes[0][3]-bboxes[0][1]),(bboxes[0][2]-bboxes[0][0]))/1.5)

        # pad the image
        image = np.pad(image,((bsi,bsi),(bsi,bsi),(0,0)), 'constant', constant_values=(110,110))

        # crop the face
        face = image[int(sy-ss):int(sy+ss),int(sx-ss):int(sx+ss)]

        # check that it is square and RGB
        if face.shape[0] == face.shape[1] and face.shape[0] > 10 and face.shape[2] == 3:

          face = cv2.resize(face,(256,256))
          outname = fname.replace(orig_path,temp_path).replace('.png','.jpg')
          os.makedirs(os.path.dirname(outname),exist_ok=True)
          cv2.imwrite(outname,face)

        else:

          print('[INFO] Non square image {}'.format(fname))

    except:

        print('[INFO] Unknown error {}'.format(fname))