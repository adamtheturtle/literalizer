class Fixture_long_string_before_list_comma_Haxe {
    public static function main() {
        final my_data = ([
            "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
            1,
        ] : Array<Dynamic>);
    }
}
