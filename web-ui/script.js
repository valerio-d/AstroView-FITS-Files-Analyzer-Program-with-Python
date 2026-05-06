const fileInput = document.getElementById("fitsFileInput");
const tweakSection = document.querySelector(".tweaks");

if (tweakSection) {
	tweakSection.style.display = "none";
}

// prevent wrong file formats to be uploaded
fileInput.addEventListener("change", function () {
	const file = this.files[0];
	if (!file) {
		return;
	}
	const fileName = file.name;

	if (!fileName.toLowerCase().endsWith(".fits")) {
		alert(
			"Please select a valid file format. Only .fits files will be accepted",
		);
		this.value = ""; // clear file input
		if (tweakSection) {
			tweakSection.style.display = "none";
		}
		return;
	}

	if (tweakSection) {
		tweakSection.style.display = "block";
	}
});

//no UiSlider set up
const slider_image1 = document.getElementById("image1-slider");
const slider_image2 = document.getElementById("image2-slider");
const slider_image3 = document.getElementById("image3-slider");

// Example: Values retrieved from your FITS header/data
const fitsMin = 120;
const fitsMax = 15000;

const sliderConfig = {
	start: [10, 90], // Start at 10% and 90% brightness
	connect: true,
	step: 0.1, // Allows for fine-tuning brightness
	range: {
		min: 0,
		max: 100,
	},
};

noUiSlider.create(slider_image1, sliderConfig);
noUiSlider.create(slider_image2, sliderConfig);
noUiSlider.create(slider_image3, sliderConfig);

slider_image1.noUiSlider.on("update", function (values) {
	// Convert percentage strings to numbers
	const lowPct = parseFloat(values[0]);
	const highPct = parseFloat(values[1]);

	// Map percentages to actual FITS pixel values
	const realLow = fitsMin + (lowPct / 100) * (fitsMax - fitsMin);
	const realHigh = fitsMin + (highPct / 100) * (fitsMax - fitsMin);

	// Now pass realLow and realHigh to your image scaling function
	updateImageContrast(realLow, realHigh);
});
slider_image2.noUiSlider.on("update", function (values) {
	// Convert percentage strings to numbers
	const lowPct = parseFloat(values[0]);
	const highPct = parseFloat(values[1]);

	// Map percentages to actual FITS pixel values
	const realLow = fitsMin + (lowPct / 100) * (fitsMax - fitsMin);
	const realHigh = fitsMin + (highPct / 100) * (fitsMax - fitsMin);

	// Now pass realLow and realHigh to your image scaling function
	updateImageContrast(realLow, realHigh);
});
slider_image3.noUiSlider.on("update", function (values) {
	// Convert percentage strings to numbers
	const lowPct = parseFloat(values[0]);
	const highPct = parseFloat(values[1]);

	// Map percentages to actual FITS pixel values
	const realLow = fitsMin + (lowPct / 100) * (fitsMax - fitsMin);
	const realHigh = fitsMin + (highPct / 100) * (fitsMax - fitsMin);

	// Now pass realLow and realHigh to your image scaling function
	updateImageContrast(realLow, realHigh);
});
