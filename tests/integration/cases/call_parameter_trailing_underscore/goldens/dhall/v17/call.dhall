let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let f = \(_ : DVal) -> {=}
let _ = f (DVal.DInteger +1)
in {=}
