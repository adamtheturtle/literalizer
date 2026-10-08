class Fixture_call_bound_ref_multiline_layout_Haxe_call {
    public static function main() {
        function f(value:Dynamic):Dynamic return null;
        final ref_data = ([
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
                ref_data,
            ] : Array<Dynamic>),
        ] : Array<Dynamic>));
    }
}
