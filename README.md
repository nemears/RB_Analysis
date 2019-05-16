# RB_Analysis
Video processing scripts used for generating and fitting autocorrelation functions for a 2D surface

To use:

cordirectory.py: Takes given directory and finds spatial Autocorrelation function for each image, and
  exports to csv file under same name as directory
  
  make sure to fill out directory and image type in script
  run script and select area to be analyzed
  script will then finish and export ACFs to csv file
  
findcoefficients.py: takes csv file of autocorrelation functions and fits them with layered exponential
  fits
  
  make sure proper csv filename is in script
  run script and new csv file with extension to name -fit will appear with coefficients for function fits
  in columns
