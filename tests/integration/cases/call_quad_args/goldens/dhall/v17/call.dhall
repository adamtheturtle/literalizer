let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = process (DVal.DInteger +1) (DVal.DInteger +2) (DVal.DInteger +3) (DVal.DInteger +4)
let _ = process (DVal.DInteger +5) (DVal.DInteger +6) (DVal.DInteger +7) (DVal.DInteger +8)
in {=}
