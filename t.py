import requests

url = 'https://api.jollymax.com/jolly-gateway/topup/order/check-uid'
userId = 'sd'
data = {
    'activityId':"",
    'appAlias': "BrawlStars",
    'appId': "APP20230525120453002",
    'country': "ru",
    'deviceId': "d78de2660eda41c9bac5c13dab8bb4d0",
    'domain': "www.jollymax.com",
    'goodsId':"G20240430171324902",
    'jmsId': "",
    'language': "ru",
    'payTypeId': "926454",
    'platformName': "",
    'roleName':"",
    'serverId': "",
    'serverName': "",
    'token': "ea84a4d8e538486e8cb5e9e79b7e968e",
    'userId': userId,
}

print(requests.post(url, json=data, headers={'Content-Type': 'application/json'}).json())
