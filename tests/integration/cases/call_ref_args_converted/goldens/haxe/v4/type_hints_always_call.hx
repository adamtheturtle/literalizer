class Fixture_call_ref_args_converted_Haxe_type_hints_always_call {
    public static function main() {
        function process(data:Dynamic, count:Dynamic):Dynamic return null;
        final myVar:Array<Dynamic> = ([
            1,
            2,
            3,
        ] : Array<Dynamic>);
        final myOther:Array<Dynamic> = ([
            4,
            5,
            6,
        ] : Array<Dynamic>);
        process(myVar, 42);
        process(myOther, 7);
    }
}
