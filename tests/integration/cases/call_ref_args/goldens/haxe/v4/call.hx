class Fixture_call_ref_args_Haxe_call {
    public static function main() {
        function process(data:Dynamic, count:Dynamic):Dynamic return null;
        final my_var = ([
            1,
            2,
            3,
        ] : Array<Dynamic>);
        final my_other = ([
            4,
            5,
            6,
        ] : Array<Dynamic>);
        process(my_var, 42);
        process(my_other, 7);
    }
}
