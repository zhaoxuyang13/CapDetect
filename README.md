# CapDetect
Detect bottle cap, for Computer Vision class


- cut.py 

cut objects from input image, ready for labeling or sent to DNN 


- labeling.py

main functionality for labeling
create 4 directories in the same folder
1. resource : images waiting to be cut labeled
2. results  : result images pieces
3. dones    : images already cut and labeled
4. wrong    : images already cut (and labeled) but produce wrong number of pieces.

create 3 files for information
1. label.csv  : labeling results (0-3)
2. number.txt : current pieces number
3. wrongs.txt : pieces that has been mis-labeled.

- detect.py

API function
1. detect
   usage: pos,type,color = detect(image)


