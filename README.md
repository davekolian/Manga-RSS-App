# Manga RSS App
 Manga RSS App is a Web application that shows if any of the manga I (currently) read has any new chapters.
 
 ## How to use
  * The app is currently live over on my [netlify](https://manga-rss-app.netlify.app/).
   
## How does it work

 #### Web Scraper
   1. It uses Web Scraping technology to scrape Scanalation websites and check if any of the specified manga have released any new chapters recently.
   2. This web scraper runs every 10 minutes on an Oracle Cloud Instance where it populates the database.
   3. The web app the reads the the database and shows the data.
 
 #### Backend
   1. With the help of Heroku and Mongoose I am able to read the data in the database.


 #### Front-end
 1. Using React.js and Redux I am able to communicate with the backend part wherein I receive the data from the database
 2. I then display it on the screen with the help of JavaScript, HTML and CSS.

   
## Coming Soon
   * Addition of a login system
   * Better system to check what's read for the UI
   
## License
   [MIT](https://github.com/davekolian/Manga-RSS-App/blob/master/LICENSE.txt)
