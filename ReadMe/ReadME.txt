Pre-requirements-
1. Download and Install Anaconda Open Source Distribution of Python in your system.
2. Download a code editor(VsCode,SublimeText) to open the folder in your system.
3. Create a conda environment and install the required libraries

Steps to create a conda environment and install the require librariess-
step 1 - Open anaconda prompt
step 2 - Run the following commands
		   1.	conda create -n heartcure python=3.9
		   2.	conda activate heartcure 
		   3.	pip install opencv-python numpy tensorflow scikit-learn imutils flask xgboost

Steps to run Project-
step 1- Open anaconda prompt
step 2- Go to your project location using the terminal
step 3- Activate the conda environment which you just created:
		  conda activate heartcure
step 4- Run your project using the following command:
   		  flask run
step 5- Open any browser and run the project using the address provided in the terminal:
		  http://127.0.0.1:5000 (it may vary in your system)

Step 6 – To view your prediction history, go to:
http://127.0.0.1:5000 (the address may vary depending on your system and port)


