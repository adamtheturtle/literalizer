class Fixture_scalar_empty_and_populated_maps_Haxe {
    public static function main() {
        final my_data = ([
            1,
            ([] : Map<String, Dynamic>),
            (["x" => 2] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
