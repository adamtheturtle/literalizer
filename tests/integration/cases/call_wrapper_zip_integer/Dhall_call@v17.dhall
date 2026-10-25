let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> DVal.DBool True
let emit = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = emit (process (DVal.DInteger +1)) (DVal.DInteger +42)
in {=}
