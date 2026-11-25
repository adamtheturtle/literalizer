class Fixture_nested_sequence_Haxe_type_hints_always {
    public static function main() {
        final my_data:Array<Dynamic> = ([
            true,
            "hi",
            ([1, 2] : Array<Dynamic>),
            null,
        ] : Array<Dynamic>);
    }
}
