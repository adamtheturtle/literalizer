let Value = < Null | Str : Text > in
let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> {=}
let _ = process (DVal.DText "")
let _ = process (DVal.DText "hello")
in {=}
