let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = process (DVal.DInteger +1) (DVal.DInteger +42)
let _ = process (DVal.DInteger +2) (DVal.DInteger +100)
in {=}
