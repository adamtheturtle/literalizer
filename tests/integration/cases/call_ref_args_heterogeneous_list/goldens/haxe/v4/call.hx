class Fixture_call_ref_args_heterogeneous_list_Haxe_call {
    public static function main() {
        function process(data:Dynamic, count:Dynamic):Dynamic return null;
        final my_ints = ([
            1,
            2,
            3,
        ] : Array<Dynamic>);
        final my_strings = ([
            "a",
            "b",
        ] : Array<Dynamic>);
        final my_empty = ([] : Array<Dynamic>);
        process(my_ints, 42);
        process(my_strings, 7);
        process(my_empty, 99);
    }
}
