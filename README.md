# Comprehensive-Assessment-of-OCR-Tools-for-Gene-Name-Recognition-in-Biological-Pathway-Figures
Code for Comprehensive Assessment of OCR Tools for Gene Name Recognition in Biological Pathway Figures

Notes:

data fusion stuff was not used since it wasn't in a good enough state for including
however we are planning to work on data fusion more in the future
overall there are bits of code from working on other things that got bundled together for this paper

word dist results.py generates more detailed results about each dataset
more in depth examination of those results will happen in a future work

data is included for others to examine. Ground truth and images are included so you can generate results yourself if you want.

mmocr version 0.6 was used. Configurations and scripts may require updating for 1.0. 
Also models may have changed, so beware that you may get different results for versions other than 0.6

make sure to have mmocr installed and environment activated before running code, since everything is dependent on mmocr for results
instructions on installing dependencies is not included since they're either in pip, conda, or have instructions on their respective websites

some of the code such as result summary scripts require specifc arguments in a specific order and don't have handling to prevent overwritting files
so be careful to read any code before running it

ask questions to sa5f5@umsystem.edu
(email will no longer be valid after May 2023, so if this email has not been updated, contact co-authors)
