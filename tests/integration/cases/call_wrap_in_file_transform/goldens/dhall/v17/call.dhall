let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> \(_ : DVal) -> DVal.DBool True
let my_data = process (DVal.DInteger +1) (DVal.DInteger +2) in my_data
