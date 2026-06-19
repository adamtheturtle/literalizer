let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let store_item = \(_ : DVal) -> \(_ : DVal) -> {=}
let read_item = \(_ : DVal) -> {=}
let _ = store_item (DVal.DInteger +1) (DVal.DInteger +10)
let _ = read_item (DVal.DInteger +1)
in {=}
