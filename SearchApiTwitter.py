import tweepy
from accessKeys import consumer_key, consumer_secret, access_key, access_secret



# postSoviets=['084d0d0155787e9d']     # Ukraine
#              # '333a5811d6b0c1cb',     # Belarus
#              # '5714382051c06d1e',     # Russia
#              # '56ac89b367a68a34',     # Kyrgyzstan
#              # '6d73a696edc5306f',     # Kazakhstan
#              # '8f3fa3e2dedc1db5',     # Uzbekistan
#              # '66fd08f1746d8702',     # Tajikistan
#              # '3d77e0dd1c4ed51c',     # Turkmenistan
#              # 'd0e642e8a900f679',     # Latvia
#              # 'd5cde4dddd7e6f94',     # Lithuania
#              # 'e222580e9a58b499',     # Estonia
#              # '1315b8e69a2d1511',     # Armenia
#              # 'efc23cd34689b068',     # Azerbaijan
#              # '60fcb78e1f3a23dd',     # Georgia
#              # 'a89b926651acf416']     # Moldova


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

places = api.geo_search(query="ukraine", granularity="country")
place_id = places[0].id

print places[0].bounding_box


# i=0
# for place_id in postSoviets:
#     print '''+++++++++++++++++++++++++++++++++++++'''
#     tweets = api.search(q = "place:" + place_id)
#     for tweet in tweets:
#         print "========="
#         # print tweet
#         print tweet.place.name
#         print tweet.coordinates
#         print tweet.text
#         print tweet.created_at
#         i+=1
# print i



















# postSoviets=['1315b8e69a2d1511',     # Armenia
#              'efc23cd34689b068',     # Azerbaijan
#              '60fcb78e1f3a23dd',     # Georgia
#              'a89b926651acf416',     # Moldova
#              '084d0d0155787e9d',     # Ukraine
#              '333a5811d6b0c1cb',     # Belarus
#              '5714382051c06d1e',     # Russia
#              '56ac89b367a68a34',     # Kyrgyzstan
#              '6d73a696edc5306f',     # Kazakhstan
#              '8f3fa3e2dedc1db5',     # Uzbekistan
#              '66fd08f1746d8702',     # Tajikistan
#              '3d77e0dd1c4ed51c',     # Turkmenistan
#              'd0e642e8a900f679',     # Latvia
#              'd5cde4dddd7e6f94',     # Lithuania
#              "e222580e9a58b499"]    # Estonia


# ARMENIA 1315b8e69a2d1511
# =============
# AZERBAIJAN efc23cd34689b068
# =============
# GEORGIA 60fcb78e1f3a23dd
# =============
# MOLDOVA a89b926651acf416
# =============
# UKRAINE 084d0d0155787e9d
# =============
# BELARUS 333a5811d6b0c1cb
# =============
# RUSSIA 5714382051c06d1e
# =============
# KYRGYZSTAN 56ac89b367a68a34
# =============
# KAZAKHSTAN 6d73a696edc5306f
# =============
# UZBEKISTAN 8f3fa3e2dedc1db5
# =============
# TAJIKISTAN 66fd08f1746d8702
# =============
# TURKMENISTAN 3d77e0dd1c4ed51c
# =============
# LATVIA d0e642e8a900f679
# =============
# LITHUANIA d5cde4dddd7e6f94
# =============
# ESTONIA e222580e9a58b499
