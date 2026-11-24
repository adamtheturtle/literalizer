package main
type PlaylistType_ struct{}
func (PlaylistType_) new(args ...any) any { return nil }
var Playlist PlaylistType_

func main() {
Playlist.new(1)
}
