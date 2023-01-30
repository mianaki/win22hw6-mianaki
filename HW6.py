import json
import unittest
import os
import requests

#
# Your name: Michaela
# Who you worked with: Tessa Voytovich
#

# generating personal API key is not requested here

def read_cache(CACHE_FNAME):
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict
   

def write_cache(CACHE_FNAME, CACHE_DICT):
    cache_data = json.dumps(CACHE_DICT)
    with open(CACHE_FNAME, 'w') as file:
        file.write(cache_data)
    

def create_request_url(term, number=1):
    request_url = f"https://itunes.apple.com/search?term={term}&limit={number}"
    return request_url

    
def get_data_with_caching(term, CACHE_FNAME):
    cache_dict = read_cache(CACHE_FNAME)
    url = create_request_url(term)
    if url in cache_dict:
        print(f"Using cache for {term}")
        return cache_dict[url]
    else:
        print(f"Fetching data for {term}")
        try:
            response = requests.get(url)
            data = json.loads(response.text)
            if data['resultCount'] == 1:
                cache_dict[url] = data['results'][0]
                write_cache(CACHE_FNAME, cache_dict)
            else:
                print('Request not set correctly')
                return None
        except:
            print('Exception')
            return None
    
        
def sort_price(CACHE_FNAME):
    '''
    Sorts a list of iTunes collections from
    the cache by price in ascending order, 
    returning the 5 most expensive products
    Parameters
    ----------
    CACHE_FNAME: str
        the name of the cache file to read from
    Returns
    -------
    tuple
        the name of the top 5 most expensive collections
        in the iTunes cache and its price like so:
        [('collection name', 0.0), ('collection name', 0.0)]
    '''
    tupple_list = []
    cache = read_cache(CACHE_FNAME)
    for dictionary in cache:
        price = cache[dictionary]['collectionPrice']
        collection = cache[dictionary]['collectionName']
        tupple_list.append((collection, price))
        top_5 = sorted(tupple_list, key = lambda x: x[1], reverse = True)[:5]
    return top_5


#######################################
############ EXTRA CREDIT #############
#######################################

def itunes_counts(CACHE_FNAME):
    '''
    Reads cache file and creates a dictionary
    with a genre name as the key and the number of 
    genre occurrences as the value, then sorts the
    dictionary in descending order, returning the 
    3 most frequent genres in the dict

    Parameters
    ----------
    CACHE_FNAME
        the name of the cache to read
    
    Returns
    -------
    dict
        a dict with the three most frequent genres 
        and their counts sorted in ascending order
    '''
    pass


####################
#### TEST CASES ####
####################

class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.CACHE_FNAME = dir_path + '/' + "cache_itunes.json"
        self.term_list = ["olivia+rodrigo", "ariana+grande", "drake", "tame+impala", "selena+gomez", "bruno+mars", "calvin+harris", "lorde", "imagine+dragons", "taylor+swift", "justin+bieber", "adele", "cage+the+elephant", "kanye+west", "britney+spears", "annavento", "ericayan"]
        self.cache = read_cache(self.CACHE_FNAME)

    def test_write_cache(self):
        write_cache(self.CACHE_FNAME, self.cache)
        dict1 = read_cache(self.CACHE_FNAME)
        self.assertEqual(dict1, self.cache)

    def test_create_request_url(self):
        for m in self.term_list:
            self.assertIn("term={}".format(m),create_request_url(m))
            self.assertIn("limit=1",create_request_url(m))
            self.assertNotIn("r=json",create_request_url(m))
            

    def test_get_data_with_caching(self):
        for m in self.term_list:
            dict_returned = get_data_with_caching(m, self.CACHE_FNAME)
            if dict_returned:
                self.assertEqual(type(dict_returned), type({}))
                self.assertIn(create_request_url(m),read_cache(self.CACHE_FNAME))
            else:
                self.assertIsNone(dict_returned)       
        self.assertEqual(json.loads(requests.get(create_request_url(self.term_list[0])).text)["results"][0],read_cache(self.CACHE_FNAME)[create_request_url(self.term_list[0])])

    def test_price(self):
        itunes_list = sort_price(self.CACHE_FNAME)
        self.assertEqual(type(itunes_list), type([]))
        self.assertEqual(len(itunes_list), 5)

    # def test_itunes_counts(self):
    #     self.assertEqual(itunes_counts(self.CACHE_FNAME), 
    #                     {'Pop': 6,
    #                      'Alternative': 3,    
    #                      'Biographies & Memoirs': 2
    #                     })
    #     pass

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_itunes.json"

    terms = ["olivia+rodrigo", "ariana+grande", "drake", "tame+impala", "selena+gomez", "bruno+mars", "calvin+harris", "lorde", "imagine+dragons", "taylor+swift", "justin+bieber", "adele", "cage+the+elephant", "kanye+west", "britney+spears", "annavento", "ericayan"]
    [get_data_with_caching(term, CACHE_FNAME) for term in terms]
    print("________________________")
    # Fetch the data for ColdPlay!
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('cold+play', CACHE_FNAME)
    data2 = get_data_with_caching('cold+play', CACHE_FNAME)
    print("________________________")

    # Getting the data for Post Malone!
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('post+malone', CACHE_FNAME)
    data2 = get_data_with_caching('post+malone', CACHE_FNAME)
    print("________________________")

    # Getting the data for The Beatles
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('the+beatles', CACHE_FNAME)
    data2 = get_data_with_caching('the+beatles', CACHE_FNAME)
    print("________________________")

    print("Get CollectionPrice for first 5 items")
    print(sort_price(CACHE_FNAME))
    print("________________________")


    # Extra Credit
    # Keep the statements commented out if you do not attempt the extra credit
    # print("EXTRA CREDIT!")
    # print("Analyzing the distribution of item genres")
    # # itunes_list() function does not take any parameters.
    # print(itunes_counts(CACHE_FNAME))
    # print("________________________")
    
 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    unittest.main(verbosity=2)