let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let f = \(_ : DVal) -> \(_ : DVal) -> {=}
-- calls heading
-- before call one
-- first argument
let _ = f (DVal.DInteger +1) (DVal.DInteger +2)  -- after call one
-- second argument
let _ = f (DVal.DInteger +3) (DVal.DInteger +4)
-- after all calls
in {=}
