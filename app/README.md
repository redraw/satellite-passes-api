# Satellite Passes API 🛰️

Query next passes for a given satellite above you. 

Uses [PyEphem](https://github.com/brandon-rhodes/pyephem) to predict passes, and [Nasa TLE API](https://github.com/ivanstan/tle-api) to get TLE updated data taken from the greatest [CelesTrak](https://celestrak.com) website.

## API
### `GET /passes`

- `lat` latitude
- `lon` longitude
- `limit` number of next passes

```
GET /passes/25544?lat=-34.9112212&lon=-57.9372988&limit=1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: satellites.fly.dev
User-Agent: HTTPie/1.0.3
```

```
HTTP/1.1 200 OK
connection: close
content-encoding: gzip
content-type: application/json
date: Tue, 05 May 2020 23:53:23 GMT
server: Fly/e30ca00 (2020-05-01)
transfer-encoding: chunked

[
    {
        "start": {
            "alt": 10.0,
            "az": "S",
            "datetime": "Wed, 06 May 2020 00:31:18 GMT",
            "timestamp": 1588725078
        },
        "highest": {
            "alt": 2.3326594388342716,
            "az": "SE",
            "datetime": "Wed, 06 May 2020 00:33:52 GMT",
            "timestamp": 1588725232
        },
        "end": {
            "alt": 10.0,
            "az": "SE",
            "datetime": "Wed, 06 May 2020 00:36:25 GMT",
            "timestamp": 1588725385
        },
        "visible": false
    }
]
```
The `visible` field actually tells if the satellite will be _probably_ visible, considering the sun is near the horizon, and the observer is at night. You can read more [here](https://www.heavens-above.com/faq.aspx).