import soundcloud

def get_soundcloud_client():
    return soundcloud.Client(
            client_id='296ab7d5973f378289cc72d56dc8eded',
            client_secret='1e2b27302f0893328749d4aeb714e3ab',
            #TODO: not hardcode
            redirect_uri='http://www.soundcloudcontest.com/soundcloud_signin'
        )

