# -*- coding: utf-8 -*-
 
import csv
import json
import os.path
from pprint import pprint
import urllib
import urllib2

web = "https://play.spotify.com/trackset/"
app = "http://open.spotify.com/trackset/Playlist/"
embed = "https://embed.spotify.com/?uri=spotify:trackset:"

 
lineup = [
    "Outkast", 
    "the Knife", 
    "the Replacements", 
    "Broken Bells", 
    "Zedd", 
    "Girl Talk", 
    "Ellie Goulding", 
    "Chromeo", 
    "Haim", 
    "Neko Case", 
    "AFI", 
    "Martin Garrix", 
    "Bonobo", 
    "Bryan Ferry", 
    "the Glitch Mob", 
    "the Afghan Whigs", 
    "the Cult", 
    "Bastille", 
    "Flume", 
    "Aloe Blacc", 
    "Jagwar Ma", 
    "A$AP Ferg", 
    "Grouplove", 
    "Woodkid", 
    "Carnage", 
    "Shlohmo", 
    "Gareth Emery", 
    "Michael Brun", 
    "MS MR", 
    "Kate Nash", 
    "Hot Since 82", 
    "Damian Lazarus", 
    "GOAT", 
    "Nina Kraviz", 
    "Anthony Green", 
    "Duke Dumont", 
    "the Jon Spencer Blues Explosion", 
    "Solomun", 
    "ZZ Ward", 
    "Anti-Flag", 
    "Caravan Palace", 
    "Flatbush Zombies", 
    "Deorro", 
    "Waxahatchee", 
    "Title Fight", 
    "Davide Squillace", 
    "DJ Falcon", 
    "Dum Dum Girls", 
    "Austra", 
    "Tom Odell", 
    "Dixon", 
    "Wye Oak", 
    "Crosses", 
    "Mako", 
    "the Preatures", 
    "the Bots", 
    "Gabba Gabba Heys", 
    "Muse", 
    "Queens of the Stone Age", 
    "Skrillex", 
    "Pharrell Williams", 
    "Lorde", 
    "Foster the People", 
    "Pet Shop Boys", 
    "MGMT", 
    "Empire of the Sun", 
    "Fatboy Slim", 
    "Nas", 
    "Kid Cudi", 
    "the Head and the Heart", 
    "Sleigh Bells", 
    "Cage the Elephant", 
    "City and Colour", 
    "Chvrches", 
    "Dillon Francis", 
    "Capital Cities", 
    "the Naked and Famous", 
    "Temples", 
    "Mogwai", 
    "Warpaint", 
    "Solange", 
    "Washed Out", 
    "Future Islands", 
    "Ty Segall", 
    "DARKSIDE", 
    "Banks", 
    "Tiga", 
    "Bombay Bicycle Club", 
    "Holy Ghost!", 
    "Netsky", 
    "RL Grime", 
    "Galantis", 
    "Foxygen", 
    "White Lies", 
    "Graveyard", 
    "the Internet", 
    "Laura Mvula", 
    "Dismemberment Plan", 
    "Headhunterz", 
    "Blood Orange", 
    "GTA", 
    "TJR", 
    "Cajmere", 
    "Guy Gerber", 
    "Nicole Moudaber", 
    "MAKJ", 
    "Bear Hands", 
    "the Magician", 
    "Young & Sick", 
    "Unlocking the Truth", 
    "Saints of Valory", 
    "Carbon Airways", 
    "UZ", 
    "Syd Arthur", 
    "Bicep", 
    "Drowners", 
    "Arcade Fire", 
    "Beck", 
    "Calvin Harris", 
    "Neutral Milk Hotel", 
    "Disclosure", 
    "Lana Del Rey", 
    "Motörhead", 
    "Alesso", 
    "Duck Sauce", 
    "Little Dragon", 
    "Beady Eye", 
    "Flosstradamus", 
    "the Toy Dolls", 
    "the 1975", 
    "Adventure Club", 
    "Big Gigantic", 
    "Chance the Rapper", 
    "Laurent Garnier", 
    "Krewella", 
    "Rudimental", 
    "STRFKR", 
    "Fishbone", 
    "Trombone Shorty", 
    "AlunaGeorge", 
    "Art Department", 
    "Flight Facilities", 
    "Frank Turner", 
    "John Newman", 
    "Maceo Plex", 
    "Superchunk", 
    "Bombino", 
    "Daughter", 
    "Bad Manners", 
    "Surfer Blood", 
    "Lee Burridge", 
    "Poolside", 
    "Classixx", 
    "Showtek", 
    "James Vincent McMorrow", 
    "Bo Ningen", 
    "Aeroplane", 
    "Ratking", 
    "Jhené Aiko", 
    "J. Roddy Walston and the Business", 
    "Factory Floor", 
    "Preservation Hall Jazz Band", 
    "Anna Lunoe", 
    "the Martinez Brothers", 
    "Scuba", 
    "John Beaver"
]
 
STOP_WORDS = ["the", "a", "an"]
 
 
class Search:
 
    def __init__(self, query_type, query):
        self.query_type = query_type.lower()
        self.query = query.lower()
        self.result_key = "{}s".format(self.query_type)
        self.query_spotify()
 
    def query_spotify(self, retry=False):
        BASE = "http://ws.spotify.com/search/1/{}.json?".format(self.query_type)
        params = dict(q=self.query)
        params = urllib.urlencode(params)  
        url = BASE + params
        resp = urllib2.urlopen(url)
        self.data = json.load(resp)
        try:
            self.hits = self.data[self.result_key]
            self.top_hit = self.hits[0]
        except IndexError:
            if not retry:
                w = filter(lambda x: x not in STOP_WORDS, self.query.split(" "))
                self.query = " ".join(w)
                self.query_spotify(retry=True)
            else:
                self.hits = self.top_hit = None
 
class Lookup:
 
    def __init__(self, uri):
        self.EXTRAS = {
            'artist': 'album',
            'album': 'track'}
 
        
        self.uri = uri
        _, self.type, _ = self.uri.split(":")
        self.lookup()
 
    def lookup(self):
        BASE = "http://ws.spotify.com/lookup/1/.json?"
        self.extra = self.EXTRAS[self.type]
        params = dict(
            uri=self.uri,
            extras="{}detail".format(self.extra)
        )
        params = urllib.urlencode(params)  
        url = BASE + params
        resp = urllib2.urlopen(url)
        self.data = json.load(resp)
        self.name = self.data[self.type]['name']
        results = self.data[self.type]["{}s".format(self.extra)]
        if self.type == 'artist':
            results = map(lambda x: x[self.extra], results)
        self.results = results
 
 
def lineup_by_pop():
    bands = []
    not_found = []
    for band in lineup:
        result = Search('artist', band)
        top = result.top_hit
        if top:
            pop = float(top['popularity'])
            name = top['name'].encode('utf-8')
            bands.append((pop, name))
        else:
            not_found.append(band)
 
    bands = sorted(bands, reverse=True)
    
    for band in bands:
        print("{:.2f} {}".format(*band))
 
    for band in not_found:
        print("Not found: {}".format(band.encode('utf-8')))
 
 
def albums_by_artist(artist, uri=None):
        
    if not uri:
        result = Search('artist', artist)
        top = result.top_hit
        if not top:
            return None
        uri = top['href']
    result = Lookup(uri)
    name = result.name.encode('utf8')
    album_map = lambda x: (
        (x['artist'], x['name']),
        x['href'])
    albums = map(album_map, result.results)

    mask = list(set([el[0] for el in albums if el[0][0].encode('utf8')]) == name)
    unique_albums = []
    for image in mask:
        album = filter(lambda x: x[0] == image, albums)[0]
        unique_albums.append(album[0] + (album[1],))
    
    return unique_albums
 
def clean_track(track, album_info):
    """Removes unneeded info from track and adds album_info"""
 
    excluded = ['artists', 'disc-number', 'external-ids', 'explicit']
    items = track.items()
    mask = lambda x: x[0] not in excluded
    track = dict(filter(mask, items))
    track[u'artist'], track[u'album'], track[u'album_href'] = album_info
 
    return track
 
def tracks_by_artist(artist, uri=None):
    """Returns list of json tracks for artist query"""
 
    albums = albums_by_artist(artist, uri)
    if not albums:
        return None
    tracks = []
    for album in albums:
        cleaner = lambda x: clean_track(x, album)
        uri = album[-1]
        result = Lookup(uri)
        cleaned = map(cleaner, result.results)
        tracks += cleaned
    
    return tracks
 
def csvify(x):
    if isinstance(x, unicode):
        output = x.encode('utf8')
        if x.find(',') <> -1:
            output = u'"{}"'.format(x).encode('utf8')
    else:
        output = str(x)
    
    return output
 
def write_tracks_to_csv():
 
    fields = [u'available', u'album', u'track-number', u'artist',
        u'popularity', u'album_href', u'length', u'href', u'name']
    with open('tracks.csv', 'w') as f:
        f.write(','.join(fields))
    for artist in lineup[:10]:
        tracks = tracks_by_artist(artist)
        if not tracks:
            continue
        for track in tracks:
            with open('tracks.csv', 'a') as f:
 
                f.write('\n')
                f.write(','.join(map(csvify, track.values())))

def load_tracks(filename):
 
    with open("{}".format(filename), 'r') as f:
        reader = csv.DictReader(f)
        tracks = [row for row in reader]
 
    return tracks
 
def load_tracks_http(url):
    f = urllib2.urlopen(url)
    reader = csv.DictReader(f)
    data = [row for row in reader]
    
    return data
 
def pop_list(tracks, size):
    """Returns playlist URL of 'size' most popular tracks out of tracks"""
 
    pops = map(lambda x: (float(x['popularity']), x), tracks)
    pops = sorted(pops, reverse=True)
    pops = pops[:size]
 
    pops = map(lambda x: x[1], pops)
    return pops
 
def build_pl_url(playlist):
    """Takes list of spotify URIs and returns playlist"""
 
    #Native player base URL: http://open.spotify.com/trackset/Playlist/
    #Web player base URL: https://play.spotify.com/trackset/Playlist/
    BASE = "https://play.spotify.com/trackset/Playlist/"
    params = ','.join(playlist)
    url = BASE + params
 
    return url



def write_artists_with_meta_to_json():
    artists = []
    for name in lineup:
        result = Search('artist', name)
        if result.top_hit:
            artists.append(result.top_hit)

    with open("data/lineup_json.txt", "w") as f:
        f.write(json.dumps(artists))

def strip_name(name):

    name = name.split('(')[0].split('-')[0].split('[')[0].strip()
    return name

def filter_tracks(tracks):
    unique = []
    dupes = 0
    for track in tracks:
        filtered = unique
        filtered = filter(lambda x: x['artist'] == track['artist'], filtered)
        filtered = filter(lambda x: strip_name(x['name']) == strip_name(track['name']), filtered)
        filtered = filter(lambda x: abs(float(x['length']) - float(track['length'])) < 3.0, filtered)
        if len(filtered) == 0:
            unique.append(track)
        else:
            dupes += 1

    return unique, dupes


def write_top_tracks_by_artist(size):

    with open('data/lineup_json.txt', 'r') as f:
        artists = json.load(f)

    for num in ["7lIBLhQHKay3r1xtO3VtWT",  "1dqGS5sT6PE2wEvP1gROZC", "4jYpX9diAOBUU0iictJYiF"]:
    #for artist in artists[51:]:
        uri = "spotify:artist:{}".format(num)
        #uri = artist['href']
        tracks = tracks_by_artist(None, uri=uri)
        if tracks:
            unique, dupes = filter_tracks(tracks)
            print "{}; removed: {}".format(artist['name'].encode('utf8'), dupes)
            tracks = pop_list(unique, size)

        try:
            with open("data/tracklist.txt", "r") as f:
                trackset = json.load(f)
        except ValueError:
            trackset = {}
        
        trackset[uri.split(":")[-1]] = tracks

        with open("data/tracklist.txt", "w") as f:
            f.write(json.dumps(trackset))

#write_top_tracks_by_artist(25)

with open("data/tracklist.txt", "r") as f:
    data = json.load(f)
print(len(data.keys()))
print(data.values()[-1])
for item in data.items():
    if not item[1]:
        print item[0]


"""
tracks = load_tracks('tracks1.csv')
tracks = load_tracks_http("https://dl.dropboxusercontent.com/u/29149143/coachella.csv")
 
top_tracks = []
artists = map(lambda x:x['artist'],tracks)
artists = list(set(artists))
 
for artist in artists:
    filt = lambda x:x['artist']==artist
    filtered = filter(filt, tracks)
    top = pop_list(filtered, 2)
    top_tracks += top
 
# Get just a subset of the most popular

top_tracks = pop_list(top_tracks, 200)

tot_length = 0
uris = []
for track in top_tracks:
    length = float(track['length'])
    uri = track['href'].split(':')[-1]
    uris.append(uri)
    tot_length += length

print("Total length: {} mins".format(
        tot_length / 60))


playlist = ",".join(uris)
print(playlist)
print(len(playlist))

"""
