module Main

type PlaylistType_() =
    member _.newValue(_x: obj) : obj = null
let Playlist = PlaylistType_()
type Val =
    | FInt of int64
    | FList of Val list
Playlist.newValue(FInt 1L)
