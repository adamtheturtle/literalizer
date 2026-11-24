class Fixture_literalize_ref_indented_comment_bindings_Haxe_ref {
    public static function main() {
                final shared = ([
                    1,
                    2,
                ] : Array<Dynamic>);
                final my_data = ([
                    // A leading comment with { braces, "quotes", and // markers
                    "first\n{ \"quoted\" // text }",
                    shared,
                ] : Array<Dynamic>);
    }
}
