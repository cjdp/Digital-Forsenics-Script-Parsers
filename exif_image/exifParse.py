import sys
import exifread
from exif import Image
try:
    pictureFile = sys.argv[1]
    picture = Image(pictureFile)

    degreesLat, minutesLat, secondsLat = (
        round(picture.gps_latitude[0]), picture.gps_latitude[1], picture.gps_latitude[2])
    degreesLong, minutesLong, secondsLong = (
        round(picture.gps_longitude[0]), picture.gps_longitude[1], picture.gps_longitude[2])

    print("Source File: " + pictureFile)
    print("Make: " + picture.make)
    print("Model: " + picture.model)
    print("Original Date/Time: " + picture.datetime_original)
    print("Latitude: " + str(degreesLat) + " degrees, " +
          str(minutesLat) + " minutes, " + str(secondsLat) + " seconds")
    print("Longitude: " + str(degreesLong) + " degrees, " +
          str(minutesLong) + " minutes, " + str(secondsLong) + " seconds")

except ValueError:
    print("Error! - File Not Found!")
except IndexError:
    print("Error! - No Image File Specified!")
