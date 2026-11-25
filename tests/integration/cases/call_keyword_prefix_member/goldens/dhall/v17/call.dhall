let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let Playlist = { newValue = \(_ : DVal) -> {=} }
let _ = Playlist.newValue (DVal.DInteger +1)
in {=}
