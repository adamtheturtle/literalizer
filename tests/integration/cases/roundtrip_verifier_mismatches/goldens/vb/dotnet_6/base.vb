Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"true_to_one", New Dictionary(Of String, Object) From {{"value", 1}}},
        {"one_to_true", New Dictionary(Of String, Object) From {{"value", True}}},
        {"false_to_zero", New Dictionary(Of String, Object) From {{"value", 0}}},
        {"zero_to_false", New Dictionary(Of String, Object) From {{"value", False}}},
        {"nested_boolean_to_float", New Dictionary(Of String, Object) From {{"value", New Double() {1.0}}}},
        {"nested_float_to_boolean", New Dictionary(Of String, Object) From {{"value", New Boolean() {False}}}},
        {"nested_value_types_changed", New Dictionary(Of String, Object) From {{"value", New Dictionary(Of String, Object) From {{"nested", New Object() {True, 0}}}}}},
        {"nested_value_types_reversed", New Dictionary(Of String, Object) From {{"value", New Dictionary(Of String, Object) From {{"nested", New Object() {1, False}}}}}},
        {"array_order_changed", New Dictionary(Of String, Object) From {{"value", New Integer() {2, 1}}}},
        {"array_length_changed", New Dictionary(Of String, Object) From {{"value", New Integer() {1, 2}}}},
        {"null_to_zero", New Dictionary(Of String, Object) From {{"value", 0}}},
        {"string_to_boolean", New Dictionary(Of String, Object) From {{"value", True}}},
        {"object_key_changed", New Dictionary(Of String, Object) From {{"value", New Dictionary(Of String, Object) From {{"b", 1}}}}}
    }
End Module
