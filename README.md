# caustic_fit
Fits a caustic function to a set of measurement points of beam sizes around a focus to determine beam quality M²

Written in spyder.
This code reads data points from a csv file (example provided in repository) that consists of measurements of beam sizes around a focus.
The data contains distance z in column 1, beam size in x in column 2 and beam size in y in column 3.
The code then fits a caustic function to the data points to determine focus size, focus position and beam quality M² in both axis.
