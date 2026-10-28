class Fixture_variant_int32_boundaries_map_Haxe {
    public static function main() {
        final my_data = ([
            "below" => -2147483649,
            "minimum" => -2147483648,
            "above" => -2147483647,
            "nested" => ([0] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
