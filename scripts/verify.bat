@echo OFF

@REM This script is used to move data from the Rust code to the Python ML model.
@REM It is used to verify the schema.

set enviroment="schema_verifier"
set python_script="model/verify.py"

echo Activating conda
call conda activate %enviroment%

echo Running Python Script
python %python_script% %*

echo Deactivating CONDA
call conda deactivate