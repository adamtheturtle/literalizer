class Fixture_int32_minimum_with_nested_list_Haxe {
    public static function main() {
        final my_data = ([
            "minimum" => -2147483648,
            "neighbor" => -2147483647,
            "maximum" => 2147483647,
            "nested" => ([-2147483648] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
