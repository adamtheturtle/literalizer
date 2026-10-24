class Fixture_nested_sibling_map_matching_values_Haxe {
    public static function main() {
        final my_data = ([
            "first" => (["items" => ([1, (["value" => 2] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
            "second" => (["items" => ([1, (["value" => 3] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
