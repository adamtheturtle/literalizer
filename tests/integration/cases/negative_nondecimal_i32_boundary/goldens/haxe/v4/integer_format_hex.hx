class Fixture_negative_nondecimal_i32_boundary_Haxe_integer_format_hex {
    public static function main() {
        final my_data = ([
            "minimum" => -0x80000000,
            "below" => -3000000000,
        ] : Map<String, Dynamic>);
    }
}
