let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let make_widget = \(_ : DVal) -> {=}
let _ = make_widget (DVal.DInteger +1)
in {=}
