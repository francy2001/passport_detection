# Detection of false passports using CNN on PYNQ board

<h6> Francesca Bocconcelli, Riccardo Bovinelli e Lorenzo Riccardi</h6>

<h2> Introduction </h2>

In this repository, we will document the development of a command-line tool that, given a list of passport images as input, could detect certain categories of <ins cite="https://github.com/turab45/Dataset-forged-characters-detection-on-driving-licences-and-passports">forged characters</ins> using a convolutional neural network implemented on an FPGA and produce an output indicating the area of the image where forgeries are present. The chosen board to implement the CNN is a PYNQ - Z2 by Xilinx. 

The first phase of the project involved creating the dataset. Then, we proceeded to create and train a CNN which is able to recognaze genuine and forged characters. Upon achieving satisfactory results, the corresponding bitstream (and overlay for the PYNQ environment) was generated using the <ins cite="https://github.com/fastmachinelearning/hls4ml">hls4ml library</ins>. 
Finally, deployment on the board, its testing, and the development of a command-line interface to utilize the CNN loaded onto the FPGA were carried out.

![image](https://github.com/francy2001/passport_detection/assets/131793582/c3433073-e2c1-41a0-986e-d611e04a09e1)

<h2>Dataset Creation</h2>

To enable the network to distinguish between genuine and fake passports, we identified four classes of objects it had to recognize: background, normal, altered, and superimposed. For this purpose, three separate files were created, each implementing the creation of a dataset of background images (`dataset_creation/background_dataset.py`), normal characters (`dataset_creation/normal_char_dataset.py`), and fake characters (`dataset_creation/fake_char_dataset.py`). In the directory `dataset_creation/dataset`, examples of the output from the aforementioned codes are available.

<h2>Model creation, training and building of CNN using Vivado</h2>

Once the dataset was created, the network model was built, pruning was performed, and the network was trained. Subsequently, the network configuration suitable for deployment on the PYNQ was defined. Finally, the network was built using Vivado. In this phase, libraries provided by TensorFlow and hls4ml were extensively utilized.
The relative code is present in `CNN_hls4ml.ipynb` and the obtained weight are in `pruned_cnn_model.h5`.
The files to pass the CNN to PYNQ (for example, the bitstream file) are in `hls4ml_PYNQ/`. 


<h2>Command-line interface</h2>

In order to use the software developed in this project, a Python script with a command-line interface was created. The following interface was chosen:
```
$ python pynqports.py img1 ... imgN
```
with img1 ... imgN being a list of paths referring to images in a format supported by NumPy. 
The relative code is present in `pynqports.py`.

![m](https://github.com/francy2001/passport_detection/assets/131793582/a7028f2a-a29b-47f2-818e-8d660c692a14)


  
