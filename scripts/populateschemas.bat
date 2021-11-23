@echo OFF

@REM This script is used to populate the schemas.txt data file.
@REM It's not really necessary if you're using the default data.
@REM It's here to help you if you want to add your own data.
@REM Just change device to mckbuilder if alredy built. 

set device=cargo run
set loops=%1

cd ../
for /l %%x in (1, 1, %loops%) do (
   %device% train 15
    echo "Trained 15"
)
cd scripts