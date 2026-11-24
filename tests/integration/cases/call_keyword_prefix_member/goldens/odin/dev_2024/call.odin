#+feature dynamic-literals
package main
_Playlist_newValue_ :: proc(args: ..any) -> any { return nil }
PlaylistType_ :: struct { newValue: proc(..any) -> any }

main :: proc() {
Playlist: PlaylistType_ = PlaylistType_{ newValue = _Playlist_newValue_ }
Playlist.newValue(1);
}
