let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = process (DVal.DInteger +1) (DVal.DInteger +2)
let _ = process (DVal.DInteger +3) (DVal.DInteger +4)
in {=}
