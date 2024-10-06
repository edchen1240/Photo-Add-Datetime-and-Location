"""
[BLK-0_sandbox.py]
Purpose: 
Author: Meng-Chi Ed Chen
Date: 
Reference:
    1.
    2.

Status: Working.
"""
import os, sys, cv2
import Module_1_File as M1F

#path_media = r'D:\01_Floor\a_Ed\09_EECS\10_Python\04_OngoingTools\2024-1005_Photo Add Datetime and Location\PDL-01_Test image\IMG_0952.JPG'
#path_media = r'D:\01_Floor\a_Ed\09_EECS\10_Python\04_OngoingTools\2024-1005_Photo Add Datetime and Location\PDL-01_Test image\IMG_0360_600x450.JPG'
path_media = r'D:\01_Floor\a_Ed\09_EECS\10_Python\04_OngoingTools\2024-1005_Photo Add Datetime and Location\PDL-01_Test image\2024-0131_The Yale Bookstore_3024x4032_(info removed).JPG'


if __name__ == "__main__":
    #[4] Extract datetime.
    ext, media_datetime, method = M1F.retrieve_datetime_of_single_media_files(path_media)
    print(f'ext:            \t{ext}')
    print(f'media_datetime: \t{media_datetime}')
    print(f'method:         \t{method}')

    #[5] Extract coordinates.
    lat_deg, lon_deg = M1F.extract_latitude_and_longitude_from_path_img(path_media)
    print(f'lat_deg:   \t{lat_deg}')
    print(f'lon_deg:  \t{lon_deg}')

    #[6] Extract location.
    if lat_deg is not None and lon_deg is not None:
        location = M1F.get_city_country_from_coordinates(lat_deg, lon_deg)
        print(f'location: \t{location}')
    else:
        location = ('Unknown City', 'Unknown Country')
        print("GPS coordinates could not be extracted.")
    
    #[8] Ensure proper formatting and handling of None values for coordinates
    if lat_deg is not None and lon_deg is not None:
        coord_text = f'({lat_deg:.3f}, {lon_deg:.3f})'
    else:
        coord_text = '(No Coordinates)'

    #[10] Construct the final text with all the extracted information
    text = f'{media_datetime} | {coord_text} | {location[0]}, {location[1]}'
    print(text)

    #[15] Add datetime.
    combined_img, msg_text = M1F.add_text_info_to_photo(path_media, text)
    print(f'[msg_text]\n {msg_text}')














