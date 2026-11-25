class Fixture_tuple_empty_then_populated_Haxe_type_hints_always {
    public static function main() {
        final my_data:Array<Dynamic> = ([
            ([1, ([] : Array<Dynamic>)] : Array<Dynamic>),
            ([2, ([3] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
