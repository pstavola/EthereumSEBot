class Feed:
    def __init__(self, name, url, hashtag):
        self.name = name
        self.url = url
        self.hashtag = hashtag

    def display_feed(self):
        print " Name    : ", self.name, "\n URL     : ", self.url, "\n Hashtag : ", self.hashtag, "\n"

    def get_name(self):
    	return self.name
        
    def get_url(self):
        return self.url

    def get_hashtag(self):
        return self.hashtag
