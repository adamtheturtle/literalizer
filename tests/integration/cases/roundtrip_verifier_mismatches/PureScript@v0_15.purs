module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "true_to_one" (PDict [(Tuple "value" (PInt 1))])),
    (Tuple "one_to_true" (PDict [(Tuple "value" (PBool true))])),
    (Tuple "false_to_zero" (PDict [(Tuple "value" (PInt 0))])),
    (Tuple "zero_to_false" (PDict [(Tuple "value" (PBool false))])),
    (Tuple "nested_boolean_to_float" (PDict [(Tuple "value" (PList [PFloat 1.0]))])),
    (Tuple "nested_float_to_boolean" (PDict [(Tuple "value" (PList [PBool false]))])),
    (Tuple "nested_value_types_changed" (PDict [(Tuple "value" (PDict [(Tuple "nested" (PList [PBool true, PInt 0]))]))])),
    (Tuple "nested_value_types_reversed" (PDict [(Tuple "value" (PDict [(Tuple "nested" (PList [PInt 1, PBool false]))]))])),
    (Tuple "array_order_changed" (PDict [(Tuple "value" (PList [PInt 2, PInt 1]))])),
    (Tuple "array_length_changed" (PDict [(Tuple "value" (PList [PInt 1, PInt 2]))])),
    (Tuple "null_to_zero" (PDict [(Tuple "value" (PInt 0))])),
    (Tuple "string_to_boolean" (PDict [(Tuple "value" (PBool true))])),
    (Tuple "object_key_changed" (PDict [(Tuple "value" (PDict [(Tuple "b" (PInt 1))]))]))
]
