let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let helper = { list = \(_ : DVal) -> {=} }
let _ = helper.list (DVal.DInteger +1)
in {=}
