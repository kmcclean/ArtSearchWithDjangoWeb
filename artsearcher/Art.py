class Art:

    #This defines the traits of particular pieces of art.
    def __init__(self, name, artist, year, image_link, museum):

        self.art = name
        self.artist = artist
        self.year = year
        self.image = image_link
        self.museum = museum

    def print_art_item(self):
        print("Title: " + self.art)
        print("Artist: " + self.artist)
        print("Year: " + self.year)
        print("Link: " + self.image)
        print("Museum: " + self.museum)