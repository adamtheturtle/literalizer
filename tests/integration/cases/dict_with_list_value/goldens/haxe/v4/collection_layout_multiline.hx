class Fixture_dict_with_list_value_Haxe_collection_layout_multiline {
    public static function main() {
        final my_data = ([
            "name" => "Alice",
            "scores" => ([
                10,
                20,
                30,
            ] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
