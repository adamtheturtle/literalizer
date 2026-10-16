let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let f = \(_ : DVal) -> {=}
-- scalar heading
-- second heading line
-- scalar inline
-- inline continuation
-- scalar trailing
let _ = f (DVal.DInteger +42)
in {=}
