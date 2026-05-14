let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let make_widget = \(_ : DVal) -> DVal.DBool True
let my_data = make_widget (DVal.DInteger +42) in my_data
