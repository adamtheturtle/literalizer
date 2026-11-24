pub type GVal {
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("true_to_one", GDict([#("value", GInt(1))])),
    #("one_to_true", GDict([#("value", GBool(True))])),
    #("false_to_zero", GDict([#("value", GInt(0))])),
    #("zero_to_false", GDict([#("value", GBool(False))])),
    #("nested_boolean_to_float", GDict([#("value", GList([GFloat(1.0)]))])),
    #("nested_float_to_boolean", GDict([#("value", GList([GBool(False)]))])),
    #("nested_value_types_changed", GDict([#("value", GDict([#("nested", GList([GBool(True), GInt(0)]))]))])),
    #("nested_value_types_reversed", GDict([#("value", GDict([#("nested", GList([GInt(1), GBool(False)]))]))])),
    #("array_order_changed", GDict([#("value", GList([GInt(2), GInt(1)]))])),
    #("array_length_changed", GDict([#("value", GList([GInt(1), GInt(2)]))])),
    #("null_to_zero", GDict([#("value", GInt(0))])),
    #("string_to_boolean", GDict([#("value", GBool(True))])),
    #("object_key_changed", GDict([#("value", GDict([#("b", GInt(1))]))])),
  ])
  let _ = my_data
}
