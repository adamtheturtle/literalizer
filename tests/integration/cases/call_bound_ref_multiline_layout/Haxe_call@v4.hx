class Fixture_call_bound_ref_multiline_layout_Haxe_call {
    public static function main() {
        function f(value:Dynamic):Dynamic return null;
        final x = ([
            ([
                1,
                2,
            ] : Array<Dynamic>),
            ([
                3,
                4,
            ] : Array<Dynamic>),
        ] : Array<Dynamic>);
        f(([
            ([
                x,
            ] : Array<Dynamic>),
        ] : Array<Dynamic>));
    }
}
