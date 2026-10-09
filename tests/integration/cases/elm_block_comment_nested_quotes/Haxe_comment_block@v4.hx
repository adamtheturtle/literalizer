class Fixture_elm_block_comment_nested_quotes_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            /* "{-" and '{-' stay readable */
            /* balanced {- nested -} and trailing -} stay readable */
            "x" => 1,
        ] : Map<String, Dynamic>);
    }
}
