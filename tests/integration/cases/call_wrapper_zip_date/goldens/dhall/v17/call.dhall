let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> DVal.DBool True
let emit = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = emit (process (DVal.DInteger +1)) (DVal.DText "2024-01-15")
in {=}
