class Fixture_tuple_nested_scope_Haxe {
    public static function main() {
        final my_data = ([
            "x" => ([1, ([2, ([3] : Array<Dynamic>)] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
