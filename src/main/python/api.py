import requests
import datetime
import xml.etree.ElementTree as ET
import re


def validateDate(input):
    try:
        return datetime.datetime.strptime(input, "%m/%d/%Y")
    except ValueError:
        raise ValueError("Date format was not correct. Should be mm/dd/yyyy.")


def handleClick(app):
    newTree = ET.Element("ItemArray")

    def parsePage(xml, numberOfEntries):
        # Pull out just the US stores and add them to the newTree
        itemArray = ET.fromstring(xml).find("ItemArray")
        nonlocal entriesInThisRangeSearched
        nonlocal totalNumberOfEntiresPulled
        for elem in itemArray:
            # Entries searched is not the same as entires pulled. Only pulling US entires, but keeping track of both.
            entriesInThisRangeSearched += 1
            if elem.find("Site").text == "US":
                totalNumberOfEntiresPulled += 1
                newTree.append(elem)
        app.status_numberofEntries.setText("%s out of %s entrie(s) in this range." % (
            entriesInThisRangeSearched, numberOfEntries))
        app.status_totalNumberOfEntries.setText(
            "Pulled %s English entires so far." % totalNumberOfEntiresPulled)

    def getXMLRes(pageNumber, startDate, toDate):
        xmlBody = """
        <?xml version="1.0" encoding="utf-8"?>
        <GetSellerListRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
            <eBayAuthToken>%s</eBayAuthToken>
        </RequesterCredentials>
        <ErrorLanguage>en_US</ErrorLanguage>
        <WarningLevel>High</WarningLevel>
        <DetailLevel>ReturnAll</DetailLevel>
        <IncludeWatchCount>true</IncludeWatchCount>
        <Pagination>
            <EntriesPerPage>200</EntriesPerPage>
            <PageNumber>%s</PageNumber>
        </Pagination>
        <StartTimeFrom>%s</StartTimeFrom>
        <StartTimeTo>%s</StartTimeTo>
        </GetSellerListRequest>
        """ % (token, pageNumber, startDate, toDate)
        res = requests.post(
            urlToRequest, headers=headers, data=xmlBody)
        if res.status_code != 200:
            raise Exception(
                "The XML Reponse returned a status code of %s" % res.status_code)

        xmlString = re.sub(' xmlns="[^"]+"', '', res.text, count=1)
        return xmlString

    def getDateRange(startDate, endDate):
        app.status_numberofEntries.setText(
            "Checking total entries and pages for date range.")
        app.status_pageNumber.setText("")
        startDateFormatted = startDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        toDateFormatted = toDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        # Get the XML response of first page to determine number of pages and entires
        pageNumber = 1
        xmlResponseString = getXMLRes(
            pageNumber, startDateFormatted, toDateFormatted)

        # We know status code == 200, validate that response is XML and it was successful.

        # Parse the XML
        root = ET.fromstring(xmlResponseString)

        if (root.find("Ack").text == "Failure"):
            raise Exception("The data received contained an error: %s" %
                            root.find("Errors").find("ShortMessage").text)

        numberOfPages = int(
            root.find("PaginationResult/TotalNumberOfPages").text)
        numberOfEntries = int(
            root.find("PaginationResult/TotalNumberOfEntries").text)

        app.status_numberofEntries.setText("%s out of %s entrie(s) in this range." % (
            entriesInThisRangeSearched, numberOfEntries))

        if numberOfEntries == 0:
            return

        app.status_pageNumber.setText("Parsing page 1")
        # parse the first page if there is one
        parsePage(xmlResponseString, numberOfEntries,)

        # return if there are no more pages
        if numberOfPages == 1:
            return

        # parse remaining pages
        for page in range(2, numberOfPages+1):
            app.status_pageNumber.setText("Parsing page %s" % page)
            xmlResponseString = getXMLRes(page, startDateFormatted,
                                          toDateFormatted)  # get XML to a string
            parsePage(xmlResponseString, numberOfEntries)
        return

    # ========================================================================
    # ========================================================================
    # ========================================================================
    try:
        token = app.tokenInput.toPlainText()

        if token == "":
            raise Exception("No Token provided.")

        orgStartDate = datetime.datetime.strptime(
            app.startDatePicker.text(), "%m/%d/%Y")
        #startDateFormatted = orgStartDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        endDate = datetime.datetime.strptime(
            app.endDatePicker.text(), "%m/%d/%Y")

        try:
            assert endDate >= orgStartDate
        except AssertionError:
            raise AssertionError("End date is before start date.")

        #endDateFormatted = endDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        fileName = "%s/ebayData%s.xml" % (
            app.folder, datetime.datetime.now().strftime("%m-%d-%y-%H%M%S"))
        urlToRequest = "https://api.ebay.com/ws/api.dll"
        headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": "967", "X-EBAY-API-CALL-NAME": "GetSellerList",
                   "X-EBAY-API-SITEID": "0", "Content-Type": "text/xml"}

        totalNumberOfEntiresPulled = 0

        for days in range(0, (endDate - orgStartDate).days, 121):
            entriesInThisRangeSearched = 0

            # Determine dates: end date is 120 days after this iteration's start date or specified end date, whichever is least
            startDate = orgStartDate + datetime.timedelta(days)
            toDate = min(startDate + datetime.timedelta(120), endDate)

            # Get the data for this date range
            app.status_dateRange.setText("Currently searching %s to %s" % (startDate.strftime(
                "%m/%d/%Y"), toDate.strftime("%m/%d/%Y")))
            getDateRange(startDate, toDate)

        # Write new XML tree to a file
        ET.ElementTree(newTree).write(fileName, encoding="UTF-8")
        app.status_dateRange.setText("Finished")
        app.status_numberofEntries.setText("")
        app.status_pageNumber.setText("")
        app.status_totalNumberOfEntries.setText("")
        app.getButton.setDisabled(False)

    except Exception as e:
        app.errorMessage.setText("An error has occured:\n%s" % e)
        app.getButton.setDisabled(False)
