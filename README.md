# Manga RSS App
 Manga RSS App is a Desktop application that shows if any of the manga I (currently) read has any new chapters.
 
 ## Installation
   * Navigate to Manga-UI/webParse.zip (https://github.com/davekolian/Manga-RSS-App/raw/master/Manga-UI/webParse.zip) and download the zip file.
   * Extract the file and navigate to /dist/webParse
   * Run webParse.exe to run the code
   
## How does it work
   * It uses Web Scraping technology to scrape Scanalation websites and check if any of the specified manga have released any new chapters recently.
   * Then it updates the data on MongoDB.
   * The webParse.exe then reads from the database and uses Kivy UI to display the data cleanly.
   
## Coming Soon
   * Addition of a login system
   * Better system to check what's read for the UI
   
## License
   [MIT](https://github.com/davekolian/Manga-RSS-App/blob/master/LICENSE.txt)
