class Fixture_literalize_ref_zig_mutable_prefixed_comments_Haxe_ref {
    public static function main() {
                var shared = ([
                    1,
                    2,
                ] : Array<Dynamic>);
                var my_data = ([
                    // A leading comment with { braces, "quotes", and // markers
                    "first\n{ \"quoted\" // text }",
                    shared,
                ] : Array<Dynamic>);
    }
}
