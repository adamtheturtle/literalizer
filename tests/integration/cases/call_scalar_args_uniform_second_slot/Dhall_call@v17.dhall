let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = process (DVal.DText "hello") (DVal.DText "a")
let _ = process (DVal.DInteger +42) (DVal.DText "b")
let _ = process (DVal.DBool True) (DVal.DText "c")
in {=}
