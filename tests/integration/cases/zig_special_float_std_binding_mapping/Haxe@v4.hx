class Fixture_zig_special_float_std_binding_mapping_Haxe {
    public static function main() {
        final std = ([
            "nan" => Math.NaN,
            "positive" => Math.POSITIVE_INFINITY,
            "negative" => Math.NEGATIVE_INFINITY,
        ] : Map<String, Dynamic>);
    }
}
