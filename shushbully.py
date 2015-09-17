import json
import requests
from requests_oauthlib import OAuth1
import sys
from time import sleep

# credentials from ghost account
GHOST_CONSUMER_KEY = ''
GHOST_CONSUMER_SECRET = ''
GHOST_ACCESS_TOKEN_KEY = ''
GHOST_ACCESS_TOKEN_SECRET = ''

# credentials from actual account
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

WHITELIST = [
    'orvtech',
]

SHITLIST = [
    'amaia_roja',
    'anat5',
    'carollafra',
    'contraofensiva',
    'correoorinoco',
    'forocandanga',
    'guerrillaragua',
    'hectorodriguez',
    'izarradeverdad',
    'jorgerpsuv',
    'jrodriguezpsuv',
    'lahojillaentv',
    'laradiodelsur',
    'maperezpirela',
    'nicolasmaduro',
    'prisciliano_alf',
    'thaivama',
    'yndiratorregros',
    'PatriciaDorta40',
]

BLOCK_URL = 'https://api.twitter.com/1.1/blocks/create.json'
MUTE_URL = 'https://api.twitter.com/1.1/mutes/users/create.json'


def retweeters(tweet_id):
    api_url = ("https://api.twitter.com/1.1/statuses/retweets/"
               "{tweet_id}.json").format(tweet_id=tweet_id)
    payload = {'count': '100'}
    auth = OAuth1(GHOST_CONSUMER_KEY, GHOST_CONSUMER_SECRET,
                  GHOST_ACCESS_TOKEN_KEY, GHOST_ACCESS_TOKEN_SECRET)
    r = requests.get(api_url, stream=False, auth=auth, params=payload)
    try:
        if (r.headers['x-rate-limit-remaining'] and
                r.headers['x-rate-limit-remaining'] == "0"):
            print("We reached rate limit for ", api_url)
            print("Try again at", r.headers["x-rate-limit-reset"])
            quit()
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("OK")
    retweetsObj = json.loads(r.content)
    return (elem['user']['screen_name'] for elem in retweetsObj)


def last_tweet_id(user):
    api_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    payload = {'screen_name': user, 'count': '1', 'trim_user': 't',
               'include_rts': 'false'}
    auth = OAuth1(GHOST_CONSUMER_KEY, GHOST_CONSUMER_SECRET,
                  GHOST_ACCESS_TOKEN_KEY, GHOST_ACCESS_TOKEN_SECRET)
    r = requests.get(api_url, stream=False, auth=auth, params=payload)
    statusObj = json.loads(r.content)
    return statusObj[0]['id']


def act_on_handle(api_url, auth, payload):
    try:
        r = requests.post(api_url, stream=False, auth=auth, params=payload)
        print(r.headers['status'], payload)
        if (r.headers['x-rate-limit-remaining'] and
                r.headers['x-rate-limit-remaining'] == "0"):
            print('We reached rate limit for {url}'.format(url=api_url))
            print('Try again at {reset}'.format(
                reset=r.headers["x-rate-limit-reset"]))
            sys.exit()
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass


def main():
    for shit_user in SHITLIST:
        try:
            tweet_id = str(last_tweet_id(shit_user))
            print("")
            print("Analizing retweeters of {user} TweetID: {tweet_id}".format(
                  user=shit_user, tweet_id=tweet_id))
            print("https://twitter.com/{user}/status/{tweet_id}".format(
                  user=shit_user, tweet_id=tweet_id))
            for user in retweeters(tweet_id):
                if user not in WHITELIST:
                    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET,
                                  ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
                    payload = "screen_name={user}".format(user=user)
                    # act_on_handle(BLOCK_URL, auth, payload)
                    act_on_handle(MUTE_URL, auth, payload)
                    sleep(1)
                else:
                    print("YOU FOLLOW {user} WHO RETWEETED {shit_user}".format(
                          user=user, shit_user=shit_user))
                    sleep(40)
            sleep(60)
        except KeyboardInterrupt:
            sys.exit()
        except:
            pass

if __name__ == '__main__':
    main()
