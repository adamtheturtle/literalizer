let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let Before = \(_ : DVal) -> {=}
let _ = Before (DVal.DInteger +1)
in {=}
