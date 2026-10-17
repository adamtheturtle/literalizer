package main

type Playlist struct { value int }

func NewPlaylist() Playlist { return Playlist{value: 42} }

func main() {
static auto p = Playlist();
if p.value != 42 { panic("Expected constructor result") }
}
