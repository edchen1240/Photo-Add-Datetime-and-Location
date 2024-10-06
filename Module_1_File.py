"""
[Module_1_Blank_Module_One.py]
Purpose: 
Author: Meng-Chi Ed Chen
Date: 
Reference:
    1.
    2.

Status: Working.
"""
import os, sys, cv2, re
import numpy as np
import pandas as pd
from tabulate import tabulate
import exifread
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import UnidentifiedImageError, Image, ExifTags
import reverse_geocoder as rg


sys.path.insert(1, r'D:\01_Floor\a_Ed\09_EECS\10_Python\00_Classes and Functions')
import F02_File as F02_File # type: ignore



def retrieve_datetime_of_single_media_files(path_media):
    #[2] Get file extension
    bsn_ext = os.path.basename(path_media)
    print(f'\t-- Processing: {bsn_ext}')
    bsn, ext = os.path.splitext(bsn_ext)
    ext = ext.upper()
    
    #[3] Check file type for image
    if ext in ['.JPG', '.JPEG', '.PNG', '.GIF']:
        try:
            media_datetime = datetime.strptime(Image.open(path_media)._getexif()[36867], 
                                                '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d, %H:%M:%S')
            method = '[1] get_date_taken'
        except (KeyError, UnidentifiedImageError, TypeError, AttributeError):
            media_datetime = datetime.fromtimestamp(os.path.getmtime(path_media)).strftime('%Y-%m-%d, %H:%M:%S')
            method = '[2] os.path.getmtime(image)'
    
    #[4] Check file type for video
    elif ext in ['.MP4', '.MOV']:
        media_datetime = datetime.fromtimestamp(os.path.getmtime(path_media)).strftime('%Y-%m-%d, %H:%M:%S')
        method = '[3] os.path.getmtime(video)'
    
    #[5] Handle unknown file types
    else:
        media_datetime, method = None, None
        print(f'Unknown file type {bsn_ext}, usually AEE.')
    
    return ext, media_datetime, method



def convert_to_degrees(value):
    #[2.1] Helper function to convert GPS coordinates to decimal degrees.
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def extract_latitude_and_longitude_from_path_img(path_img):
    #[1] Extract GPS info from EXIF of the image.
    bsn_img = os.path.basename(path_img)
    with open(path_img, 'rb') as file_img:
        tags = exifread.process_file(file_img)
        lat_ref = tags.get('GPS GPSLatitudeRef')
        lat = tags.get('GPS GPSLatitude')
        lon_ref = tags.get('GPS GPSLongitudeRef')
        lon = tags.get('GPS GPSLongitude')

        #[1.1] Convert latitude and longitude to decimal degrees.
        if lat and lon:
            lat_deg = convert_to_degrees(lat)
            if lat_ref.values != 'N':
                lat_deg = -lat_deg
            lon_deg = convert_to_degrees(lon)
            if lon_ref.values != 'E':
                lon_deg = -lon_deg
            return lat_deg, lon_deg
        else:
            print(f'No GPS information found in the image: {bsn_img}')
            return None, None

def get_city_country_from_coordinates(lat, lon):
    #[3] Extract city and country from coordinates using reverse geocoding.
    coordinates = (lat, lon)
    try:
        result = rg.search(coordinates)
        if result:
            city = result[0].get('name', 'Unknown City')
            country = result[0].get('cc', 'Unknown Country')
            return city, country
        else:
            print(f'No results found for coordinates: {coordinates}')
            return None, None
    except Exception as e:
        print(f'Error during reverse geocoding: {e}')
        return None, None









def replace_pattern_in_filename_and_save(dir_img, bsn_ext, new_tag, arrimg):
    """
    Replace the _(*). pattern in the filename with a new tag.
    If pattern cannot be found, add f'_{new_tag}' just before the file ext.
    """
    #[1] Split the base name and extension
    bsn, ext = os.path.splitext(bsn_ext)
    
    #[2] Regular expression to match the _(*) pattern
    pattern = r'\_\([^)]+\)$'  # This matches _ followed by ( and any characters except ) until ) at the end
    
    #[3] Check if the pattern exists and is properly formatted
    match = re.search(pattern, bsn)
    if match:
        #[4] Replace the matched pattern with the new tag
        new_bsn_ext = f'{re.sub(pattern, f"_({new_tag})", bsn)}{ext}'
    else:
        #[5] Append the new tag if pattern is not found
        new_bsn_ext = f'{bsn}_({new_tag}){ext}'
    
    #[8] Save image.
    path_img = os.path.join(dir_img, new_bsn_ext)
    cv2.imwrite(path_img, arrimg)

    return path_img

def add_text_info_to_photo(path_img, text, tag_adtx='1-text'):
    #[1] Load the image.
    arr_img = cv2.imread(path_img)
    dir_img = os.path.dirname(path_img)
    bsn_ext = os.path.basename(path_img)
    height, width, channels = arr_img.shape
    msg_text = ''
    print(f'\n[crop_image_center_square] Processing image: {bsn_ext}')
    
    #[2] Check image size.
    if height < 400 or width < 400:
        text_img_too_small = f'-- The scale of the image is too small ({height}, {width}) and text might not be readable.'
        print(text_img_too_small)
        msg_text += f'{text_img_too_small}\n'
    
    #[4] Image scale settings.
    text_space_ratio = 0.03
    font_scale = round(2 * height/3800, 2)
    font_thk_int = int(6 * height/3600)
    text_font = f'-- Font (font_scale, font_thk_int) = ({font_scale}, {font_thk_int})'
    print(text_font)
    msg_text += f'{text_font}\n'
    
    #[5] Check if image exist.
    if arr_img is None:
        raise FileNotFoundError(f"Image at {path_img} could not be loaded.")

    #[7] Increase the bottom by 100 pixels with a white background.
    increased_height = int(height * text_space_ratio)
    new_height = height + increased_height
    white_background = np.full((increased_height, width, 3), 255, dtype=np.uint8)  # White background
    text_resize = f'-- Old ({height} x {width}), New ({new_height} x {width}), H diff {increased_height}'
    print(text_resize)
    msg_text += f'{text_resize}\n'

    #[9] Combine the original image and white background.
    combined_img = np.vstack((arr_img, white_background))

    #[10] Add black text.
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thk_int)
    text_x = (width - text_size[0]) // 2  # Center text horizontally
    text_y = int(height + 0.6 * increased_height)  # Place text in the middle of the added white background

    #[12] Save the cropped image.
    cv2.putText(combined_img, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thk_int)
    replace_pattern_in_filename_and_save(dir_img, bsn_ext, tag_adtx, combined_img)

    return combined_img, msg_text






















