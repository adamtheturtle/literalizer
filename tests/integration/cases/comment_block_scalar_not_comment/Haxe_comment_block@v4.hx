class Fixture_comment_block_scalar_not_comment_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            "description" => "# not a comment\n",
            "name" => "foo",
        ] : Map<String, Dynamic>);
    }
}
