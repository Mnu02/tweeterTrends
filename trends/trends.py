"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments, load_tweets
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait
from string import ascii_letters
from ucb import main, trace, interact, log_current_line
from math import sqrt


###################################
# Phase 1: The Feelings in Tweets #
###################################

# The tweet abstract data type, implemented as a dictionary.

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    >>> tweet_string(t)
    '"just ate lunch" @ (38, 74)'
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    return tweet["text"]

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    return tweet["time"]

def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    result = make_position(tweet["latitude"], tweet["longitude"])
    return result

# The tweet abstract data type, implemented as a function.

def make_tweet_fn(text, time, lat, lon):
    """An alternate implementation of make_tweet: a tweet is a function.

    >>> t = make_tweet_fn("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text_fn(t)
    'just ate lunch'
    >>> tweet_time_fn(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> latitude(tweet_location_fn(t))
    38
    """
    def makeTweetFnHelper(stringKey):
        if stringKey == "text":
            return text
        elif stringKey == "time":
            return time
        elif stringKey == "lat":
            return lat
        elif stringKey == "lon":
            return lon
    return makeTweetFnHelper

def tweet_text_fn(tweet):
    """Return a string, the words in the text of a functional tweet."""
    return tweet('text')

def tweet_time_fn(tweet):
    """Return the datetime representing when a functional tweet was posted."""
    return tweet('time')

def tweet_location_fn(tweet):
    """Return a position representing a functional tweet's location."""
    return make_position(tweet('lat'), tweet('lon'))

### === +++ ABSTRACTION BARRIER +++ === ###

def tweet_words(tweet):
    """Return the words in a tweet."""
    return extract_words(tweet_text(tweet))

def tweet_string(tweet):
    """Return a string representing a functional tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    builder = ''
    for character in text:
        if character in ascii_letters:
            builder += character                # build a long string with ascii letters and spaces
        else:
            builder += ' '
    return builder.split()

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'
    return [value]

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    return s[0] != None

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    return s[0]

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))

def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("berkeley golden bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    # get a list of all the extracted words from a tweet
    # iterate over the list and if the word has a sentiment ie val is a number add it to the growing sum
    # if it has no sentiment, increase the none count
    # end iteration
    # if none count == length of tweet words list, then your list has all nones ie make a sentiment with None
    # else, divide the growing sum with the length of the list minus the none count

    sentimentSum = 0
    noneCount = 0
    tweetWordList = tweet_words(tweet)
    for word in tweetWordList:
        wordSentiment = get_word_sentiment(word)
        if has_sentiment(wordSentiment):
            sentimentSum += sentiment_value(wordSentiment)
        else:
            noneCount += 1

    if noneCount == len(tweetWordList):
        return make_sentiment(None)
    else:
        average = sentimentSum / (len(tweetWordList) - noneCount)
        return make_sentiment(average)
    

#################################
# Phase 2: The Geometry of Maps #
#################################

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, use the latitude and longitude of its first
    position as its centroid.

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> round5 = lambda x: round(x, 5) # Rounds floats to 5 digits
    >>> tuple(map(round5, find_centroid(triangle)))
    (3.0, 2.0, 6.0)
    >>> tuple(map(round5, find_centroid([p1, p3, p2, p1])))
    (3.0, 2.0, 6.0)
    >>> tuple(map(float, find_centroid([p1, p2, p1])))  # A zero-area polygon
    (1.0, 2.0, 0.0)
    """
    areaSum = 0
    centroidX = 0
    centroidY = 0
    for i in range(len(polygon)-1):
        areaSum += latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i])
        centroidX += (latitude(polygon[i]) + latitude(polygon[i+1])) * ((latitude(polygon[i])*longitude(polygon[i+1])) - (latitude(polygon[i+1])*longitude(polygon[i])))
        centroidY += (longitude(polygon[i])+longitude(polygon[i+1]))* (latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i]))

    area = 0.5 * areaSum
    if area != 0:
        x = (1/(6 * area)) * centroidX
        y = (1/(6 * area)) * centroidY
        return (x, y, abs(area))

    return (latitude(polygon[0]), longitude(polygon[0]), 0.0)

def find_state_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_state_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_state_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    xNumerator = 0
    yNumerator = 0
    area = 0
    for polygon in polygons:
        temp = find_centroid(polygon)
        xNumerator += temp[0] * temp[2]
        yNumerator += temp[1] * temp[2]
        area += temp[2]

    x = xNumerator / area
    y = yNumerator / area
    return make_position(x, y) 



###################################
# Phase 3: The Mood of the Nation #
###################################

def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> two_tweets_by_state = group_tweets_by_state([sf, ny])
    >>> len(two_tweets_by_state)
    2
    >>> california_tweets = two_tweets_by_state['CA']
    >>> len(california_tweets)
    1
    >>> tweet_string(california_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    
    tweets_by_state = {}
    # for each tweet, look at every state ie have two for loops, 1 for tweets & 1 for states (sounds inefficient but meh)
    for tweet in tweets:
        tempList = []                           # always gonna have one element inside
        for state in us_states:
            stateCenter = find_state_center(us_states[state])               # find the center of current state
            tweetPositionObject = tweet_location(tweet)
            distance = geo_distance(tweetPositionObject, stateCenter)            # implement a method to calc the dist between a tweet's location n that of the state's center
            if len(tempList) == 0:                          # only for the 1st state we're looking at
                tempList.append(distance)                   # put tweet to state dist in list
                rememberedState = state                     # remember the state who dist data you have
            else:                                           # for the rest of the states
                if distance < tempList[0]:                  # compare the distances. You want the least and then remember the state
                    rememberedState = state
                    tempList[0] = distance
                                                            # for the i-th tweet, you are done referencing it with all states
        if rememberedState in tweets_by_state:              # if state already has some tweets linked to it
            tweets_by_state[rememberedState].append(tweet)
        else:                                               # if this state is new to the dictionary and is getting its first tweet
            tweets_by_state[rememberedState] = [tweet]
            
    return tweets_by_state


def calcSentiment(tweetList):
    """
    Returns the average sentiment of the tweets in the list
    Requires `tweetList` is a list of tweet abstract data types
    """
    total = 0
    nonCount = 0
    for tweet in tweetList:
        sentiment = analyze_tweet_sentiment(tweet)
        if not has_sentiment(sentiment):
            nonCount += 1
        elif has_sentiment(sentiment):
            total += sentiment_value(analyze_tweet_sentiment(tweet))

    divisor = (len(tweetList) - nonCount)
    if divisor == 0:
        return "None"
    else:
        return total/(len(tweetList) - nonCount)


def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    averaged_state_sentiments = {}
    for state in tweets_by_state: 
      avgSentiment = calcSentiment(tweets_by_state[state])
      if type(avgSentiment) != str:
            averaged_state_sentiments[state] = avgSentiment
    return averaged_state_sentiments


##########################
# Command Line Interface #
##########################

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_state_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_state_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_query(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def swap_tweet_representation(other=[make_tweet_fn, tweet_text_fn,
                                     tweet_time_fn, tweet_location_fn]):
    """Swap to another representation of tweets. Call again to swap back."""
    global make_tweet, tweet_text, tweet_time, tweet_location
    swap_to = tuple(other)
    other[:] = [make_tweet, tweet_text, tweet_time, tweet_location]
    make_tweet, tweet_text, tweet_time, tweet_location = swap_to


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_query', '-m', action='store_true')
    parser.add_argument('--use_functional_tweets', '-f', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    if args.use_functional_tweets:
        swap_tweet_representation()
        print("Now using a functional representation of tweets!")
        args.use_functional_tweets = False
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))


# class Solution(object):
#     def lengthOfLongestSubstring(self, s):
#         """
#         :type s: str
#         :rtype: int
#         """
#         strBuilder = '' 
#         count = 0 
#         maxLen = 0
#         i = 0                              # use this to index the string
#         processed = 0                      # keeps track of whether we're done counting from every xr
#         while (i < len(s)):
#             if (not s[i] in strBuilder):
#                 strBuilder += s[i]         # string not in builder so add it
#                 count += 1                 # increase the count by one
#                 i += 1                     # advance i pointer by one too to point at the next element
#                 if (count > maxLen):       # maxLen must record the highest value of count
#                     maxLen = count
#             else:                          # we encountered an element already in the builder
#                 strBuilder = ''            # strB becomes empty too to start work for the next elem
#                 count = 0                  # start counting unique elements ie zero
#                 processed += 1             # you're done with the letter you were on so shift to the next
#                 i = processed              # i will start from processed
#         return maxLen
        
        
        
#    			#create set to hold unique values
#         my_set= set()
#         #maximum, left and right pointers
#         maximum, left, right = 0, 0, 0
#         while right < len(s):
#             #if there is now repeatition, removing all letters from set
#             # before repition occurance using left pointer
#             while s[right] in my_set:
#                 my_set.remove(s[left])
#                 left += 1
#             #appending elements to set
#             my_set.add(s[right])
#             #updating longest
#             maximum = max(maximum, right - left + 1)
#             right += 1
        
#         return maximum
