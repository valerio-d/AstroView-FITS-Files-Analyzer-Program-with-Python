from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

# Open the FITS file and handle multi-dimensional data
fits_file_path = r'etaCarinae.fits'  # Raw string for file path
#fits file credits: https://chandra.harvard.edu/photo/openFITS/xray_data.html

try:
    # Open FITS file
    with fits.open(fits_file_path) as hdulist:
        hdulist.info()  # Print information about FITS file

        # Access the primary HDU data
        image_data = hdulist[0].data

        # Check if data is None
        if image_data is None:
            raise ValueError("No image data found in the primary HDU. Check other HDUs.")
        
        # Check the shape of the image data
        print(f"Image Data Shape: {image_data.shape}")

        if image_data.ndim == 2:
            # Treat 2D as a single-slice stack so all options run
            image_stack = image_data[np.newaxis, :, :]
        elif image_data.ndim == 3:
            image_stack = image_data
        else:
            raise ValueError(f"Unsupported image dimensions: {image_data.ndim}")

        if image_data.ndim in (2, 3):
            # Option 1: Visualize a single slice (e.g., the first slice)
            single_slice = image_stack[0, :, :]

            single_slice = np.log10(single_slice - np.min(single_slice) + 1)
            single_slice = np.clip(single_slice, 0, np.max(single_slice))

            plt.figure(figsize=(8, 8))
            plt.imshow(single_slice, cmap='gray', origin='lower')
            plt.colorbar()
            plt.title('FITS Image - Slice 0 (Log Scaled)')
            plt.xlabel('X Pixel')
            plt.ylabel('Y Pixel')
            plt.show()

            # Option 2: Combine slices (e.g., mean projection)
            combined_image = np.mean(image_stack, axis=0)

            combined_image = np.log10(combined_image - np.min(combined_image) + 1)
            combined_image = np.clip(combined_image, 0, np.max(combined_image))

            plt.figure(figsize=(8, 8))
            plt.imshow(combined_image, cmap='gray', origin='lower')
            plt.colorbar()
            plt.title('FITS Image - Mean Projection (Log Scaled)')
            plt.xlabel('X Pixel')
            plt.ylabel('Y Pixel')
            plt.show()

            # Option 3: Visualize all slices
            num_slices = image_stack.shape[0]
            fig, axes = plt.subplots(1, num_slices, figsize=(5 * num_slices, 5))
            for i in range(num_slices):
                slice_image = image_stack[i, :, :]

                slice_image = np.log10(slice_image - np.min(slice_image) + 1)
                slice_image = np.clip(slice_image, 0, np.max(slice_image))

                axes[i].imshow(slice_image, cmap='gray', origin='lower')
                axes[i].set_title(f'Slice {i}')
                axes[i].axis('off')
            plt.show()

except FileNotFoundError:
    print(f"File not found: {fits_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
