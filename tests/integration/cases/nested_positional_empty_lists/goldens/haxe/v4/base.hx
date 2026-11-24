class Fixture_nested_positional_empty_lists_Haxe {
    public static function main() {
        final my_data = ([
            ([
                ([] : Array<Dynamic>),
            ] : Array<Dynamic>),
            ([
                ([
                    1,
                ] : Array<Dynamic>),
            ] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
