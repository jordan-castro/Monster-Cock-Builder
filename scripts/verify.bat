@echo OFF

@REM This script is used to move data from the Rust code to the Python ML model.
@REM It is used to verify the schema.

set enviroment="schema_verifier"
set python_script="model/verify.py"

echo Activating conda
call conda activate %enviroment%

@REM KMeans is known to have a memory leak on Windows with MKL, 
@REM when there are less chunks than available threads. 
@REM You can avoid it by setting the environment variable OMP_NUM_THREADS=1.
set OMP_NUM_THREADS=1

echo Running Python Script
python %python_script% %*

echo Deactivating CONDA
call conda deactivate