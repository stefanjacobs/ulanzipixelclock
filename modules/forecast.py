import requests, json


# use data of https://toolkit.solcast.com.au/home-pv-system for solarforecast
# use data of xxx for weather

MOCK_DATA = '{"forecasts":[{"pv_estimate":2.1868,"pv_estimate10":1.7803,"pv_estimate90":3.0101,"period_end":"2024-03-17T13:00:00.0000000Z","period":"PT30M"},{"pv_estimate":2.2316,"pv_estimate10":1.7621,"pv_estimate90":2.9148,"period_end":"2024-03-17T13:30:00.0000000Z","period":"PT30M"},{"pv_estimate":1.9254,"pv_estimate10":1.5156,"pv_estimate90":2.2406,"period_end":"2024-03-17T14:00:00.0000000Z","period":"PT30M"},{"pv_estimate":1.5339,"pv_estimate10":1.1008,"pv_estimate90":1.7348,"period_end":"2024-03-17T14:30:00.0000000Z","period":"PT30M"},{"pv_estimate":1.433,"pv_estimate10":0.9335,"pv_estimate90":1.9283,"period_end":"2024-03-17T15:00:00.0000000Z","period":"PT30M"},{"pv_estimate":1.073,"pv_estimate10":0.6341,"pv_estimate90":1.6402,"period_end":"2024-03-17T15:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.6716,"pv_estimate10":0.4078,"pv_estimate90":0.9521,"period_end":"2024-03-17T16:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.2731,"pv_estimate10":0.1869,"pv_estimate90":0.4645,"period_end":"2024-03-17T16:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.1115,"pv_estimate10":0.0727,"pv_estimate90":0.1648,"period_end":"2024-03-17T17:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.0242,"pv_estimate10":0.0145,"pv_estimate90":0.0339,"period_end":"2024-03-17T17:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T18:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T18:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T19:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T19:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T20:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T20:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T21:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T21:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T22:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T22:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T23:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-17T23:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T00:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T00:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T01:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T01:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T02:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T02:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T03:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T03:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T04:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T04:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T05:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T05:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.0099,"pv_estimate10":0.0099,"pv_estimate90":0.0149,"period_end":"2024-03-18T06:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.0794,"pv_estimate10":0.0645,"pv_estimate90":0.1042,"period_end":"2024-03-18T06:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.1986,"pv_estimate10":0.1638,"pv_estimate90":0.2482,"period_end":"2024-03-18T07:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.4385,"pv_estimate10":0.3044,"pv_estimate90":0.6007,"period_end":"2024-03-18T07:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.7147,"pv_estimate10":0.4958,"pv_estimate90":0.9795,"period_end":"2024-03-18T08:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.97,"pv_estimate10":0.6483,"pv_estimate90":1.3636,"period_end":"2024-03-18T08:30:00.0000000Z","period":"PT30M"},{"pv_estimate":1.2351,"pv_estimate10":0.8041,"pv_estimate90":1.7345,"period_end":"2024-03-18T09:00:00.0000000Z","period":"PT30M"},{"pv_estimate":1.5227,"pv_estimate10":0.9921,"pv_estimate90":2.148,"period_end":"2024-03-18T09:30:00.0000000Z","period":"PT30M"},{"pv_estimate":1.8168,"pv_estimate10":1.2003,"pv_estimate90":2.7668,"period_end":"2024-03-18T10:00:00.0000000Z","period":"PT30M"},{"pv_estimate":2.1344,"pv_estimate10":1.4132,"pv_estimate90":3.5141,"period_end":"2024-03-18T10:30:00.0000000Z","period":"PT30M"},{"pv_estimate":2.458,"pv_estimate10":1.6247,"pv_estimate90":4.2744,"period_end":"2024-03-18T11:00:00.0000000Z","period":"PT30M"},{"pv_estimate":2.6956,"pv_estimate10":1.7529,"pv_estimate90":4.7963,"period_end":"2024-03-18T11:30:00.0000000Z","period":"PT30M"},{"pv_estimate":2.853,"pv_estimate10":1.7894,"pv_estimate90":5.0698,"period_end":"2024-03-18T12:00:00.0000000Z","period":"PT30M"},{"pv_estimate":2.9888,"pv_estimate10":1.7621,"pv_estimate90":5.3997,"period_end":"2024-03-18T12:30:00.0000000Z","period":"PT30M"},{"pv_estimate":3.1197,"pv_estimate10":1.6805,"pv_estimate90":5.6927,"period_end":"2024-03-18T13:00:00.0000000Z","period":"PT30M"},{"pv_estimate":3.0682,"pv_estimate10":1.5269,"pv_estimate90":5.7034,"period_end":"2024-03-18T13:30:00.0000000Z","period":"PT30M"},{"pv_estimate":2.8397,"pv_estimate10":1.3356,"pv_estimate90":5.4863,"period_end":"2024-03-18T14:00:00.0000000Z","period":"PT30M"},{"pv_estimate":2.52,"pv_estimate10":1.1157,"pv_estimate90":4.6762,"period_end":"2024-03-18T14:30:00.0000000Z","period":"PT30M"},{"pv_estimate":2.1191,"pv_estimate10":0.8851,"pv_estimate90":3.7742,"period_end":"2024-03-18T15:00:00.0000000Z","period":"PT30M"},{"pv_estimate":1.6046,"pv_estimate10":0.6623,"pv_estimate90":2.8059,"period_end":"2024-03-18T15:30:00.0000000Z","period":"PT30M"},{"pv_estimate":1.0787,"pv_estimate10":0.4287,"pv_estimate90":1.8395,"period_end":"2024-03-18T16:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.6108,"pv_estimate10":0.2226,"pv_estimate90":0.9241,"period_end":"2024-03-18T16:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.2463,"pv_estimate10":0.1042,"pv_estimate90":0.258615,"period_end":"2024-03-18T17:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.0671,"pv_estimate10":0.0287,"pv_estimate90":0.0705,"period_end":"2024-03-18T17:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T18:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T18:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T19:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T19:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T20:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T20:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T21:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T21:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T22:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T22:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T23:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-18T23:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T00:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T00:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T01:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T01:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T02:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T02:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T03:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T03:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T04:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T04:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T05:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0,"pv_estimate10":0,"pv_estimate90":0,"period_end":"2024-03-19T05:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.0151,"pv_estimate10":0.005,"pv_estimate90":0.0301,"period_end":"2024-03-19T06:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.0943,"pv_estimate10":0.0397,"pv_estimate90":0.1787,"period_end":"2024-03-19T06:30:00.0000000Z","period":"PT30M"},{"pv_estimate":0.2333,"pv_estimate10":0.0993,"pv_estimate90":0.5432,"period_end":"2024-03-19T07:00:00.0000000Z","period":"PT30M"},{"pv_estimate":0.5626,"pv_estimate10":0.2035,"pv_estimate90":1.4958,"period_end":"2024-03-19T07:30:00.0000000Z","period":"PT30M"},{"pv_estimate":1.0296,"pv_estimate10":0.32,"pv_estimate90":3.1613,"period_end":"2024-03-19T08:00:00.0000000Z","period":"PT30M"},{"pv_estimate":1.5042,"pv_estimate10":0.5011,"pv_estimate90":4.5397,"period_end":"2024-03-19T08:30:00.0000000Z","period":"PT30M"},{"pv_estimate":1.9079,"pv_estimate10":0.6481,"pv_estimate90":5.4118,"period_end":"2024-03-19T09:00:00.0000000Z","period":"PT30M"},{"pv_estimate":2.5001,"pv_estimate10":0.8269,"pv_estimate90":6.2572,"period_end":"2024-03-19T09:30:00.0000000Z","period":"PT30M"},{"pv_estimate":3.388,"pv_estimate10":1.0266,"pv_estimate90":6.8867,"period_end":"2024-03-19T10:00:00.0000000Z","period":"PT30M"},{"pv_estimate":4.1982,"pv_estimate10":1.2327,"pv_estimate90":7.33,"period_end":"2024-03-19T10:30:00.0000000Z","period":"PT30M"},{"pv_estimate":4.958,"pv_estimate10":1.4253,"pv_estimate90":7.8066,"period_end":"2024-03-19T11:00:00.0000000Z","period":"PT30M"},{"pv_estimate":5.4371,"pv_estimate10":1.5541,"pv_estimate90":7.9167,"period_end":"2024-03-19T11:30:00.0000000Z","period":"PT30M"},{"pv_estimate":5.7236,"pv_estimate10":1.6176,"pv_estimate90":7.8459,"period_end":"2024-03-19T12:00:00.0000000Z","period":"PT30M"},{"pv_estimate":5.4863,"pv_estimate10":1.5641,"pv_estimate90":7.4696,"period_end":"2024-03-19T12:30:00.0000000Z","period":"PT30M"},{"pv_estimate":4.9326,"pv_estimate10":1.4011,"pv_estimate90":7.1193,"period_end":"2024-03-19T13:00:00.0000000Z","period":"PT30M"}]}'

WEATHER_CLOUDY = [0,0,2112,16800,65312,58816,27360,2112,0,2112,21056,58848,65248,65216,58880,27360,0,12674,50466,65184,65344,65312,65216,58816,0,50744,59160,65152,65376,65344,65248,65312,65535,65535,65535,59231,59199,65188,58848,16800,59196,65535,65535,65535,65535,57016,29544,2144,59196,65503,65535,65535,65535,63390,50711,2145,59196,59196,59196,59196,59196,61277,54970,4226]

WEATHER_SNOW = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,35953,35953,0,0,0,0,0,42260,54938,46518,35953,0,0,0,0,42260,54938,54970,54938,0,0,0,0,61277,61277,54938,46518,0,0,0,0,52825,54970,48599,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,35953,35953,0,0,54938,42260,0,42260,54938,46518,35953,54938,65535,61277,0,42260,54938,54970,54938,65535,65535,65535,65535,61277,61277,54938,46518,0,35953,42260,46518,52825,54970,48599,0],[0,0,0,0,0,35953,35953,0,0,54938,42260,0,42260,54938,46518,35953,54938,65535,61277,0,42260,54938,54970,54938,65535,65535,65535,65535,61277,61277,54938,46518,0,35953,42260,46518,52825,54970,48599,0,0,0,0,0,65535,0,0,0,0,65535,0,0,0,0,65535,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,35953,35953,0,0,54938,42260,0,42260,54938,46518,35953,54938,65535,61277,0,42260,54938,54970,54938,65535,65535,65535,65535,61277,61277,54938,46518,0,35953,42260,46518,52825,54970,48599,0,0,0,0,65535,0,0,0,0,0,65535,0,0,0,0,0,0,0,0,0,0,0,65535,0,0],[0,0,0,0,0,35953,35953,0,0,54938,42260,0,42260,54938,46518,35953,54938,65535,61277,0,42260,54938,54970,54938,65535,65535,65535,65535,61277,61277,54938,46518,0,35953,42260,46518,52825,54970,48599,0,0,0,0,0,0,0,65535,0,0,0,0,65535,0,0,0,0,0,65535,0,0,0,65535,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,35953,35953,0,0,54938,42260,0,42260,54938,46518,35953,54938,65535,61277,0,42260,54938,54970,54938,65535,65535,65535,65535,61277,61277,54938,46518,0,35953,42260,46518,52825,54970,48599,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,54938,42260,0,42260,0,0,0,54938,65535,61277,0,42260,0,0,0,65535,65535,65535,65535,61277,0,0,0,0,35953,42260,46518,52825],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,54938,0,0,0,0,0,0,0,65535,0,0,0,0,0,0,0,0]


WEATHER_RAIN = [0,0,0,0,0,16904,16904,0,0,16904,16904,0,16904,59196,59196,16904,16904,50744,50744,16904,50744,50744,50744,50744,42260,42260,42260,42260,42260,42260,42260,42260,16904,27501,27501,27501,27501,27501,27501,16904,0,16904,16904,16904,16904,16904,19257,0,0,0,19257,0,0,0,0,0,0,0,0,0,19257,0,0,0],[0,0,0,0,0,16904,16904,0,0,16904,16904,0,16904,59196,59196,16904,16904,50744,50744,16904,50744,50744,50744,50744,42260,42260,42260,42260,42260,42260,42260,42260,16904,27501,27501,27501,27501,27501,27501,16904,0,16904,16904,16904,16904,16904,0,0,0,0,0,0,0,0,19257,0,0,0,19257,0,0,0,0,0],[0,0,0,0,0,16904,16904,0,0,16904,16904,0,16904,59196,59196,16904,16904,50744,50744,16904,50744,50744,50744,50744,42260,42260,42260,42260,42260,42260,42260,42260,16904,27501,27501,27501,27501,27501,27501,16904,0,19257,16904,16904,16904,16904,0,0,0,0,0,0,19257,0,0,0,0,0,0,0,0,0,19257,0],[0,0,0,0,0,16904,16904,0,0,16904,16904,0,16904,59196,59196,16904,16904,50744,50744,16904,50744,50744,50744,50744,42260,42260,42260,42260,42260,42260,42260,42260,16904,27501,27501,27501,27501,27501,27501,19257,0,16904,16904,16904,16904,16904,0,0,0,19257,0,0,0,0,0,0,0,0,0,0,19257,0,0,0],[0,0,0,0,0,16904,16904,0,0,16904,16904,0,16904,59196,59196,16904,16904,50744,50744,16904,50744,50744,50744,50744,42260,42260,42260,42260,42260,42260,42260,42260,16904,27501,27501,27501,27501,27501,27501,16904,0,16904,16904,16904,16904,16904,0,19257,0,0,0,0,0,0,0,0,0,19257,0,0,0,0,0,0],[0,0,0,0,0,16904,16904,0,0,16904,16904,0,16904,59196,59196,16904,16904,50744,50744,16904,50744,50744,50744,50744,42260,42260,42260,42260,42260,42260,42260,42260,16904,27501,27501,27501,27501,27501,27501,16904,0,16904,16904,16904,16904,16904,0,0,0,0,0,19257,0,0,0,19257,0,0,0,0,0,0,0,0],[0,0,0,0,0,16904,16904,0,0,16904,16904,0,16904,59196,59196,16904,16904,50744,50744,16904,50744,50744,50744,50744,42260,42260,42260,42260,42260,42260,42260,42260,16904,27501,27501,27501,27501,27501,27501,16904,0,16904,16904,16904,16904,16904,0,0,0,0,0,0,0,0,0,0,0,0,0,19257,0,0,0,19257]

WEATHER_SUN = [65457,65376,65376,65216,56768,46272,0,65440,65376,65376,65216,65216,56768,0,0,0,65376,65216,65216,56768,56768,0,0,0,65216,65216,56768,56768,0,0,65440,0,56768,56768,56768,0,0,0,0,0,46272,0,0,0,0,0,0,0,0,0,0,65440,0,0,0,0,65440,0,0,0,0,0,0,0]

GREEN = "#32612D"

def updateUlanzi(config, text, picture):
    uri = config.get("ulanzi.uri")
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'sleepMode': False,
        'switchAnimation': {
            'aktiv': True,
            'animation': 'fade',
        },
        'bitmap': {
            'data': picture, 
            'position': {
                'x': 0,
                'y': 0,
            },
            'size': {
                'width': 8,
                'height': 8,
            },
        },
        'text': {
            'textString': text,
            'bigFont': False,
            'scrollText': False,
            'scrollTextDelay': 0,
            'centerText': True,
            'position': {
                'x': 7,
                'y': 1,
            },
            'hexColor': GREEN,
        },
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()

import os, datetime

now = datetime.datetime.now(datetime.timezone.utc)
lastUpdate = now - datetime.timedelta(minutes=241)
inputPower = 0


def formatValue(val):
    val = round(val)
    # check, if W or kW
    einheit = "Wh"
    if abs(val) > 999:
        val = round(val/1000)
        einheit = "kWh"

    # format watt string
    value = str(val) + einheit
    return value


def getForecast(step):
    SOL_ID = os.getenv("SOL_ID")
    SOL_TOKEN = os.getenv("SOL_TOKEN")
    url = "https://api.solcast.com.au/rooftop_sites/" + SOL_ID + "/forecasts?format=json"

    payload={}
    headers = {
        'Authorization': 'Bearer ' + SOL_TOKEN
    }
    # response = requests.request("GET", url, headers=headers, data=payload)
    # response.raise_for_status()
    # solar_forecast = json.loads(response.text)
    solar_forecast = json.loads(MOCK_DATA)
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    solar_forecast = [f for f in solar_forecast["forecasts"] if tomorrow in f["period_end"] and f['pv_estimate'] != 0]
    forecast = 0
    for x in solar_forecast:
        forecast += x["pv_estimate"] * 0.5
    return round(forecast*1000)


def update(config, step):
    global lastUpdate, inputPower
    now = datetime.datetime.now(datetime.timezone.utc)
    if now - lastUpdate > datetime.timedelta(hours=4):
        # perform update of solar forecast data, power
        inputPower = getForecast(step)
        pass

    
    value = formatValue(inputPower)

    updateUlanzi(config, value, WEATHER_CLOUDY)
    return True




if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    import config
    c = config.Config("cfg/config.yml")
    step = [s for s in c.get("show") if s["name"] == "forecast"]
    update(c, step)