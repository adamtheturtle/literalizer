package main
type PlaylistType_ struct{}
func (PlaylistType_) newValue(args ...any) any { return nil }
var Playlist PlaylistType_

func main() {
Playlist.newValue(1)
}
