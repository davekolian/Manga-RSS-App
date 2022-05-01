[![Netlify Status](https://api.netlify.com/api/v1/badges/26fcc39c-ba88-4d2a-876f-f9fb1fe26de7/deploy-status)](https://app.netlify.com/sites/manga-rss-app/deploys)
![Heroku](https://heroku-badge.herokuapp.com/?app=heroku-badge)

# Manga RSS App

Manga RSS App is a web application that shows if any of the manga I (currently) read has any new chapters. It is now able to store the last read chapter and counts new chapters from the last read. Additionally, it shows the number of new chapters that you **have not read yet**. However, updating the last read chapter is manual and is done by pressing a button for each manga.

## How to use

- The app is currently live over on my [netlify](https://manga-rss-app.netlify.app/).

## How to build for yourself

- Coming soon

## How does it work

#### Web Scraper

1.  It uses Web Scraping technology to scrape Scanalation websites and check if any of the specified manga have released any new chapters recently.
2.  This web scraper runs every 10 minutes on an Oracle Cloud Instance where it populates the database.
3.  The web app the reads the the database and shows the data.

#### Backend

1.  With the help of Heroku and Mongoose I am able to read the data in the database.

#### Front-end

1.  Using React.js and Redux I am able to communicate with the backend part wherein I receive the data from the database
2.  I then display it on the screen with the help of JavaScript, HTML and CSS.

## Coming Soon

- Addition of a login system

## License

[MIT](https://github.com/davekolian/Manga-RSS-App/blob/master/LICENSE.txt)
