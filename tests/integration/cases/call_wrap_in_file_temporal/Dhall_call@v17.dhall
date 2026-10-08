let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let check = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = check (DVal.DText "2024-01-15T10:30:00+00:00") (DVal.DText "2024-06-01")
in {=}
