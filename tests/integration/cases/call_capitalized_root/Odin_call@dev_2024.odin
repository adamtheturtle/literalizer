#+feature dynamic-literals
package main
_Playlist_new_ :: proc(args: ..any) -> any { return nil }
PlaylistType_ :: struct { new: proc(..any) -> any }

main :: proc() {
Playlist: PlaylistType_ = PlaylistType_{ new = _Playlist_new_ }
Playlist.new(1);
Playlist.new(2);
}
