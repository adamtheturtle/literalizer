: my_data
+obj
    s\" true_to_one" +key +obj s\" value" +key 1 +int -obj
    s\" one_to_true" +key +obj s\" value" +key true +bool -obj
    s\" false_to_zero" +key +obj s\" value" +key 0 +int -obj
    s\" zero_to_false" +key +obj s\" value" +key false +bool -obj
    s\" nested_boolean_to_float" +key +obj s\" value" +key +arr 1.0e0 +float -arr -obj
    s\" nested_float_to_boolean" +key +obj s\" value" +key +arr false +bool -arr -obj
    s\" nested_value_types_changed" +key +obj s\" value" +key +obj s\" nested" +key +arr true +bool 0 +int -arr -obj -obj
    s\" nested_value_types_reversed" +key +obj s\" value" +key +obj s\" nested" +key +arr 1 +int false +bool -arr -obj -obj
    s\" array_order_changed" +key +obj s\" value" +key +arr 2 +int 1 +int -arr -obj
    s\" array_length_changed" +key +obj s\" value" +key +arr 1 +int 2 +int -arr -obj
    s\" null_to_zero" +key +obj s\" value" +key 0 +int -obj
    s\" string_to_boolean" +key +obj s\" value" +key true +bool -obj
    s\" object_key_changed" +key +obj s\" value" +key +obj s\" b" +key 1 +int -obj -obj
 -obj
;
