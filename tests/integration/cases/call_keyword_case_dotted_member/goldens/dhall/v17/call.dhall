let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let thing = { Before = \(_ : DVal) -> {=} }
let _ = thing.Before (DVal.DInteger +1)
in {=}
