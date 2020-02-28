import requests
import datetime
import xml.etree.ElementTree as ET
import re


def parsePage(xml):
    itemArray = ET.fromstring(xml).find(
        "ItemArray")
    ET.ElementTree(itemArray).write(xmlFile, encoding="UTF-8")
    # xmlFile.write(ET.tostring(itemArray))


def getXMLRes(pageNumber, startDate, toDate):
    print("        getting res for page %s" % pageNumber)
    xmlBody = """
    <?xml version="1.0" encoding="utf-8"?>
    <GetSellerListRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**pANEXg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GiD5CFpQudj6x9nY+seQ**gTcGAA**AAMAAA**ORWQ41/02/yFU6IGfhGDrFXd0sCi7KcCRk2R8JEZ7d+Yp3LqMCKTisVDRN/beL+oalSnK8/ym4Mg7Ncw8vyhj5a/91Fq/BUxdUZJ0Xcx0kW/KyVnf9GYhlaniQzTj2e+wkxi8WXCRcBSbypLvQkq5Bq4A3+4c9tTzKWAKHbjGn+hD/iu56T+ETvZKKRYchk7goD6+EynJ+SDtV/cKsrG9C/Q5JpnQRtiRPCO+d3j+7Z4tqqmt0hLhKt7OCmXisYHfo+X/IhcYtw4jpXpoO7TYLvocqhHH/B5WJvGKEPLua6KY2uNiNwOUnwWRmA/bmspGBqqoJCTRvxSJQIDcGECr5IMox0NyvT8Y+M1nJZfpoqS2EqUrKQA8ffLHfEF1DZwqnKSEnPVSVPywXgOqX3Ez/XjjawB5QuMu8RQHTK1gTB+Z5Kyp4T1QotZ0Wdmv3xT4/GR4NAB6ldCdFtLSz4+cCVIjz8H3ETv73s31sKSn02DNrT0KRRKkOnbQrBdGFOi3XtyNH6kUIcJtcBAo3pd9l5cW4YkY/hHENfgYFz9vyJ+wR8pBLYXvrHK4rRju1nMCBrSlkcL1Pi2JOyfpoKfxpzM8o7jjB/twoknjteY66hKCJc7Q1G2htIUn+PlLfSPmwYUNgbZx/K4MbvKeQFdpEyaujqT3FjZkwdljZpPjwRzzv3NTooEcbOgS99hX7PEP6t1kVWH3ePQGvH41c8LDPedpFvlq+IT2CTxozPA3W/9mQz6c/Jw60h2o+iH+8gO</eBayAuthToken>
    </RequesterCredentials>
	<ErrorLanguage>en_US</ErrorLanguage>
	<WarningLevel>High</WarningLevel>
    <DetailLevel>ReturnAll</DetailLevel>
    <IncludeWatchCount>true</IncludeWatchCount>
    <Pagination>
        <EntriesPerPage>200</EntriesPerPage>
        <PageNumber>""" + str(pageNumber) + """</PageNumber>
    </Pagination>
    <StartTimeFrom>""" + startDate + """</StartTimeFrom>
    <StartTimeTo>""" + toDate + """</StartTimeTo>
    </GetSellerListRequest>
    """
    return re.sub(' xmlns="[^"]+"', '', requests.post(
        urlToRequest, headers=headers, data=xmlBody).text, count=1)


def getDateRange(startDate, endDate):   # returns total number of entires for that date range
    startDateFormatted = startDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    toDateFormatted = endDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    print("    searching from " + startDate.strftime("%m/%d/%Y") +
          " to " + endDate.strftime("%m/%d/%Y"))

    # Get the XML response to determine number of pages and entires
    pageNumber = 1
    xmlString = getXMLRes(pageNumber, startDateFormatted, toDateFormatted)

    # Parse the XML and get data
    root = ET.fromstring(xmlString)
    numberOfPages = int(root.find("PaginationResult/TotalNumberOfPages").text)
    numberOfEntries = int(
        root.find("PaginationResult/TotalNumberOfEntries").text)
    print("            %s entries" % numberOfEntries)

    if numberOfEntries == 0:
        return numberOfEntries

    # parse the first page if there is one
    parsePage(xmlString)
    print("                got page 1")

    # return if there are no more pages
    if numberOfPages == 1:
        return numberOfEntries

    # parse remaining pages
    for page in range(2, numberOfPages+1):
        xmlString = getXMLRes(page, startDateFormatted,
                              toDateFormatted)  # get XML to a string
        parsePage(xmlString)
        print("                got page %s" % page)
    return numberOfEntries


def validateDate(input):
    try:
        return datetime.datetime.strptime(input, "%m/%d/%Y")
    except ValueError:
        raise ValueError("Date format was not correct. Should be mm/dd/yyyy.")


orgStartDate = validateDate(input("Enter start date (mm/dd/yyyy):\n"))
orgStartDateFormatted = orgStartDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")
endDate = validateDate(input("Enter end date (mm/dd/yyyy):\n"))
try:
    assert endDate >= orgStartDate
except AssertionError:
    raise AssertionError("End date is before start date.")
endDateFormatted = endDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")

fileName = "ebayData%s.xml" % datetime.datetime.now().strftime("%m-%d-%y-%H%M%S")
xmlFile = open(fileName, "wb")
urlToRequest = "https://api.ebay.com/ws/api.dll"
headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": "967", "X-EBAY-API-CALL-NAME": "GetSellerList",
           "X-EBAY-API-SITEID": "0", "Content-Type": "text/xml"}

totalNumberOfEntires = 0
for days in range(0, (endDate - orgStartDate).days, 121):
    print(str(days) + " days and " +
          str(totalNumberOfEntires) + " entries collected so far")

    # Open file as append
    xmlFile.close()
    xmlFile = open(fileName, "ab")

    # Determine dates: end date is 120 days after this iterations start date or specified end date, whichever is least
    startDate = orgStartDate + datetime.timedelta(days)
    toDate = min(startDate + datetime.timedelta(120), endDate)

    # Get the data for this date range
    totalNumberOfEntires += getDateRange(startDate, toDate)
