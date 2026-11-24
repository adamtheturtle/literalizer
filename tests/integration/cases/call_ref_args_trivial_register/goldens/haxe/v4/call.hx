class Fixture_call_ref_args_trivial_register_Haxe_call {
    public static function main() {
        function process(value:Dynamic, count:Dynamic):Dynamic return null;
        final my_int = 1;
        final my_bool = true;
        final my_float = 3.14;
        final my_list = ([
            1,
            2,
            3,
        ] : Array<Dynamic>);
        process(my_int, 42);
        process(my_bool, 7);
        process(my_float, 9);
        process(my_list, 1);
    }
}
