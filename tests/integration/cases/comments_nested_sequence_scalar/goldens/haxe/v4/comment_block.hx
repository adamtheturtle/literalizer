class Fixture_comments_nested_sequence_scalar_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            (["ADD", "alice", "hello"] : Array<Dynamic>),
            ([
                "DEL",
                "bob",
                "5",  /* removes "world" */
            ] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
