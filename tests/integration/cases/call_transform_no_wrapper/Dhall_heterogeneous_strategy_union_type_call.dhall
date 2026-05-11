let Value = < Str : Text | Int : Integer | Bool : Bool > in
let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> DVal.DBool True
let _ = process (DVal.DText "hello")
let _ = process (DVal.DInteger +42)
let _ = process (DVal.DBool True)
in {=}
