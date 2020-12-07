    
if __name__ == '__main__':
    from bs4 import BeautifulSoup as soup  # HTML data structure
    from urllib.request import urlopen as uReq  # Web client
    
    # URl to web scrap from.
    page_url = "https://www.amazon.com.br/gp/bestsellers/books/ref=zg_bs_books_home_all?pf_rd_p=fee50879-7060-4905-a775-b7dff9daa54a&pf_rd_s=center-3&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=A1ZZFT5FULY4LN&pf_rd_r=E45R500ZD8S6175CM9DQ&pf_rd_r=E45R500ZD8S6175CM9DQ&pf_rd_p=fee50879-7060-4905-a775-b7dff9daa54a"
    
    # Opens the connection and download html and parse
    uClient = uReq(page_url)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    containers = page_soup.findAll("li", {"class": "zg-item-immersion"})
    
    # Create the .csv file
    out_filename = "most_selled_books_amazon.csv"
    headers = "Name, Author, Price \n"
    f = open(out_filename, "w")
    f.write(headers)
    
    # Create lists
    book_name = list()
    #author = list()
    price = list ()
    
    #debug
    '''
    test = containers[0]
    print (test)
    '''
    
    for container in containers:
        book_name.append(container.span.div.a.text.strip())
        #author.append(container.)
        price.append(container)
    
    j = 1 
    for i in book_name:
        print(str(j)+ ' - ' + i)
        j +=1
        f.write( i + "\n")
    
    f.close()  # Close the file

