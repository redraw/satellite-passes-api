# 🛰️ Satellite Passes API

Query next passes for a given satellite above you.

Uses [Skyfield](https://github.com/skyfielders/python-skyfield) to predict passes, and [Nasa TLE API](https://github.com/ivanstan/tle-api) to get TLE updated data taken from the greatest [CelesTrak](https://celestrak.com) website.

## API
### `GET /passes/<norad-id>`

Parameters:

- `lat` latitude (required)
- `lon` longitude (required)
- `limit` number of next passes
- `days` number of days to calculate passes ahead
- `visible_only` can be `true`/`false`, filter passes by visible passes only

```
GET /passes/25544?lat=-34.9112212&lon=-57.9372988&limit=1 HTTP/1.1
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
    "rise": {
      "alt": "10.00",
      "az": "317.05",
      "az_octant": "NW",
      "utc_datetime": "2020-06-02 05:22:20.959562+00:00",
      "utc_timestamp": 1591075340,
      "is_sunlit": false,
      "visible": false
    },
    "culmination": {
      "alt": "79.94",
      "az": "44.48",
      "az_octant": "NE",
      "utc_datetime": "2020-06-02 05:25:44.705872+00:00",
      "utc_timestamp": 1591075544,
      "is_sunlit": false,
      "visible": false
    },
    "set": {
      "alt": "10.00",
      "az": "130.38",
      "az_octant": "SE",
      "utc_datetime": "2020-06-02 05:29:10.634226+00:00",
      "utc_timestamp": 1591075750,
      "is_sunlit": false,
      "visible": false
    },
    "visible": false
  }
]
```
- `alt`/`az` are measured in degrees.
- `is_sunlit` tells if satellite is being illuminated by the sun.
- `visible` field tells if the satellite will be _probably_ visible, considering the sun is near the horizon, and the observer is at night. You can read more [here](https://www.heavens-above.com/faq.aspx).

Note: Results are cached 1 day for each parameters combo.

Source code: [github](https://github.com/redraw/satellite-passes-api)
