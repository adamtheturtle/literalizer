let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = process (DVal.DInteger +1) (DVal.DText "hello")
let _ = process (DVal.DText "two") (DVal.DBool False)
let _ = process (DVal.DDouble 3.5) (DVal.DText "")
in {=}
