class Fixture_cpp_variant_int32_boundaries_map_Haxe_integer_format_hex {
    public static function main() {
        final my_data = ([
            "below" => -2147483649,
            "minimum" => -0x80000000,
            "above" => -0x7fffffff,
            "nested" => ([0x0] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
