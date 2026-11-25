class Fixture_dict_mixed_int_widths_Haxe {
    public static function main() {
        final my_data = ([
            "a" => 1,
            "b" => 3000000000,
            "c" => "x",
        ] : Map<String, Dynamic>);
    }
}
