class Fixture_comments_nested_sequence_scalar_Haxe_combined {
    public static function main() {
        var my_data = ([
            (["ADD", "alice", "hello"] : Array<Dynamic>),
            ([
                "DEL",
                "bob",
                "5",  // removes "world"
            ] : Array<Dynamic>),
        ] : Array<Dynamic>);
        my_data = ([
            (["ADD", "alice", "hello"] : Array<Dynamic>),
            ([
                "DEL",
                "bob",
                "5",  // removes "world"
            ] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
