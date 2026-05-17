class Fixture_dict_with_list_value_Haxe_type_hints_always {
    public static function main() {
        final my_data:Map<String, Dynamic> = ([
            "name" => "Alice",
            "scores" => ([10, 20, 30] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
