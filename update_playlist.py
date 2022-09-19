import functions

# this should run only once per day

tracks = functions.get_lines_from_file("tracks.txt")
    
ordered_tracks = functions.top_50(tracks)

functions.replace_playlist(ordered_tracks)