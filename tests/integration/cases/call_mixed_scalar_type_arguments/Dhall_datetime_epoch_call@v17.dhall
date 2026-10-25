let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let capture = \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = capture (DVal.DDouble NaN) (DVal.DDouble Infinity) (DVal.DDouble -Infinity) (DVal.DDouble 1.25) (DVal.DText "2024-01-15") (DVal.DText +1705322096) (DVal.DText "[ordinary text]")
in {=}
