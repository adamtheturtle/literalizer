class Fixture_nested_map_list_integer_widening_Haxe {
    public static function main() {
        final my_data = ([
            "a" => ([1] : Array<Dynamic>),
            "b" => ([1099511627776] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
