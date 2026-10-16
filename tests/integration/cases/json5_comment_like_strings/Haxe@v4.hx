class Fixture_json5_comment_like_strings_Haxe {
    public static function main() {
        final my_data = ([
            "// data",
            "/* data */",
            "escaped quote: \" // data",
            "backslash: \\",
        ] : Array<Dynamic>);
    }
}
