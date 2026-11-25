let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let Playlist = { new = \(_ : DVal) -> {=} }
let _ = Playlist.new (DVal.DInteger +1)
in {=}
