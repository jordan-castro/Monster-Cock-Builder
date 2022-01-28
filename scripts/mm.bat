:: This file is used to run the mosaic method. Just pass in the original image and the output image name.
@echo OFF

set enviroment="schema_verifier"
set python_script="model/mosaic.py"

:: Activate environment
echo Activating CONDA
call conda activate %enviroment%

:: Call script
echo Running Python Script
python %python_script% %*

:: Deactivate environment
echo Deactivating CONDA
call conda deactivate