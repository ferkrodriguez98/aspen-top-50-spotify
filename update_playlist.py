import functions

# this should run only once per day

def update_playlist(radio, playlist_id):
    tracks = functions.get_songs_only_past_week(radio + "/tracks.txt")
        
    ordered_tracks = functions.top_50(tracks)

    functions.replace_playlist(ordered_tracks, playlist_id)

update_playlist("aspen", "7bZVSBqJalnab6Yl6bGk3a")
update_playlist("vorterix", "5yWsFE5mNDxV0ljNWX2EdR")
update_playlist("rock&pop", "3n1KqCxQ7J1WxDegFgTbJy")