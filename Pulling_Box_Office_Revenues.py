#!/usr/bin/env python
# coding: utf-8

# In[1]:


def Pull_Box_Office_Revenues():    
    # Import necessary packages
    from bs4 import BeautifulSoup
    import requests
    import re
    import pandas as pd
    from time import sleep
    from random import randint
    
    # Set fixed values
    num_pages = 5
    offset_val = 200
    
    # Set counter variable
    offset_count = 0
    
    # Set dummy variables
    rankings = []
    titles = []
    lifetime_gross = []
    year = []
    
    # Loop through pages
    while offset_count < num_pages * offset_val:
        
        # Set URL for each page equal to response
        if offset_count == 0:
            response = requests.get('https://www.boxofficemojo.com/chart/top_lifetime_gross/')
        else:
            response = requests.get('https://www.boxofficemojo.com/chart/top_lifetime_gross/?offset=' + str(offset_count))
        
        # Pause the loop
        sleep(randint(8,15))
        
        # Parse the content using BeautifulSoup
        Box_office_soup = BeautifulSoup(response.content, 'html.parser')
        
        # Add values to the ranking list
        rank_find_all = Box_office_soup.find_all(class_='a-text-right mojo-header-column mojo-truncate mojo-field-type-rank')
        rankings.extend([r.text for r in rank_find_all])
        
        # Add values to the titles list
        movie_name_find_all = Box_office_soup.find_all(class_='a-text-left mojo-field-type-title')
        titles.extend([r.text for r in movie_name_find_all])
        
        # Add values to the lifetime_gross list
        lifetime_gross_find_all = Box_office_soup.find_all(class_='a-text-right mojo-field-type-money')
        lifetime_gross.extend([r.text[1:] for r in lifetime_gross_find_all])
        
        # Add values to the years list
        year_find_all = Box_office_soup.find_all(class_='a-text-left mojo-field-type-year')
        year.extend([r.text for r in year_find_all])
        
        # Move on to the next page
        offset_count += 200
        
    # Create the box office database
    Box_office_db = pd.DataFrame([rankings, titles, lifetime_gross, year]).transpose()
    Box_office_db.columns = (['Rank', 'Title', 'Lifetime Gross', 'Year'])
    Box_office_db.set_index('Rank', inplace = True)
    return Box_office_db        

