# Image Interpolation and enhancement backend server
Backend apis for image enhancer.
Combines a high resolution panchromatic image(lacks the chromatic data) in base64 format with a low resolution multispectral (lacks the resolution data) in base64 format image first using wavelet fusion, then passes it through a Laplacian filter for sharpening and then sends the data to the frontend.


#Steps To Recreate the Project

<ul>
<li> Download the conda distribution, from <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html" >Here</a> and follow the steps to install the conda distribution successfully</li>
<li>After downloading the distribution activate a conda virtual environment using the command create a new virtual environment using the command conda create -n envname python=x.x anaconda </li>
<li>Activate the virtualenv</li>
<li> Clone the project inside the folder you want to recreate it</li>
<li> Download the necessary requirements by using the command pip install -r requirements.txt</li>
<li>Go to the directory containing the main.py file. Run the command _uvicorn main:app --reload_ to start the server. The server is now ready to accept requests from the frontend. </li>
</ul>