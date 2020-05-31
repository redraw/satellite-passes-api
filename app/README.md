# 🛰️ Satellite Passes API

Query next passes for a given satellite above you. 

Uses [PyEphem](https://github.com/brandon-rhodes/pyephem) to predict passes, and [Nasa TLE API](https://github.com/ivanstan/tle-api) to get TLE updated data taken from the greatest [CelesTrak](https://celestrak.com) website.

## API
### `GET /passes/<norad-id>`

- `lat` latitude (requeried)
- `lon` longitude (requeried)
- `limit` number of next passes

```
GET /passes/25544?lat=-34.9112212&lon=-57.9372988 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: satellites.fly.dev
User-Agent: HTTPie/1.0.3
```
Response example,
```
[
  {
    "culmination": {
      "alt": "17.38", 
      "az": "308.01", 
      "az_octant": "N", 
      "is_sunlit": true, 
      "utc_datetime": "Mon, 01 Jun 2020 14:21:49 GMT", 
      "utc_timestamp": 1591021309
    }, 
    "rise": {
      "alt": "10.00", 
      "az": "264.51", 
      "az_octant": "N", 
      "is_sunlit": true, 
      "utc_datetime": "Mon, 01 Jun 2020 14:19:29 GMT", 
      "utc_timestamp": 1591021169
    }, 
    "set": {
      "alt": "9.98", 
      "az": "351.63", 
      "az_octant": "NW", 
      "is_sunlit": true, 
      "utc_datetime": "Mon, 01 Jun 2020 14:24:08 GMT", 
      "utc_timestamp": 1591021448
    }, 
    "visible": true
  },
  ...
]
```

The `visible` field actually tells if the satellite will be _probably_ visible, considering the sun is near the horizon, and the observer is at night. You can read more [here](https://www.heavens-above.com/faq.aspx).

Source code: [github](https://github.com/redraw/satellite-passes-api)