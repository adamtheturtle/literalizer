class Fixture_comment_block_scalar_not_comment_Haxe {
    public static function main() {
        final my_data = ([
            "description" => "# not a comment\n",
            "name" => "foo",
        ] : Map<String, Dynamic>);
    }
}
