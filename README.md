# Mesh-Reconstruction-of-vehicles-in-Traffic-Sceness.

CSE 598 : Perception In Robotics Project (Spring 2022)

Project Team: 
 1. Pavan Sai Verma Budde 2. Ethan Wisdom 3. Akash Roshan Mund 4. Pavan Kumar Gurram  5. Sai Krishna Vamsi Mahadasa

This repository contains code base from 
 1. https://github.com/nywang16/Pixel2Mesh (Pixel2Mesh)
 2. https://github.com/aimagelab/mcmr (MCMR)
 3. https://github.com/dbolya/yolact (YOLACT)
 
## Project Goal: Construct 3D vehicle mesh from 2D traffic image

## Code Execution Setup
**Pixel2Mesh:** - on ASU Agave
1. module load anaconda/py3
2. conda create --name env python=3.6.8 -y 
3. source activate env
4. pip install tensorflow==1.13.2
5. pip install tflearn==0.3.2
6. pip install --upgrade scikit-image --user
7. python demo.py --image Data/examples/car.png

**MCMR:** - on ASU Agave
1. cd mcmr
2. module load anaconda/py3
3. conda create --name 3dmesh python=3.6.8 -y 
4. source activate 3dmesh
5. module load gcc/7.2.0
6. module load cuda/10.2.89
7. echo CUDA_HOME = usr/local/cuda-10.2

Execute YOLACT on google COLAB

## Output

Experiment On Yolact:

![alt text](https://github.com/buddepavansaivarma/Mesh-Reconstruction-of-vehicles-in-Traffic-Scenes/blob/main/YolactOutPut_image.png)]

Experiment On Yolact + Pixel2Mesh:

![alt text](https://github.com/buddepavansaivarma/Mesh-Reconstruction-of-vehicles-in-Traffic-Scenes/blob/main/Yolact%2Bpixel2mesh_image.png)]

Experiment On MCMR:

![alt text](https://github.com/buddepavansaivarma/Mesh-Reconstruction-of-vehicles-in-Traffic-Scenes/blob/main/mcmr_image.png)]

## Notes

Note that all credit for the code base we have used goes to the original authors of the respective projects. As a part of our project goal, on top of those code bases we have performed our experiments.

 
