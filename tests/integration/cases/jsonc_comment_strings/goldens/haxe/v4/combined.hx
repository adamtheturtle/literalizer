class Fixture_jsonc_comment_strings_Haxe_combined {
    public static function main() {
        var my_data = ([
            // strings stay data
            "https://example.org/a/*b*/",  // URL annotation
            "escaped quote: \" // still data",
            "backslash: \\",  // outside the string
            "/* not a comment */",
        ] : Array<Dynamic>);
        my_data = ([
            // strings stay data
            "https://example.org/a/*b*/",  // URL annotation
            "escaped quote: \" // still data",
            "backslash: \\",  // outside the string
            "/* not a comment */",
        ] : Array<Dynamic>);
    }
}
