from astropy.io import fits #astropy handles input/output, fits is the module for Flexible Image Transport System Files
import numpy as np #numpy uses arrays to represent images, spectral cubes, time series, and catalogs. Everything in a FITS file becomes a NumPy array.
import matplotlib.pyplot as plt #Used to plot graphs

# Open the FITS file and handle multi-dimensional data
fits_file_path = r'n132d_0.3-0.5keV.fits'  # Raw string for file path
# Brightness control (percentile ranges after log scaling)
# Lower the low percentile and/or lower the high percentile to make an image look brighter. 
BRIGHTNESS_PERCENTILES = { #adjust values to adapt to image ligthing
    "option1": (30, 100),
    "option2": (30, 85),
    "option3": (1, 10),
}
#fits file credits: https://chandra.harvard.edu/photo/openFITS/xray_data.html

try: #try-except block in case file is corropted or data files are missing
    # Open FITS file using fits.open()
    with fits.open(fits_file_path) as hdulist: 
        #FITS files are lists of HDUs, Header Data Unit, HDU0 is the main image, anything after that is extras
        hdulist.info()  
        # Print information about FITS file
        #outputs the number of HDUs, type of each HDU, shape of the data, and data type
        
        # Access the primary HDU data (the main image)
        image_data = hdulist[0].data #.data extracts the numerical data as a NumPy array
        

        # Error Handling: Check if data exsists
        if image_data is None:
            raise ValueError("No image data found in the primary HDU. Check other HDUs.")
        
        # Check the shape of the image data
        print(f"Image Data Shape: {image_data.shape}") 
        #shape displays the array dimentions
        #e.g., (1024, 1024) is a 2D image, (10, 1024, 1024) there are 10 slices of images

        if image_data.ndim == 2: #ndim is the number of dimensions
            # Treat 2D as a single-slice stack so all options run
            image_stack = image_data[np.newaxis, :, :] 
            #adds a new dimentions, treating the shape as a stack

        elif image_data.ndim == 3:
            image_stack = image_data 
            #if the image is 3D, nothing is chnaged (it already is a stack)

        else:
            raise ValueError(f"Unsupported image dimensions: {image_data.ndim}")

        if image_data.ndim in (2, 3):
            # Option 1: Visualize a single slice (e.g., the first slice)
            single_slice = image_stack[0, :, :]

            #log scaling
            single_slice = np.log10(single_slice - np.min(single_slice) + 1)
            #clipping
            single_slice = np.clip(single_slice, 0, np.max(single_slice))

            #plotting
            vmin1, vmax1 = np.percentile(single_slice, BRIGHTNESS_PERCENTILES["option1"])
            plt.figure(figsize=(8, 8))
            plt.imshow(single_slice, cmap='gray', origin='lower', vmin=vmin1, vmax=vmax1) #display the image, gray color
            plt.colorbar() #add intensity sclae for scientific interpretation
            plt.title('FITS Image - Slice 0 (Log Scaled)') #labelling
            plt.xlabel('X Pixel')
            plt.ylabel('Y Pixel')
            plt.show()

            # Option 2: Combine slices (e.g., mean projection)
            combined_image = np.mean(image_stack, axis=0)
            #this collapses the stack resulting in 2D image

            combined_image = np.log10(combined_image - np.min(combined_image) + 1)
            combined_image = np.clip(combined_image, 0, np.max(combined_image))

            vmin2, vmax2 = np.percentile(combined_image, BRIGHTNESS_PERCENTILES["option2"])
            plt.figure(figsize=(8, 8))
            plt.imshow(combined_image, cmap='gray', origin='lower', vmin=vmin2, vmax=vmax2)
            plt.colorbar()
            plt.title('FITS Image - Mean Projection (Log Scaled)')
            plt.xlabel('X Pixel')
            plt.ylabel('Y Pixel')
            plt.show()

            # Option 3: Visualize all slices
            num_slices = image_stack.shape[0]
            fig, axes = plt.subplots(1, num_slices, figsize=(5 * num_slices, 5)) #creates multiples sublots, one for each slice
            # Ensure axes is always iterable (for single-slice case)
            if num_slices == 1:
                axes = [axes]
            for i in range(num_slices): #loop over the images
                slice_image = image_stack[i, :, :]

                slice_image = np.log10(slice_image - np.min(slice_image) + 1)
                slice_image = np.clip(slice_image, 0, np.max(slice_image))

                vmin3, vmax3 = np.percentile(slice_image, BRIGHTNESS_PERCENTILES["option3"])
                axes[i].imshow(slice_image, cmap='gray', origin='lower', vmin=vmin3, vmax=vmax3)
                axes[i].set_title(f'Slice {i}')
                axes[i].axis('off')
            plt.show()

except FileNotFoundError:
    print(f"File not found: {fits_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
