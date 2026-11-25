class Fixture_call_ref_args_reused_Haxe_call {
    public static function main() {
        function process(data:Dynamic, count:Dynamic):Dynamic return null;
        final single_var = ([
            4,
            5,
            6,
        ] : Array<Dynamic>);
        final repeated_var = 1;
        process(repeated_var, 1);
        process(single_var, 0);
        process(repeated_var, 8);
    }
}
