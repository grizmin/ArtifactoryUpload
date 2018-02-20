### ArtifactoryUpload wrapper

This tool executes jfrog cli with 5 minutes timeout.
If jfrog upload hangs due to unknown reason it will kill the invoked
subprocess and handle exit code properly.

* sample usage:
```angular2html
konstantin@bg-hs:~/scripts$ ./ArtifactoryUpload.py -bv 18.3.0.95
[INFO] Starting ./ArtifactoryUpload.py on 2018-02-20 02:30:30.579492 with params: ['-bv', '18.3.0.95']
[Info] [Thread 9] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_node-18.3.0.95-lib.zip
[Info] [Thread 6] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_node_aggregated-18.3.0.95.jar
[Info] [Thread 3] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_game_aggregated-18.3.0.95-lib.zip
[Info] [Thread 15] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_publisher_ng-18.3.0.95.jar
[Info] [Thread 8] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_node-18.3.0.95.jar
[Info] [Thread 5] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_publisher_ng-18.3.0.95-lib.zip
[Info] [Thread 12] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_gateway-18.3.0.95-lib.zip
[Info] [Thread 10] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_network_api-18.3.0.95.war
[Info] [Thread 13] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_game-18.3.0.95.jar
[Info] [Thread 4] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_lobby-18.3.0.95.jar
[Info] [Thread 11] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_lobby-18.3.0.95-lib.zip
[Info] [Thread 1] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_game_aggregated-REPLAYER-18.3.0.95.jar
[Info] [Thread 14] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_gateway-18.3.0.95.jar
[Info] [Thread 0] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_game_aggregated-REPLAYER-18.3.0.95-lib.zip
[Info] [Thread 7] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_node_aggregated-18.3.0.95-lib.zip
[Info] [Thread 2] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_game_aggregated-18.3.0.95.jar
[Info] [Thread 6] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_game-18.3.0.95-lib.zip
[Info] [Thread 15] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_channel-18.3.0.95.jar
[Info] [Thread 4] Uploading artifact: /dserver/poker/18.3/0.95/server/poker_channel-18.3.0.95-lib.zip
{
  "status": "success",
  "totals": {
    "success": 19,
    "failure": 0
  }
}
[INFO] [*] Files were uploaded successfully for 7.33 seconds.
konstantin@bg-hs:~/scripts$


```

###### Author Konstantin Krastev <grizmin@gmail.com>