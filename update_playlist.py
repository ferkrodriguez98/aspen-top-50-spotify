import functions

# this should run only once per day

tracks = functions.get_tracks_from_file()
    
ordered_tracks = functions.top_50(tracks)

functions.replace_playlist(ordered_tracks)