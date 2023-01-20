supported protocol types

* standard - oscillation experiment, rotate omega only, no sample x, y, z motion
* vector - oscillation experiment, rotate omega, translate x, y, and z
* raster - implemented as a step scan with each row/column a vector with only x (or y) and omega translation, followed by a step in the y (or x) direction. note that this is not like other facilities that generally have only an x (or y) translation, with the detector triggered on that axis, without an omega rotation
* eScan - energy scan - change DCM energy axis, monitor with X-ray fluorescence detector
