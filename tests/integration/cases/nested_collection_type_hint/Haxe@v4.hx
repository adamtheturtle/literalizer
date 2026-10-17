class Fixture_nested_collection_type_hint_Haxe {
    public static function main() {
        final my_data = ([
            "a" => ([(["b" => 1] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
