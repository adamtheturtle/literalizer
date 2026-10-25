class Fixture_yaml_partially_outdented_comment_Haxe_combined {
    public static function main() {
        var my_data = ([
            "a" => ([
                "b" => ([1] : Array<Dynamic>),
                // Outdented from the sequence, so the inner mapping claims this.
                "c" => 2,
            ] : Map<String, Dynamic>),
            // Outdented from the inner mapping too, so the root claims this.
            "d" => 3,
        ] : Map<String, Dynamic>);
        my_data = ([
            "a" => ([
                "b" => ([1] : Array<Dynamic>),
                // Outdented from the sequence, so the inner mapping claims this.
                "c" => 2,
            ] : Map<String, Dynamic>),
            // Outdented from the inner mapping too, so the root claims this.
            "d" => 3,
        ] : Map<String, Dynamic>);
    }
}
