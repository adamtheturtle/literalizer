class Fixture_string_with_backslash_Haxe {
    public static function main() {
        final my_data = ([
            "C:\\path\\to\\file",
            "back\\\\slash",
            "hello \\\"world\\\"",
            "path\\to \"# file",
            "trailing\\",
            "both \"quotes''' here",
            "line1\\nline2\nwith newline",
        ] : Array<Dynamic>);
    }
}
