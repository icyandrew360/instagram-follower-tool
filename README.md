# instagram-follower-tool
Re-implements lost functionality from an old Instagram API endpoint. Since GET followers and GET following are now deprecated since 2016(?) and unusable, I've decided to implement them back for myself/anyone who requires that functionality.

Requirements: 
Firefox webdriver for selenium
selenium

Usage:

Create a .env file and populate it with the values from default.env. Please replace the placeholders with your own credentials to use.

In main, call the get_follower_details function. It will return 4 variables that are as named. Feel free to use those variables in whichever way you like.

Variables will be returned in a list of python dicts each with 2 keys: full_name and username.
