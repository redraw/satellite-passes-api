# |
# 🛰️ Groundtrack API Query next passes for a given satellite above you.
# |
# Uses
# | [Skyfield](https://github.com/skyfielders/python-skyfield) to predict passes, and 
# | [Celestrak GP API](https://celestrak.com/NORAD/documentation/gp-data-formats.php) to get updated TLE data.
# | [GitHub](https://github.com/redraw/satellite-passes-api) 
# | [Docs](https://satellites.fly.dev/docs) 
# | [openapi.json](https://github.com/redraw/satellite-passes-api/blob/master/app/static/openapi.json)
-----------------------------------------------------------
## API ### GET 
`/passes/<norad-id>`
`"Schema".$_-0/"=enum referenceFrame:` 
 `.$_-0/byte {`
`/// Earth Mean Equator and Equinox of J2000`
# |`EME2000,
# |`///  Geocentric Celestial Reference Frame
# |`GCRF,
# |`/// Greenwich Rotating Coordinates
# |`GRC,
# |`/// International Celestial Reference Frame
# |`ICRF,
# |`/// International Terrestrial Reference Frame 2000
# |`ITRF2000,
# |`/// International Terrestrial Reference Frame 1993
# |`ITRF93, 
# |`/// International Terrestrial Reference Frame 1997
# |`ITRF97,
# |`/// Mars Centered Inertial
# |`MCI,
# |`/// True of Date, Rotating
# |`TDR,
# |`/// True Equator Mean Equinox
# |`TEME,
# |`/// True of Date
# |`TOD, }`
# |`
# |`enum timeSystem : byte {
# |`  /// Greenwich Mean Sidereal Time
# |`  GMST,
# |`  /// Global Positioning System
# |`  GPS,
# |`  /// Mission Elapsed Time
# |`  MET,
# |`  /// Mission Relative Time
# |`  MRT,
# |`  /// Spacecraft Clock (receiver) (requires rules for interpretation in ICD)
# |`  SCLK,
# |`  /// International Atomic Time
# |`  TAI,
# |`  /// Barycentric Coordinate Time
# |`  TCB,
# |`  /// Barycentric Dynamical Time
# |`  TDB,
# |`  /// Geocentric Coordinate Time
# |`  TCG,
# |`  /// Terrestrial Time
# |`  TT,
# |`  /// Universal Time
# |`  UT1,
# |`  /// Coordinated Universal Time 
# |`  UTC
# |`}
# |`
# |`enum meanElementTheory : byte {
# |`  /// Simplified General Perturbation Model  4
# |`  SGP4,
# |`  /// Draper Semi-analytical Satellite Theory
# |`  DSST,
# |`  /// Universal Semianalytical Method
# |`  USM
# |`}
# |`
# |`table MPE {  
# |`  ENTITY_ID: string;
# |`  EPOCH: double;
# |`  MEAN_MOTION: double;
# |`  ECCENTRICITY: double;
# |`  INCLINATION: double;
# |`  RA_OF_ASC_NODE: double;
# |`  ARG_OF_PERICENTER: double;
# |`  MEAN_ANOMALY: double;
# |`  BSTAR: double;
# |`}
# |`
# |`table MPECOLLECTION {
# |`  CLASSIFICATION_TYPE: string;
# |`  REF_FRAME:referenceFrame = TEME;
# |`  REF_FRAME_EPOCH: double;
# |`  TIME_SYSTEM:timeSystem = UTC;
# |`  MEAN_ELEMENT_THEORY:meanElementTheory = SGP4;
# |`  RECORDS:[MPE];
# |`"root""$_type" 
# |`"MPE";
# |`"$file_identifier" 
# |`"$MPE";`
# |`---
# |`Parameters`:
# |`Flask`==`1.1.2`
# |`redis`==`3.5.0`
# |`hiredis`==`1.0.1`
# |`gunicorn`==`20.0.4`
# |`requests`==`2.23.0`
# |`marshmallow`==`3.5.2`
# |`Markdown`==`3.2.1`
# |`more-itertools`==`8.2.0`
# |`skyfield`==`1.39`
# |`Flask-Cors`==`3.0.9`
# |`flask-swagger-ui`==`3.36.0`
# |`+itsdangerous`==`2.0.1`
# |`- `lat` latitude (required)
# |`- `lon` longitude (required)
# |`- `limit` number of next passes
# |`- `days` number of days to calculate passes ahead
# |`- `visible_only` can be `true`/`false`, filter passes by visible passes only
# |`---
# |```
# |`GET /passes/25544?lat=-34.9112212&lon=-57.9372988&limit=1 HTTP/1.1
# |`Accept: */*
# |`Accept-Encoding: gzip, deflate
# |`Connection: keep-alive
# |`Host: satellites.fly.dev
# |`User-Agent: HTTPie/1.0.3
# |```
# |`Response example,
# |```
# |`[
# |`  {
# |`    "rise": {
# |`      "alt": "10.00",
# |`      "az": "317.05",
# |`      "az_octant": "NW",
# |`      "utc_datetime": "2020-06-02 05:22:20.959562+00:00",
# |`      "utc_timestamp": 1591075340,
# |`      "is_sunlit": false,
# |`      "visible": false
# |`    },
# |`    "culmination": {
# |`      "alt": "79.94",
# |`      "az": "44.48",
# |`      "az_octant": "NE",
# |`      "utc_datetime": "2020-06-02 05:25:44.705872+00:00",
# |`      "utc_timestamp": 1591075544,
# |`      "visible": false    },
# |`    "set": {
# |`      "alt": "10.00",
# |`      "az": "130.38",
# |`      "az_octant": "SE",
# |`      "utc_datetime": "2020-06-02 05:29:10.634226+00:00",
# |`      "utc_timestamp": 1591075750,
# |`      "is_sunlit": false,
# |`      "visible": false
# |`    },
# |`    "visible": false
# |`  }
# |`]
# |```
# |`- `alt`/`az` are measured in degrees.
# |`- `is_sunlit` tells if satellite is being illuminated by the sun.
# |`- `visible` field tells if the satellite will be _probably_ visible, considering the sun is near the horizon, and the observer is at night. You can # |`read more [here](https://www.heavens-above.com/faq.aspx).
# |`
# |`Note: Results are cached 1 day for each parameters combo, except `limit`.`
# |----------------------------------------------------`
