let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> {=}
let _ = process (DVal.DInteger -1)
let _ = process (DVal.DInteger -2)
let _ = process (DVal.DInteger -3)
in {=}
