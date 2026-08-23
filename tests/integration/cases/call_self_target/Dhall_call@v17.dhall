let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let self = \(_ : DVal) -> {=}
let _ = self (DVal.DText "hello")
in {=}
