module Main

type PlaylistType_() =
    member _.new(_x: obj) : obj = null
let Playlist = PlaylistType_()
type Val =
    | FInt of int64
    | FList of Val list
Playlist.new(FInt 1L)
