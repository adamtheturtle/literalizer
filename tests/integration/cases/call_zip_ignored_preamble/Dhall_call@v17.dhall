let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> DVal.DBool True
let _ = process (DVal.DInteger +1)
let _ = process (DVal.DInteger +2)
in {=}
