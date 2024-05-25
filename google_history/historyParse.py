import sys
import sqlite3
import ntpath
from datetime import datetime

try:
    historyFileInput = sys.argv[1]
    historyFile = sqlite3.connect(historyFileInput)
    cursor = historyFile.cursor()

    totalDownloads = (cursor.execute('select count(id) from downloads'))
    totalDownloadsResult = totalDownloads.fetchone()[0]

    fileName = cursor.execute(
        'select current_path, max(end_time-start_time) from downloads')
    fileNameResult = fileName.fetchone()[0]
    finalFileNameResult = ntpath.basename(fileNameResult)

    fileSize = cursor.execute(
        'select total_bytes, max(end_time-start_time) from downloads')
    fileSizeResult = fileSize.fetchone()[0]

    uniqueTerms = cursor.execute(
        'select count (distinct term) from keyword_search_terms')
    uniqueTermsResult = uniqueTerms.fetchone()[0]

    mostRecSearch = cursor.execute(
        'select lower_term, max(url_id) from keyword_search_terms')
    mostRecSearchResult = mostRecSearch.fetchone()[0]

    # match visits.url and MAX keyword_search_terms.url_id(408)
    mostRecSearchTime = cursor.execute(
        "select visits.visit_time from visits inner join (select max(url_id) as max_url_id from keyword_search_terms) as max_url on visits.url = max_url.max_url_id")
    mostRecSearchTimeResult = mostRecSearchTime.fetchone()[0]
    timestamp = (mostRecSearchTimeResult / 1000000) - 11644473600
    date_time = datetime.fromtimestamp(timestamp).strftime("%Y-%b-%d %H:%M:%S")

    print("Source File: " + str(historyFileInput))
    print("Total Downloads: " + str(totalDownloadsResult))
    print("File Name: " + str(finalFileNameResult))
    print("File Size: " + str(fileSizeResult))
    print("Unique Search Terms: " + str(uniqueTermsResult))
    print("Most Recent Search: " + str(mostRecSearchResult))
    print("Most Recent Search Date/Time: " +
            str(date_time))

except IndexError:
    print("Error! - No History File Specified!")
except ValueError:
    print("Error! - File Not Found!")
except sqlite3.OperationalError:
    print("Error! - File Not Found!")