class Fixture_tuple_empty_then_populated_Haxe {
    public static function main() {
        final my_data = ([
            ([1, ([] : Array<Dynamic>)] : Array<Dynamic>),
            ([2, ([3] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
