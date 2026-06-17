let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let put = \(_ : DVal) -> \(_ : DVal) -> {=}
let get = \(_ : DVal) -> {=}
let _ = put (DVal.DInteger +1) (DVal.DInteger +10)
let _ = get (DVal.DInteger +1)
in {=}
