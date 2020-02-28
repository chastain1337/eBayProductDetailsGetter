eBay Product Details Getter

This app was created as an alternative to the now discontinued TurboLister, built for those with large eBay catalogues in mind. The program has been tested successfully on a date range containing 110,000 listings.

You will need an eBay developers account to generate a production User Token using Auth’n’Auth. You will have to supply the program with this token.

Downloading and Usage:
-	To use the standalone executable, copy only “target/eBay_Product_Details_Getter” to your machine and launch “eBay_Product_Details_Getter.exe”
-	Supply the user token, date range, and folder where the file will be saved.
-	Click “Get Product Details”


Features:
-	Downloads all product data, even the full description and stuff you don’t care about
-	Will still fetch all listings, but filter our non-English listings, so if you have WebInterpret turned on, you will only get your real listings, not their interpreted variations
-	You can specify any date range, but the program will fetch data in ranges of up to 120 days (max set by eBay), and pages of max 200 products each
-	Writes to an XML file when it is finished
-	It is recommended to use Excel’s PowerQuery to import the XML and convert to spreadsheet or .csv