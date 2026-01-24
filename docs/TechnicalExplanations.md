- # Code Explainations
- ## Importing
	-
	  ```python
	  from astropy.io import fits
	  import numpy as np
	  import matplotlib.pyplot as plt
	  ```
	- **Astropy** is the main Python library for astronomy
	- `astropy.io` is what handles input/output
	- `fits` is the module for **Flexible Image Transport System** (FITS) **files**.
	- FITS files can store images, spectra, data cubes, and metdata
	-
	- **NumPy** is the Python library for scientific and numerical calculations
	- NumPy uses arrays which in astrophysics can represent images (2D), spectral cubes (3D), time series, and catalogs. Everything in a FITS image eventually becomes a <u>NumPy array</u>
	-
	- **Matplotlib** is the library used to plot graphs
	- it can be used to display images, plot spectra, show light curves, visualize data cubes
	-
	-
	  > Astropy reads data -> Numpy manipulates data -> Matplotlib visualizes data  
	-
- ## The FITS File
	-
	  ```python
	  fits_file_path = r'etaCarinae.fits'
	  ```
	- This is the path to the FITS file, showing the Eta Carinae, a massive, unstable binary star system located in the Carina Nebula.
	- the `r` means **raw string**, this prevents Python from interpreting backslashes as escape characters
	-
- ## Error Handling
	- Start the code with a **try-except block**, meaning that if data files are missing or corrupted there will be no crashes or errors. - essential in scientific coding
	-
- ## Opening the FITS File
	-
	  ```python
	  with fits.open(fits_file_path) as hdulist:
	  ```
	- `fits.open()` opens the FITS file and returns an **HDUList (Header Data Unit)**
	- FITS files are lists of HDUs, HDU0 is the primary HDU, the main image, while anything after that is the extra images, tables, spectra, etc.
	- `with - as` is good practice as the file is automatically closed once open.
-
- ## Inspecting the FITS structure
	-
	  ```python
	  hdulist.info()
	  ```
	- this outputs the Number of HDUs, type of each HDU, shape of the data, and data type, giving a general overview of the data inside the FITS file.
-
- ## Extracting the Image Data
	-
	  ```python
	  image_data = hdulist[0].data
	  ```
	- By doing this, we define the image_data variable
	-
	  ```hdulist[0]```
	- `.data` extracts the numerical data as a **NumPy array**, meaning that the variable itself is now a Numpy array too.
-
- ## Error Handling and Data Checking
	- ```python
	  if image_data is None:
	    raise ValueError("No image data found .....")
	  ```
	- This prevents errors/crashing if a FITS file doesn't contain any image data <u>in the primary HDU</u> as some store it in other HDUs
-
- ## Inspecting the Dimensions
	-
	  ```python
	  print(f"Image Data Shape: {image_data.shape}")
	  ```
	- `.shape` tells us the **array dimensions**
	- for example: (1024, 1024) -> 2D image, (10, 1024, 1024) -> 10 slices of images
	-
- ## Handling 2D and 3D data
	-
	  ```python
	  if image_data.ndim == 2:
	  ```
	- `.ndim` is the number of dimentions
	-
	- ### 2D image
		-
		  ```python
		  image_stack = image_data[np.newaxis, :, :]
		  ```
		- `np.newaxis` adds a new dimension, treating the shape as a stack
		- original shape -> (Y,X) | new shape => (1, Y, X)
	- ### 3D image
		-
		  ```python
		  elif image_data.ndim == 3:
		    image_stack = image_data
		  ```
		- if the image is 3D, it has 3 dimensions and is already a stack so no changes are needed
	- ### Error Handling: Unsupported Dimensions
		-
		  ```python
		  else:
		    raise ValueError("unsupported image dimensions")
		  ```
-
- ## Visualizing the FITS File
	-
	  ```python
	  if image_data.ndim in (2,3):
	  ```
	- ensuring that only valid images types proceed
	-
	- ### Single slice visualization (option 1)
		-
		  ```python
		  single_slice = image_stack[0, ":, :"]
		  ```
		- selects the first slice, shape format => (Y,X)
		- In astrophysics, this could be: First energy bin, First time frame, First wavelength slice
		-
		- #### **Log Scaling**
			-
			  ```python
			  single_slice = np.log10(single_slice - np.min(single_slice) + 1)
			  ```
			- astronomical images have huge dynamic range, brighter sources can be millions of times brighter than faint ones
			- `np.min(single_slice)` shifts the minimum to 0
			- `+1` avoids log(0)
			- `np.log10()` compresses the dynamic range
			- all of this is standard in astronomy imaging
		- #### **Clipping**
			-
			  ```python
			  single_slice = np.clip(single_slice, 0, np.max(single_slice))
			  ```
			- ensuring that there are no negative values
			- preventing display artifacts
		- #### **Plotting**
			-
			  ```python
			  plt.figure(figsize=(8, 8))
			  plt.imshow(single_slice, cmap='gray', origin='lower')
			  ```
				- `figsize` inches
				-
				  ```imshow```
				- ``cmap='gray'`` is the standard color for astronomy
				- `origin='lower'` is the coordinate system that macthes the FITS convention
				- astronomy images use bottom-left as origin, not top-left
				-
				- ```python
				  plt.colorbar()
				  ```
				- adds an **intensity scale** on the side, useful for <u>scientific interpretation</u>
				-
				-
				  ```python
				  plt.title('FITS Image - Slice 0 (Log Scaled)')
				  plt.xlabel('X Pixel')
				  plt.ylabel('Y Pixel')
				  plt.show()
				  ```
				- labelling the axis and image, showing the plot
		- ### Combine slices - mean projection (option 2)
			-
			  ```python
			  combined_image = np.mean(image_stack, axis=0)
			  ```
			- this collapses the stack, resulting in a 2D image
			- used in astrophysics for increasing signal-to-noise
			- collapsing energy or time dimentions
		- ### Visualize all Slices (option 3)
			-
			  ```python
			  num_slices = image_stack.shape[0]
			  ```
			- number of **images** in the stack
			-
			  ```python
			  fig, axes = plt.subplots(1, num_slices, figsize=(5 * num_slices, 5))
			  ```
			- creating multiple sublots, one for each slice
			-
			- #### **Loop over slices**
				-
				  ```python
				  for i in range(num_slices):
				    axes[i].imshow(slice_image, cmap='gray', origin='lower')
				    axes[i].set_title(f'Slice {i}')
				    axes[i].axis('off')
				  ```
				- produces a gallery of slices, showing each one after the other
-

