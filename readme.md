# Don't Asleep Bot

Don't Asleep 用に任意のルートを巡回し続ける車両を出せる、車両 Bot スクリプト

## 使い方
1. 次のような JSON ファイルを作成します
    ```json
    {
      "sleepiness": 4,
      "vehicle_type": {
        "type": "sedan",
        "color": "red"
      },
      "route": [
        {"latitude": 34.68196327829134, "longitude": 135.8177934529487},
        {"latitude": 34.6792282361953, "longitude": 135.81676348473533},
        {"latitude": 34.67856651889069, "longitude": 135.81828697938425},
        {"latitude": 34.6785135812779, "longitude": 135.81984266053985},
        {"latitude": 34.681972100861614, "longitude": 135.82051857717985}
      ]
    }
    ```
2. 次のようにして起動します
    ```bash
    $ python main.py example_vehicle.json
    ```
