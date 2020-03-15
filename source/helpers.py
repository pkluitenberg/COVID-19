#!/usr/bin/env python

####################################################################################################
# Title: helpers.py                                                                                #
# Purpose: Provides a variety of functions to be called in the covid19.ipynb notebook              #
# Author: Paul Kluitenberg                                                                         #
# Last Modified: 03/15/2020                                                                        #
# Functions: dir_df: returns a dataframe of files in a directory                                   #
#            from_url: downloads file from URL specified to directory                              #
#            scrape_link: scrapes webpage for a download link to a specific file type              #
####################################################################################################

def dir_df(dir: str):
    """
    This function returns a dataframe with the file names, sizes, and paths from a provided directory.
    """
    
    # begin import modules
    import pandas as pd
    import os
    # end import modules
    
    # confirm that the directory provided actually exists
    try:
        dir_lst = os.listdir(dir)
    except:
        return "Directory provided does not exist"
    
    # convert the list of files into a dataframe
    dir_df = pd.DataFrame(dir_lst, columns=["FILE_NAME"])
    
    # add in file path and file size
    dir_df['FILE_PATH'] = dir + "/" + dir_df['FILE_NAME']
    dir_df['FILE_SIZE'] = dir_df['FILE_PATH'].apply(os.path.getsize)
    
    return dir_df

def from_url(url:str, dest:str, overwrite=False, make_dir=False):
    """
    This function takes a url, downloads the file from the url, and saves it to the destination provided.
    Additionally, you can choose to have it overwrite an existing file and you can have it choose to make
    the directory if it currently does not exist.
    """
    
    # begin import modules
    import wget
    import os
    # end import modules
    
    # bind static variables
    BASE_DIR, FILE_NAME = os.path.split(dest)
    
    # check if the directory exsits
    if not os.path.isdir(BASE_DIR):
        print("File destination does not exist")
        # create the directory if it does not exist and make_dir is set to True. Else return without downloading file.
        if make_dir:
            print("make_dir set to True, making directory: ", BASE_DIR)
            try:
                os.makedirs(BASE_DIR)
            except:
                print("Could not make directory")
        else:
            return("""Directory will not be created and file not downloaded. 
                      Please set make_dir to True to create directory""")
    else:
        pass
    
    # confirm that the path exists and download file depending on the overwite state
    if os.path.exists(dest):
        if overwrite:
            try:
                wget.download(url,dest)
            except:
                return("File could not be downloaded. Check URL")
            return("File downloaded to the following location: " + dest)
        else:
            return("File not downloaded because overwrite set to False")
    else:
        try:
            wget.download(url,dest)
        except:
            return("File could not be downloaded. Check URL")
        return("File downloaded to the following location: ", dest)
    
def scrape_link(url:str, file_type:str):
    """
    This function takes a url and scrapes all hrefs from the HTML that have a given file type in them.
    The function returns the hrefs as a list.
    """
    
    # begin import modules
    import requests
    from bs4 import BeautifulSoup
    # end import modules
    
    # HTTP request to URL and storing data in object 'page'
    page = requests.get(url)
    
    # create beautiful soup object
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # search through hrefs to link to specified file(s)
    ref_lst = [a['href'] for a in soup.find_all('a',href=True) if file_type in a['href']]
    
    return ref_lst

