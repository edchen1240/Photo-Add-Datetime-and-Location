# Photo Add Datetime and Location

This project provides a set of Python scripts to extract datetime and location information from images and add this information to the images as text.

## Features

- Extract datetime information from image EXIF data
- Extract GPS coordinates from image EXIF data
- Perform reverse geocoding to get city and country information from coordinates
- Add extracted information as text to the image
- Handle various image formats (JPG, JPEG, PNG, GIF) and video formats (MP4, MOV)

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- Pandas
- Tabulate
- ExifRead
- Pillow
- Reverse Geocoder
- Matplotlib

## Installation

1. Clone this repository
2. Install the required packages:

```
pip install opencv-python numpy pandas tabulate ExifRead Pillow reverse_geocoder matplotlib
```

## Usage

1. Import the necessary modules:

```python
import Module_1_File as M1F
```

2. Process an image:

```python
path_media = "path/to/your/image.jpg"

# Extract datetime
ext, media_datetime, method = M1F.retrieve_datetime_of_single_media_files(path_media)

# Extract coordinates
lat_deg, lon_deg = M1F.extract_latitude_and_longitude_from_path_img(path_media)

# Get location information
if lat_deg is not None and lon_deg is not None:
    location = M1F.get_city_country_from_coordinates(lat_deg, lon_deg)
else:
    location = ('Unknown City', 'Unknown Country')

# Construct text to add to image
text = f'{media_datetime} | ({lat_deg:.3f}, {lon_deg:.3f}) | {location[0]}, {location[1]}'

# Add text to image
combined_img, msg_text = M1F.add_text_info_to_photo(path_media, text)
```

## Main Functions

- `retrieve_datetime_of_single_media_files(path_media)`: Extracts datetime from media file
- `extract_latitude_and_longitude_from_path_img(path_img)`: Extracts GPS coordinates from image
- `get_city_country_from_coordinates(lat, lon)`: Performs reverse geocoding
- `add_text_info_to_photo(path_img, text)`: Adds text to image

## Notes

- The script uses a custom file handling module `F02_File`. Ensure this module is in the correct path or adjust the import statement accordingly.
- Some functions require specific file paths. Adjust these paths according to your system setup.

## Author

Meng-Chi Ed Chen

## Status

Working

## Note (git push)
1. Navigate the terminal to the folder and `echo %cd%` to check.
2. Run the following codes in terminal one by one.
`git add .`
`git commit -m "Update readme"  `                      
`git push origin main`