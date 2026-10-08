let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let f = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = f (DVal.DInteger +1) (DVal.DInteger +2)
in {=}
