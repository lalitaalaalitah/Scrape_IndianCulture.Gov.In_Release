# Read Me

## Info

A website by Government of India contains many Rarebooks, Manuscripts and eBooks, etc.

This script is created to collect those books.

Rarebooks are more than 700 GB.
Manuscripts are more than 130 GB.
eBooks size is not known.

This script is created for practising python. Please, don't abuse the website. Use this script to download only needed items.


## How to Use

1. Create a new virtual environment, source it or add to shebang in the main script.
2. Install requests and bs4

        pip install requests

        pip install bs4

3. cd to the directory where script is located.
4. Run as

    a. this

        python ./v1_DownloadAllBooksFromIndianCultureGovIn_Release_270320221.py

    OR,

    b. make the script executable and then run directly. You must have your environment added to shebang.

        chmod +x ./v1_DownloadAllBooksFromIndianCultureGovIn_Release_270320221.py

        ./v1_DownloadAllBooksFromIndianCultureGovIn_Release_270320221.py

## Automatic download

For automating download of all three categories of PDF, i.e. rare books, manuscripts, eBooks ---

Replace

            download_this_category = input('do you want to download this category of PDF? yes(y), No(n)\n')

with

            download_this_category = 'y'


------------------

And for automating download of all PDF related to each category ---

Replace

        download_this_book = input('Do you want to download this book. Yes(y), No(n)?\n')

with

        download_this_book = 'y'