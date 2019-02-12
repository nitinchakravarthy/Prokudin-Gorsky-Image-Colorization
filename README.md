# Prokudin-Gorsky-Image-Colorization
This project provides a python code that aligns and colorize Sergey prokudin-gorsky's digitized glass plate images.
More information about the images can be found here http://www.loc.gov/pictures/collection/prok/.

The code contains three different approaches.
Normalized cross-correlation was used to align images.
The first implementaion is a naive look up with a window size of [-15, 15] on the horizonatal and the vertical axes. This method is implemented in the 'getShift()' method in the code.

The second implementation is a recurssive approach in which the image is donwnscaled till a point where a naive search approach would result in an acceptable solution and backtrack it till the top with a very local search window ([-1,1]) at every level. This is a top-down recursive implementaion. This method is implemented in the 'getShiftPyramid()' method in the code.

The third implemntation is a interative implementation of the second approach, in which the number of level to downsample is calculated initially and then loop is run from the lowest scale by incrementing the scale by a factor of 2 everytime till we reach the desired scale also which performing a very local search at every step. This is a bottom- up implementaion. Implemented in the 'getShiftPyramidIterative()' method in the code.

A sample input and output are as follows:

![alt text](https://github.com/nitinchakravarthy/Prokudin-Gorsky-Image-Colorization/blob/master/Images/cathedral.jpg)
![alt text](https://github.com/nitinchakravarthy/Prokudin-Gorsky-Image-Colorization/blob/master/Results/cathedral.jpg)
