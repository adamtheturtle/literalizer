class Fixture_scalar_and_populated_map_sequence_Haxe {
    public static function main() {
        final my_data = ([
            1,
            (["a" => 2] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
