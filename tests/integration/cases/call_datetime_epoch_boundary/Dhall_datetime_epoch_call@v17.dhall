let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let consume = \(_ : DVal) -> {=}
let _ = consume (DVal.DInteger -2147483649)
let _ = consume (DVal.DInteger +2147483648)
in {=}
