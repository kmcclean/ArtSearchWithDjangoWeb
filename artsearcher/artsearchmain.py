from bs4 import BeautifulSoup
from urllib import request
from artsearcher.Art import Art
import re


class ArtSearcher:

    def art_search(self, search_term):

        # This is where the user inputs what they would like to search for.
        search_terms_dashes_for_spaces = self.search_term_converter(search_term, "-")
        search_term_percent_encoding_for_spaces = self.search_term_converter(search_term, "%20")

        # This creates a list of the art pieces for each of the museums
        amaa_list = self.create_amaa_object(search_terms_dashes_for_spaces)
        walker_list = self.create_walker_art_object(search_term_percent_encoding_for_spaces)
        mia_list = self.create_mia_art_object(search_term_percent_encoding_for_spaces)

        # This is where the list that is returned is created.
        master_list = []
        for item in amaa_list:
            master_list.append(item)
        for item in walker_list:
            master_list.append(item)
        for item in mia_list:
            master_list.append(item)
        return master_list

    # This is where a dictionary entry for each artist is created, with their number of appearances at museums counted.
    def artist_name_appearances(self, museum_list, artist_dictionary):
        for artist_name in museum_list:
            # http://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python-3-3
            if artist_name.artist in artist_dictionary.keys():
                times = artist_dictionary[artist_name.artist]
                times += 1
                artist_dictionary[artist_name.artist] = times
            else:
                artist_dictionary[artist_name.artist] = 1

        return artist_dictionary

    # this takes the search term and turns it into something that can be used by websites.
    def search_term_converter(self, term, new_phrase):
        remade_term = term.replace(" ", new_phrase)
        return remade_term

    # This creates an art object for the American Museum of Asmat Art.
    def create_amaa_object(self, seach_term):

        titles = []
        artist_possibles_list = []
        image_link = []
        artist_list = []
        amaa_results = []

        # This is the base search url for the American Museum of Asmat Art searh
        soup_url = "http://artsatust.museumssites.com/collections/search-the-collections/search/search:" + seach_term

        # Because the website requires a AMAA website breaks up the information into pages, this runs a loop until it runs out of returned pages.
        while True:
            soup_amaa1 = BeautifulSoup(request.urlopen(soup_url), 'html.parser')

            # This checks to see if any records were returned. If they weren't it breaks the loop right away.
            for records_check in soup_amaa1.find_all(attrs={"class": "body_text"}):
                soupy = BeautifulSoup(repr(records_check), 'html.parser')
                stripped_soupy = str(soupy.string).strip()
                if (stripped_soupy == "No records to display"):
                    break

            # This gets the title of the artwork
            for item1 in soup_amaa1.find_all(attrs={"class": "hlink"}):
                soup_amaa2 = BeautifulSoup(repr(item1), 'html.parser')
                if(soup_amaa2.string != "Contact us"):
                    titles.append(soup_amaa2.string)

            # This gets a list of possible artists to work through.
            for item in soup_amaa1.find_all(attrs={"id": "main_body"}):
                soup = BeautifulSoup(repr(item), 'html.parser')
                for item2 in soup.find_all("ul"):
                    soup1 = BeautifulSoup(repr(item2), 'html.parser')
                    for item3 in soup1.find_all("li", ""):
                            artist_possibles_list.append(item3)

            # This takes the list of possibles, and uses the number of titles generated to determine the names of the artists.
            # Since the names come at the end, it has to work from the back of the list
            artist_length = -1 * len(titles)
            artist_name_list = artist_possibles_list[artist_length:]
            for artist in artist_name_list:
                artist = str(artist).strip("<li>")
                artist = artist.strip("</")
                artist = artist.strip(" ")
                if "," in artist:
                    artist = artist[:artist.index(",")]

                artist = self.check_for_amaa_errors(artist)
                artist_list.append(artist)

            # This gets the url for the image from the HTML that is pulled.
            for item5000 in soup_amaa1.find_all(attrs={"class": "thumbnail"}):
                soup_amaa = BeautifulSoup(repr(item5000), 'html.parser')
                for item100 in soup_amaa.find_all("img"):
                    url = "http://artsatust.museumssites.com" + item100.get("src")
                    image_link.append(url)

            # This is a check to see if the loop is finished.
            # The website has certain markers that show up when it is finished running through the returned responses.
            # If this hits one of those, it breaks the loop.
            next_disable_list = soup_amaa1.find_all(attrs={"class": "next disable"})
            next_list = soup_amaa1.find_all(attrs={"class": "next"})
            if len(next_disable_list) != 0:
                break
            elif len(next_list) != 0:
                for item in soup_amaa1.find_all(attrs={"class":"next"}):
                    soup_thing = BeautifulSoup(repr(item), 'html.parser')
                    for item2 in soup_thing.find_all("a"):
                        soup_url = item2.get("href")
            else:
                break

            amaa_results = self.create_amaa_results(titles, artist_list, image_link)
            return amaa_results

    # This takes all the art pieces that have been found and creates an art object for each one.
    def create_amaa_results(self, titles, artist_list, image_link):
        results = []
        counter = 0
        while counter < len(titles):
            a = Art(titles[counter], artist_list[counter], "Years Not Provided by AMAA", image_link[counter], "American Museum-Asmat Art")
            results.append(a)
            counter += 1
        return results

    # There are some of the AMAA artists that are not collected correctly. This take care of those.
    def check_for_amaa_errors(self, artist):
        check = re.match('<li>(.*)</li>', artist)
        if check:
            return check
        else:
            return artist

    # this searches the Minneapolis Institute of Art, and creates an art objects
    # for pieces that are returned as searches.
    def create_mia_art_object(self, search_term):
        soup_mia1 = BeautifulSoup(request.urlopen("http://collections.artsmia.org/search/" + search_term), 'html.parser')
        meta_list_of_art_data = []
        art_url_list = []
        mia_art_list = []

        # this uses the body of the returned HTML to find information on the
        for item in soup_mia1.find_all("body"):

            art_item_total = 0
            soup_mia2 = BeautifulSoup(repr(item), 'html.parser')
            for item1 in soup_mia2.find_all("figcaption"):
                title = ""
                date = ""
                span_counter = 0
                name = ""

                # This is where the program gets the date and the title of the piece.
                soup_mia3 = BeautifulSoup(repr(item1), 'html.parser')
                for item2 in soup_mia3("span"):
                    soup_mia4 = BeautifulSoup(repr(item2), 'html.parser')
                    if span_counter == 0:
                        title = soup_mia4.string
                    elif span_counter == 2:
                        date = soup_mia4.string
                    span_counter += 1

                # This gets the name of the artist who created the piece
                for item3 in soup_mia3.find_all("p"):
                    soup_mia5 = BeautifulSoup(repr(item3), 'html.parser')
                    for item4 in soup_mia5.find_all("em"):
                        soup_mia6 = BeautifulSoup(repr(item4), 'html.parser')
                        name += soup_mia6.string + " "

                # Once all of this has been collected, a metadata list is created so that all of an individual piece's
                # are kept together.
                stripped_name = name.strip()
                list_of_art_data=[str(title), str(date), str(stripped_name)]
                meta_list_of_art_data.append(list_of_art_data)
                art_item_total += 1

            # This gets the url for the image to the piece.
            for item4 in soup_mia2.find_all("img"):
                art_url_list.append(item4.get("src"))

            # This is to cover for any situation where a link is not available for a piece of art (they are listed at
            # the end of searches on the MIA website).
            while art_item_total != len(art_url_list):
                art_url_list.append("No link available")

        # This is where Art objects from the MIA are created.
        list_counter = 0
        for art_list in meta_list_of_art_data:
            art_list.append(art_url_list[list_counter])
            m = Art(art_list[0], art_list[2], art_list[1], art_list[3], "Minneapolis Institute of Art")
            list_counter += 1
            mia_art_list.append(m)

        return mia_art_list

    # This creates art objects for search responses from the Walker Art Center.
    def create_walker_art_object(self, search_term):

        titles = []
        artists = []
        years = []
        image_links = []
        list_of_walker_art = []

        # This starts the loops to iterate over the information from the Walker Art Center's collection results.
        soup_walker1 = BeautifulSoup(request.urlopen("http://www.walkerart.org/collections/browse?q=" + search_term), 'html.parser')
        for item in soup_walker1.find_all("body"):
            soup_walker2 = BeautifulSoup(repr(item), 'html.parser')

            # This gets the titles of the pieces.
            for item2 in soup_walker2.find_all(attrs={"class":"title ellipsis"}):
                soup_walker3 = BeautifulSoup(repr(item2), 'html.parser')
                titles.append(soup_walker3.string)

            # This gets the artists of the pieces.
            for item3 in soup_walker2.find_all(attrs={"class": "artist"}):
                soup_walker4 = BeautifulSoup(repr(item3), 'html.parser')
                artist_stripped = str(soup_walker4.string).strip()
                artists.append(artist_stripped)

            # This gets the years the painting was created.
            for item4 in soup_walker2.find_all(attrs={"class": "year"}):
                soup_walker5 = BeautifulSoup(repr(item4), 'html.parser')
                years.append(soup_walker5.string)

            # This gets the images link that will be used to show the image of the artwork.
            for item5 in soup_walker2.find_all(attrs={"class" : "grid_view"}):
                soup_walker6 = BeautifulSoup(repr(item5), 'html.parser')
                for item5 in soup_walker6.find_all("img"):
                    image_links.append(item5.get("src"))

        # This creates an art object for each of the Walker pieces found in the search.
        counter = 0
        while counter < len(titles):
            w = Art(titles[counter], artists[counter], years[counter], image_links[counter], "Walker Art Center")
            list_of_walker_art.append(w)
            counter += 1

        return list_of_walker_art
