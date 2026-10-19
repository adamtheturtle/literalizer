class Fixture_comment_nested_openers_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            /* nested openers / * and {- remain */
            "x" => 1,
        ] : Map<String, Dynamic>);
    }
}
