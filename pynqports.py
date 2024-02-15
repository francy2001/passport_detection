from axi_stream_driver import NeuralNetworkOverlay
import numpy as np
from PIL import Image
from os import path
import sys

def addBBox(image, certainty):
    if certainty < 0.75:
        color = [1, 1, 0]
    else:
        color = [1, 0, 0]
    image[0,:,:] = color
    image[:,0,:] = color
    image[-1,:,:] = color
    image[:,-1,:] = color
    return image

n_classes = 4
slices = np.ndarray((234,32,32,3))
nn = NeuralNetworkOverlay('hls4ml_nn.bit', slices.shape, (slices.shape[0], n_classes))
img_output_folder = ""

img_width = 600
img_height = 430
block_width = 32
block_height = 32

for file_arg in sys.argv[1:]:
    img = Image.open(file_arg)

    im_arr = np.asarray(img)
    
    # slices extraction
    k = 0
    for j in range(int(img_width / block_width)):
        for i in range(int(img_height / block_height)):
            slices[k,:,:,:] = im_arr[(block_width * i):(block_width * (i+1)),(16+block_height * j):(16+block_height * (j+1))] / 255.0
            k += 1

    predictions_1, latency_1, throughput_1 = nn.predict(slices, profile=True)

    # classification and image reconstruction
    i = 0
    output_file = path.join(img_output_folder, "".join(file_arg.split(".")[:-1]) + "_analyzed.png")
    reconstructed_image = np.ndarray((416,0,3))
    
    for classification in predictions_1:
        max_class = np.max(classification)
        if (max_class == classification[2] or max_class == classification[3]):
            slices[i,:,:,:] = addBBox(slices[i,:,:,:], max_class)
    
        if i % int((img_height / 32)) == 0:
            if i != 0:
                reconstructed_image = np.concatenate((reconstructed_image, column), axis=1)
            #else:
            #    reconstructed_image = slices[i,:,:,:]
            column = slices[i,:,:,:]
        else:
            column = np.concatenate((column, slices[i,:,:,:]), axis=0)
        i += 1
    
    Image.fromarray((reconstructed_image * 255).astype(np.uint8)).save(output_file)
    print("written " + str(output_file))