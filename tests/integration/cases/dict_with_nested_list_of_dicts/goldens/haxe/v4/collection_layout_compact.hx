class Fixture_dict_with_nested_list_of_dicts_Haxe_collection_layout_compact {
    public static function main() {
        final my_data = ([
            "a" => ([([(["b" => 1] : Map<String, Dynamic>)] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
