let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let op = \(_ : DVal) -> {=}
let _ = op (DVal.DText "hello")
in {=}
