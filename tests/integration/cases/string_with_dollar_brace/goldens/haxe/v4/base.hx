class Fixture_string_with_dollar_brace_Haxe {
    public static function main() {
        final my_data = ([
            "prefix ${HOME} suffix",
            "${interpolated}",
        ] : Array<Dynamic>);
    }
}
