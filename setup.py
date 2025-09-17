import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CrystalTool",                            
    version="0.1",                            
    author="Yi Yao, Lin Li",                        
    description="A simple python package to handle crystal structure problems",
    long_description=long_description,          
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),        
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                         
    python_requires='>=3.10',                  
    py_modules=["CrystalTool"],                   
    package_dir={'':'CrystalTool/src'},            
    install_requires=[]                       
)