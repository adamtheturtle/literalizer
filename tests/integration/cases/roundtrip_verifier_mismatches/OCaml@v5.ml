module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("true_to_one", OMap [("value", OInt 1)]);
    ("one_to_true", OMap [("value", OBool true)]);
    ("false_to_zero", OMap [("value", OInt 0)]);
    ("zero_to_false", OMap [("value", OBool false)]);
    ("nested_boolean_to_float", OMap [("value", OList [OFloat 1.0])]);
    ("nested_float_to_boolean", OMap [("value", OList [OBool false])]);
    ("nested_value_types_changed", OMap [("value", OMap [("nested", OList [OBool true; OInt 0])])]);
    ("nested_value_types_reversed", OMap [("value", OMap [("nested", OList [OInt 1; OBool false])])]);
    ("array_order_changed", OMap [("value", OList [OInt 2; OInt 1])]);
    ("array_length_changed", OMap [("value", OList [OInt 1; OInt 2])]);
    ("null_to_zero", OMap [("value", OInt 0)]);
    ("string_to_boolean", OMap [("value", OBool true)]);
    ("object_key_changed", OMap [("value", OMap [("b", OInt 1)])])
]

end
