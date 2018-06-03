<img src="https://s3-eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2016/05/11170038/Instagram_Logo-1002x1003.jpg" width="200" align="right">

# Instagram-Crawler
Non API. Crawling post (photo, likes, comments, date ...) by username, hashtags

## Installation
1. Make sure you have Chrome browser installed.
2. Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) and put it into driver folder: `./driver/chromedriver`
3. Install requirements `pip install -r requirements.txt`

## Examples:
> Results: under the ./data folder

Download the first 10 photos and from username "instagram"
```
$ python3.6 crawl.py -q 'instagram' -n 10
```
Download the first 5 photos and from hashtags #hello, #hi
```
$ python3.6 crawl.py -q '#hello, #hi' -n 10
```
###### you can enter multiple username or hashtags by separating them with commas
### Example of a files data
```
likes: 
5,326

comments: 
923

message: 
Art of @kendricklamar by @illestration&#10;Bold, bright and colorful. 

commentMessages: 
tttt: Amazing 😉
this_is_t.rs: my name says it all

dateTime: 
2018-05-30T19:42:03.000Z
```
###### photo of post will download in ./data folder

## Usage
```
Usage:
    crawl.py [-q QUERY] [-n NUMBER] [-h HELP]
    
Options:
    -q QUERY  username, add '#' to search for hashtags, e.g. 'username' or '#hashtag'
                  For multiple query seperate with comma, e.g. 'username1, username2, #hashtag'

    -n NUM    number of returned posts [default: 10000]
    
    -h HELP   show this help message and exit
```
