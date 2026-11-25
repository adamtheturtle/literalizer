class Fixture_roundtrip_verifier_mismatches_Haxe {
    public static function main() {
        final my_data = ([
            "true_to_one" => (["value" => 1] : Map<String, Dynamic>),
            "one_to_true" => (["value" => true] : Map<String, Dynamic>),
            "false_to_zero" => (["value" => 0] : Map<String, Dynamic>),
            "zero_to_false" => (["value" => false] : Map<String, Dynamic>),
            "nested_boolean_to_float" => (["value" => ([1.0] : Array<Dynamic>)] : Map<String, Dynamic>),
            "nested_float_to_boolean" => (["value" => ([false] : Array<Dynamic>)] : Map<String, Dynamic>),
            "nested_value_types_changed" => (["value" => (["nested" => ([true, 0] : Array<Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>),
            "nested_value_types_reversed" => (["value" => (["nested" => ([1, false] : Array<Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>),
            "array_order_changed" => (["value" => ([2, 1] : Array<Dynamic>)] : Map<String, Dynamic>),
            "array_length_changed" => (["value" => ([1, 2] : Array<Dynamic>)] : Map<String, Dynamic>),
            "null_to_zero" => (["value" => 0] : Map<String, Dynamic>),
            "string_to_boolean" => (["value" => true] : Map<String, Dynamic>),
            "object_key_changed" => (["value" => (["b" => 1] : Map<String, Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
