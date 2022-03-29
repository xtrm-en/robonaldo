try:
    import rsk2 as rsk
except:
    import rsk

with rsk.Client(host='172.19.39.223') as client:
    client.stop_motion()