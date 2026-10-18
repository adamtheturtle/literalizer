class Fixture_call_elm_bound_multiline_multiple_Haxe_call {
    public static function main() {
        function f(value:Dynamic):Dynamic return null;
        final ref_data = ([
            1,
            2,
        ] : Array<Dynamic>);
        f(([
            ref_data,
        ] : Array<Dynamic>));
        f(([
            ref_data,
        ] : Array<Dynamic>));
    }
}
