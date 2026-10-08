class Fixture_scala_nested_map_sequence_type_Haxe {
    public static function main() {
        final my_data = ([
            "a" => (["b" => ([1, 2, 3] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
