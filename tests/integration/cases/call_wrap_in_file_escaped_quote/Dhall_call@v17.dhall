let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> {=}
let _ = process (DVal.DText "a\"b")
in {=}
