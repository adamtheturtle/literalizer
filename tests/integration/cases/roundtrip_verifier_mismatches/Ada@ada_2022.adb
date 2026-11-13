with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("true_to_one", AMap'[AEntry ("value", AInt (1))]),
        AEntry ("one_to_true", AMap'[AEntry ("value", ABool (True))]),
        AEntry ("false_to_zero", AMap'[AEntry ("value", AInt (0))]),
        AEntry ("zero_to_false", AMap'[AEntry ("value", ABool (False))]),
        AEntry ("nested_boolean_to_float", AMap'[AEntry ("value", AList'[AFloat (1.0)])]),
        AEntry ("nested_float_to_boolean", AMap'[AEntry ("value", AList'[ABool (False)])]),
        AEntry ("nested_value_types_changed", AMap'[AEntry ("value", AMap'[AEntry ("nested", AList'[ABool (True), AInt (0)])])]),
        AEntry ("nested_value_types_reversed", AMap'[AEntry ("value", AMap'[AEntry ("nested", AList'[AInt (1), ABool (False)])])]),
        AEntry ("array_order_changed", AMap'[AEntry ("value", AList'[AInt (2), AInt (1)])]),
        AEntry ("array_length_changed", AMap'[AEntry ("value", AList'[AInt (1), AInt (2)])]),
        AEntry ("null_to_zero", AMap'[AEntry ("value", AInt (0))]),
        AEntry ("string_to_boolean", AMap'[AEntry ("value", ABool (True))]),
        AEntry ("object_key_changed", AMap'[AEntry ("value", AMap'[AEntry ("b", AInt (1))])])
    ];
begin
    null;
end Main;
