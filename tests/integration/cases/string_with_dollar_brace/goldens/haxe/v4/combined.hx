class Fixture_string_with_dollar_brace_Haxe_combined {
    public static function main() {
        var my_data = ([
            "prefix ${HOME} suffix",
            "${interpolated}",
        ] : Array<Dynamic>);
        my_data = ([
            "prefix ${HOME} suffix",
            "${interpolated}",
        ] : Array<Dynamic>);
    }
}
