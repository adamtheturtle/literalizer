let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let capture = \(_ : DVal) -> {=}
let _ = capture (DVal.DInteger +1)
in {=}
