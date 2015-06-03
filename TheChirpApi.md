# Introduction #

CHIRP Radio provides access to its data through a [RESTful](http://en.wikipedia.org/wiki/Representational_State_Transfer) API.  If you are using the API for something interesting, please let us know.  You can email kumar.mcmillan@gmail.com

# Making Requests #

All requests to the API should include a name that identifies the source.  For example, the Android application adds ?src=chirpradio-android to all requests:

```
https://chirpradio.appspot.com/api/current_playlist?src=chirpradio-android
```

Please be cool (like Fonzi) when using the API.

## GZipped Responses ##

To reduce data transfer for mobile devices and whatnot, you can send this header to receive a gzipped response:

```
Accept-Encoding: gzip
```

In the example of the Current Playlist service, this reduces the payload to ~700b from ~2kb.  If you don't get a gzipped response after sending this header, you might have to adjust your user agent to include `gzip` in its name.  For example:

```
Accept-Encoding: gzip
User-Agent: curl/gzip
```

This feature is [built into Google App Engine](http://code.google.com/appengine/docs/python/runtime.html#Responses).

## JSONP Responses ##

For easier cross-domain support you can use [JSONP](http://en.wikipedia.org/wiki/JSONP) (JSON-with-padding).  Just add a jsonp URL parameter with the name of the function callback:

```
http://chirpradio.appspot.com/api/current_playlist?src=your-source&jsonp=processResponse
```

This will return JavaScript code that you can execute in a script tag to process the data:

```
processResponse({"foo":"bar"});
```

# Services #

All HTTP responses are [JSON](http://www.json.org/) or [JSONP](http://en.wikipedia.org/wiki/JSONP) formatted documents and all text is encoded as UTF-8.

# Current Playlist #

| Endpoint |  https://chirpradio.appspot.com/api/current_playlist |
|:---------|:-----------------------------------------------------|
| Methods supported | **GET**                                              |

Overview of JSON response:

```
{
    'now_playing': {
        // Track object playing on CHIRP right now.
    },
    'recently_played': [
        // list of five Track objects previously played on CHIRP.
    ]
}
```

Each **Track object** has the following fields.

| **Field** | **Can be NULL?** | **Description** |
|:----------|:-----------------|:----------------|
| **id**    | Not NULL         | Unique identifier for the track. This is a URL-safe ascii string. |
| **dj**    | Not NULL         | Name of the CHIRP DJ who played the track. |
| **artist** | Not NULL         | Artist of the track played. |
| **artist\_is\_local** | Not NULL         | Boolean. This is true if the artist is local to Chicago, otherwise false. |
| **track** | Not NULL         | Title of the track. |
| **release** | Not NULL         | Title of the release. Could be an album name or the name of the track if it's a single. |
| **label** | Not NULL         | Name of the label the release appears on. |
| **notes** | Not NULL         | Any notes that the DJ made on the track. Example: "Cold, Bold, and Together was a decent funk band including Kenny G as a member!" When there are no notes you get an empty string. |
| **played\_at\_gmt** | Not NULL         | ISO formatted timestamp of when the track was played, as GMT |
| **played\_at\_gmt\_ts** | Not NULL         | Unix timestamp (seconds since Unix epoch) in universal time (GMT) of when the track was played |
| **played\_at\_local** | Not NULL         | ISO formatted timestamp of when the track was played, in local Chicago time |
| **played\_at\_local\_expire** | Not NULL         | **DEPRECATED**. This is no longer supported. ISO formatted timestamp in local Chicago time of when a track may be considered expired. Currently set to 6 months in the future. |
| **played\_at\_local\_ts** | Not NULL         | Unix timestamp (seconds since Unix epoch) in local Chicago time of when the track was played |
| **lastfm\_urls** | Not NULL         | A dictionary of LastFM URLs to various sizes of album artwork for this track.  **NOTE** If you display LastFM URLs then you need to link to LastFM as a source and also follow their [Terms of Service](http://www.last.fm/api/tos) |
| **lastfm\_urls[`sm_image`]** | **NULL**         | URL to small album image.  There doesn't seem to be a standard size, one example is 34x34. This might be NULL temporarily while it's fetched. |
| **lastfm\_urls[`med_image`]** | **NULL**         | URL to medium album image.  There doesn't seem to be a standard size, one example is 64x64. This might be NULL temporarily while it's fetched. |
| **lastfm\_urls[`large_image`]** | **NULL**         | URL to large album image.  There doesn't seem to be a standard size, one example is 174x174. This might be NULL temporarily while it's fetched. |

Example:

```
{
    "now_playing": {
        "artist_is_local": false,
        "dj": "Cher Vincent",
        "artist": "Don Hinson and the The Rigamorticians",
        "track": "Monster Mash",
        "notes": "",
        "played_at_local_ts": 1350862475.0,
        "label": "Capitol",
        "played_at_gmt_ts": 1350880475,
        "played_at_gmt": "2012-10-22T04:34:35.609576",
        "release": "Monster Dance Party",
        "played_at_local_expire": "2013-04-25T23:34:35.609576-05:00",
        "played_at_local": "2012-10-21T23:34:35.609576-05:00",
        "id": "ahBzfmNoaXJwcmFkaW8taHJkchYLEg1QbGF5bGlzdEV2ZW50GMWXrQUM",
        "lastfm_urls": {
            "med_image": null,
            "sm_image": null,
            "_processed": true,
            "large_image": null
        }
    },
    "recently_played": [{
        "artist_is_local": false,
        "dj": "Cher Vincent",
        "artist": "Django Django",
        "track": "Storm",
        "notes": "",
        "played_at_local_ts": 1350862217.0,
        "label": "Ribbon",
        "played_at_gmt_ts": 1350880217,
        "played_at_gmt": "2012-10-22T04:30:17.209755",
        "release": "Django Django",
        "played_at_local_expire": "2013-04-25T23:30:17.209755-05:00",
        "played_at_local": "2012-10-21T23:30:17.209755-05:00",
        "id": "ahBzfmNoaXJwcmFkaW8taHJkchYLEg1QbGF5bGlzdEV2ZW50GOHdrQUM",
        "lastfm_urls": {
            "med_image": "http://userserve-ak.last.fm/serve/64s/73874416.png",
            "sm_image": "http://userserve-ak.last.fm/serve/34s/73874416.png",
            "_processed": true,
            "large_image": "http://userserve-ak.last.fm/serve/174s/73874416.png"
        }
    }, {
        "artist_is_local": false,
        "dj": "Cher Vincent",
        "artist": "Broken Bells",
        "track": "The Ghost Inside",
        "notes": "",
        "played_at_local_ts": 1350862024.0,
        "label": "Columbia",
        "played_at_gmt_ts": 1350880024,
        "played_at_gmt": "2012-10-22T04:27:04.358217",
        "release": "Broken Bells",
        "played_at_local_expire": "2013-04-25T23:27:04.358217-05:00",
        "played_at_local": "2012-10-21T23:27:04.358217-05:00",
        "id": "ahBzfmNoaXJwcmFkaW8taHJkchYLEg1QbGF5bGlzdEV2ZW50GJXRrAUM",
        "lastfm_urls": {
            "med_image": "http://userserve-ak.last.fm/serve/64s/62207221.png",
            "sm_image": "http://userserve-ak.last.fm/serve/34s/62207221.png",
            "_processed": true,
            "large_image": "http://userserve-ak.last.fm/serve/174s/62207221.png"
        }
    }, {
        "artist_is_local": false,
        "dj": "Cher Vincent",
        "artist": "Ty Segall",
        "track": "The Hill",
        "notes": "",
        "played_at_local_ts": 1350861891.0,
        "label": "Drag City",
        "played_at_gmt_ts": 1350879891,
        "played_at_gmt": "2012-10-22T04:24:51.258562",
        "release": "Twins",
        "played_at_local_expire": "2013-04-25T23:24:51.258562-05:00",
        "played_at_local": "2012-10-21T23:24:51.258562-05:00",
        "id": "ahBzfmNoaXJwcmFkaW8taHJkchYLEg1QbGF5bGlzdEV2ZW50GJ2rqQUM",
        "lastfm_urls": {
            "med_image": "http://userserve-ak.last.fm/serve/64s/82864247.png",
            "sm_image": "http://userserve-ak.last.fm/serve/34s/82864247.png",
            "_processed": true,
            "large_image": "http://userserve-ak.last.fm/serve/174s/82864247.png"
        }
    }, {
        "artist_is_local": false,
        "dj": "Cher Vincent",
        "artist": "Echo Lake",
        "track": "In Dreams",
        "notes": "",
        "played_at_local_ts": 1350861595.0,
        "label": "Slumberland",
        "played_at_gmt_ts": 1350879595,
        "played_at_gmt": "2012-10-22T04:19:55.131654",
        "release": "Wild Peace",
        "played_at_local_expire": "2013-04-25T23:19:55.131654-05:00",
        "played_at_local": "2012-10-21T23:19:55.131654-05:00",
        "id": "ahBzfmNoaXJwcmFkaW8taHJkchYLEg1QbGF5bGlzdEV2ZW50GN-5rAUM",
        "lastfm_urls": {
            "med_image": "http://userserve-ak.last.fm/serve/64s/80265629.png",
            "sm_image": "http://userserve-ak.last.fm/serve/34s/80265629.png",
            "_processed": true,
            "large_image": "http://userserve-ak.last.fm/serve/174s/80265629.png"
        }
    }, {
        "artist_is_local": false,
        "dj": "Cher Vincent",
        "artist": "The Misfits",
        "track": "Dig Up Her Bones",
        "notes": "",
        "played_at_local_ts": 1350861424.0,
        "label": "Geffen",
        "played_at_gmt_ts": 1350879424,
        "played_at_gmt": "2012-10-22T04:17:04.521602",
        "release": "American Psycho",
        "played_at_local_expire": "2013-04-25T23:17:04.521602-05:00",
        "played_at_local": "2012-10-21T23:17:04.521602-05:00",
        "id": "ahBzfmNoaXJwcmFkaW8taHJkchYLEg1QbGF5bGlzdEV2ZW50GJGcrgUM",
        "lastfm_urls": {
            "med_image": "http://userserve-ak.last.fm/serve/64s/43943693.jpg",
            "sm_image": "http://userserve-ak.last.fm/serve/34s/43943693.jpg",
            "_processed": true,
            "large_image": "http://userserve-ak.last.fm/serve/174s/43943693.jpg"
        }
    }]
}
```

Here's an example of requesting the current playlist with Python's [requests](http://docs.python-requests.org/en/latest/) library:

```
import requests
res = requests.get('https://chirpradio.appspot.com/api/current_playlist?src=YOUR-SOURCE',
                   headers={'Accept-Encoding': 'gzip'})
print res.json()
```

# Statistics #

| Endpoint |  https://chirpradio.appspot.com/api/stats |
|:---------|:------------------------------------------|
| Methods supported | **GET**                                   |

Overview of JSON response:

```
{
    'this_week': {
        'start': 'YYYY-MM-DD',
        'end': 'YYYY-MM-DD',
        'releases': [
            // Array of Release objects sorted by most played.
            // This contains the top-played 40 releases for the
            // current week (i.e. today minus 7 days).
        ]
    }
}
```

Each **Release object** has the following fields.

| **Field** | **Can be NULL?** | **Description** |
|:----------|:-----------------|:----------------|
| **id**    | Not NULL         | Unique identifier for the release. This is a URL-safe ascii string. |
| **artist** | Not NULL         | Artist of the release. |
| **release** | Not NULL         | Title of the release. Could be an album name or the name of the track if it's a single. |
| **label** | Not NULL         | Name of the label the release appears on. |
| **play\_count** | Not NULL         | Average number of times this release was played on CHIRP this week. |

Example:

```
{
  "this_week": {
    "start": "2012-12-09",
    "end": "2012-12-16",
    "releases": [
      {
        "play_count": 38,
        "release": "The Odds",
        "label": "Dischord",
        "id": "bf41b36477eef1e2547e1fdd0aa8af136b1cc860",
        "artist": "The Evens"      
      },
      {
        "play_count": 37,
        "release": "The Corner Man",
        "label": "Empty Cellar",
        "id": "1a656efd2866350911c50715e1fb89838afffa5e",
        "artist": "The Cairo Gang"      
      },
      {
        "play_count": 31,
        "release": "Our House On The Hill",
        "label": "Woodsist",
        "id": "349b66242174040183e054f232a89347fe11d8e9",
        "artist": "The Babies"      
      },
      {
        "play_count": 29,
        "release": "Local Business",
        "label": "XL",
        "id": "3c147611b2ab6441fcc65215f66c3e20508af083",
        "artist": "Titus Andronicus"      
      },
      {
        "play_count": 29,
        "release": "The Bears For Lunch",
        "label": "GBV Inc.",
        "id": "7f5446aae401b0b5d75d90af90c46313eab0b0f2",
        "artist": "Guided By Voices"      
      },
      {
        "play_count": 28,
        "release": "Beyul",
        "label": "Profound Lore",
        "id": "52dd8dcc475d7ced5c5ddbceea71cf3259b4329d",
        "artist": "Yakuza"      
      },
      {
        "play_count": 26,
        "release": "Smart Bar Chicago 1985",
        "label": "Goofin'",
        "id": "78ddf3758524ab36cfbf3f4849e07c55288a5ef3",
        "artist": "Sonic Youth"      
      },
      {
        "play_count": 25,
        "release": "Free Reign",
        "label": "Domino",
        "id": "c184a054eaad56c58c3ad923e1dae9b3cb5ecb8c",
        "artist": "Clinic"      
      },
      {
        "play_count": 24,
        "release": "Secret Enigma",
        "label": "B-Music",
        "id": "f1a8649db31fffd7d56618dece8c5af977e552e6",
        "artist": "Andrzej Korzynski"      
      },
      {
        "play_count": 22,
        "release": "Behind the Mirror",
        "label": "FDH/Red Lounge",
        "id": "8ea25a4503a508fb122c10e9c2271e6b41a7bd8b",
        "artist": "Outer Minds"      
      },
      {
        "play_count": 22,
        "release": "good kid, m.A.A.d city",
        "label": "Interscope",
        "id": "8b45b810c7268dee4b7eab4d7d9de28ec05487a6",
        "artist": "Kendrick Lamar"      
      },
      {
        "play_count": 22,
        "release": "A World Out of Time",
        "label": "Thrill Jockey",
        "id": "7580a2a45693f1aa6df15a922945fbd58036fcf1",
        "artist": "Eternal Tapestry"      
      },
      {
        "play_count": 20,
        "release": "Sorry To Bother You",
        "label": "ANTI-",
        "id": "8b22881596e6321bb9a676a6355e0ae78593eba0",
        "artist": "The Coup"      
      },
      {
        "play_count": 20,
        "release": "Horizon Unlimited",
        "label": "Knitting Factory",
        "id": "2604febc42f390c6d9d3168ae5f54c6e830743a7",
        "artist": "The Lijadu Sisters"      
      },
      {
        "play_count": 18,
        "release": "Silent Congas",
        "label": "DFA",
        "id": "0cf8eca42ea1aadc67674ba0c9831e27b89264e4",
        "artist": "Larry Gus"      
      },
      {
        "play_count": 17,
        "release": "(III)",
        "label": "Casablanca",
        "id": "e105516ddd9a28eb07aa8d032ea1df33d1f31325",
        "artist": "Crystal Castles"      
      },
      {
        "play_count": 17,
        "release": "Victory",
        "label": "Fake Four Inc.",
        "id": "08b5a738ad07db6b8dff02511acff38c372432dd",
        "artist": "Child Actor"      
      },
      {
        "play_count": 17,
        "release": "True",
        "label": "Terrible",
        "id": "92d8208dc8a755d0dbea640a876c07202a3a846c",
        "artist": "Solange"      
      },
      {
        "play_count": 17,
        "release": "No Can Do",
        "label": "Triple Crown Audio",
        "id": "cbb9dd44609f16cd7997dfb2f279b5e38de7cb61",
        "artist": "Ladyhawk"      
      },
      {
        "play_count": 17,
        "release": "The Haunted Man",
        "label": "Capitol",
        "id": "2917cc4d95d1ad60195f4c97a3d14d4232f2b4c8",
        "artist": "Bat For Lashes"      
      },
      {
        "play_count": 17,
        "release": "Daughter of Cloud",
        "label": "Polyvinyl",
        "id": "d023b65f4133cc09c6c7409de44d3d0140fd86fd",
        "artist": "Of Montreal"      
      },
      {
        "play_count": 17,
        "release": "Cobra Juicy",
        "label": "Rad Cult",
        "id": "21ddb30dcbb9d1c2bf194ba12fd128bf43ed448a",
        "artist": "Black Moth Super Rainbow"      
      },
      {
        "play_count": 16,
        "release": "Form a Sign",
        "label": "Kindercore",
        "id": "e205dd60155f2548cad469c2eb298f0f56e77369",
        "artist": "Grape Soda"      
      },
      {
        "play_count": 16,
        "release": "Catacombs After Party",
        "label": "Trashy Creatures/Burger",
        "id": "e31ad4b32be6b657078fa4f2156d3ada5c93a299",
        "artist": "Tiger High"      
      },
      {
        "play_count": 16,
        "release": "The Wildfire EP",
        "label": "self-released",
        "id": "4762ac1f79dd40536fabb163429f1b03ff35b8d7",
        "artist": "The Riverbreaks"      
      },
      {
        "play_count": 16,
        "release": "Flume",
        "label": "Future Classic",
        "id": "9bc93c7cf9b286f3ee0a1a5834e7dbaafbb5652e",
        "artist": "Flume"      
      },
      {
        "play_count": 16,
        "release": "GEM",
        "label": "FatCat",
        "id": "73f1f3f7a65d700bcafbcc132a4f10e3f1e14ac5",
        "artist": "U.S. Girls"      
      },
      {
        "play_count": 16,
        "release": "Pale Fire",
        "label": "The Control Group",
        "id": "d55851c948646f8ee262f3cb6b05ee6d1037de2e",
        "artist": "El Perro Del Mar"      
      },
      {
        "play_count": 16,
        "release": "Ex-Cult",
        "label": "Goner",
        "id": "2c47bdf7c6f7076d4ceb694789b5b8f8c040d41c",
        "artist": "Ex-Cult"      
      },
      {
        "play_count": 16,
        "release": "Quarter Turns Over a Living Line",
        "label": "Blackest Ever Black",
        "id": "d86b51d2ad2166d4ece814c1e30c386fbc915aaa",
        "artist": "Raime"      
      },
      {
        "play_count": 15,
        "release": "Mumps, etc.",
        "label": "Anticon.",
        "id": "ab1bf25df39aed1aec26bc8ec2fae52631c9b326",
        "artist": "Why?"      
      },
      {
        "play_count": 15,
        "release": "Legend",
        "label": "Nuclear Blast",
        "id": "dfeb7a26100b8c52b4d931b20ef1b941f7567192",
        "artist": "Witchcraft"      
      },
      {
        "play_count": 15,
        "release": "Death Proof EP",
        "label": "Have 10p",
        "id": "dc9944fcaf53fcaac0fb94db61c9961f7cc26a2e",
        "artist": "Kate Nash"      
      },
      {
        "play_count": 15,
        "release": "2006-2008",
        "label": "Goner",
        "id": "1239b7eba2e87075b9792d17e0a136b0a5c52623",
        "artist": "The Barbaras"      
      },
      {
        "play_count": 15,
        "release": "New Relics",
        "label": "Rock Action",
        "id": "875faa064fe36f7e32688aba4a81e4d8b4fb2f66",
        "artist": "Errors"      
      },
      {
        "play_count": 15,
        "release": "3",
        "label": "galapagos4",
        "id": "cb0b82539a65a4e93367037a195c2767bae4b02f",
        "artist": "Typical Cats"      
      },
      {
        "play_count": 15,
        "release": "333",
        "label": "Latenight/Weeknight",
        "id": "580be2faf24b5768ae3fc6506befebbc852d0bd8",
        "artist": "A Shoreline Dream"      
      },
      {
        "play_count": 15,
        "release": "Sic Alps",
        "label": "Drag City",
        "id": "f6d2582d0744f53f832fc24684f035e3f0dc6285",
        "artist": "Sic Alps"      
      },
      {
        "play_count": 15,
        "release": "On Triple Beams",
        "label": "In The Red",
        "id": "54cb04589605d93bcbf83f4809d5226fbbe1f5c5",
        "artist": "Tyvek"      
      },
      {
        "play_count": 14,
        "release": "Step Inside",
        "label": "Metal Blade",
        "id": "1adba1e55fa28ce8320cc968292369386617e754",
        "artist": "Troubled Horse"      
      },
      {
        "play_count": 14,
        "release": "Lost Songs",
        "label": "Superball",
        "id": "07ca2ae30f95d62008718e781b444f933580fa87",
        "artist": "...And You Will Know Us by the Trail of Dead"      
      },
      {
        "play_count": 14,
        "release": "Golden Void",
        "label": "Thrill Jockey",
        "id": "3586aba43b573b0cdaf337426f3e2aacad8c5f81",
        "artist": "Golden Void"      
      },
      {
        "play_count": 13,
        "release": "JIAOLONG",
        "label": "Merge",
        "id": "b6fb5733701c03cd3ef37b7619ccb904d03af11f",
        "artist": "Daphni"      
      },
      {
        "play_count": 13,
        "release": "Colored Emotions",
        "label": "Domino",
        "id": "23d855dcbc19fd2aaeb0c497929776ea681fb30a",
        "artist": "Night Moves"      
      },
      {
        "play_count": 13,
        "release": "Rotted Tooth Flexi Series",
        "label": "Rotted Tooth",
        "id": "1ec53f85f9a79d4886a99c9742a27815b6d2c315",
        "artist": "Heavy Times"      
      },
      {
        "play_count": 13,
        "release": "Toys Unatic",
        "label": "Moon Glyph",
        "id": "4a88f74d9b4c1886334b85ac0cbd543acac495d3",
        "artist": "Treasure Hunt"      
      },
      {
        "play_count": 13,
        "release": "Gentle Stream",
        "label": "Partisan",
        "id": "5eb466bf95366fd46c23e1ec154723f8c888d84d",
        "artist": "The Amazing"      
      },
      {
        "play_count": 13,
        "release": "New Myth/Old Science",
        "label": "Cuneiform",
        "id": "756f5349deae87901368a18ef07724b4ea00ae03",
        "artist": "Living By Lanterns"      
      },
      {
        "play_count": 13,
        "release": "Sunshine",
        "label": "Joyful Noise",
        "id": "4cd39eef95e57d984fded8b871f31b4cb66cb8e2",
        "artist": "Talk Normal"      
      }
    ]  
  }
}
```