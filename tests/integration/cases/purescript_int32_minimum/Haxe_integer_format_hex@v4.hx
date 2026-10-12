class Fixture_purescript_int32_minimum_Haxe_integer_format_hex {
    public static function main() {
        final my_data = ([
            "minimum" => -0x80000000,
            "neighbor" => -0x7fffffff,
            "maximum" => 0x7fffffff,
            "nested" => ([-0x80000000] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
