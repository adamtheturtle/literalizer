class Fixture_yaml_nested_sequence_between_comments_Haxe {
    public static function main() {
        final my_data = ([
            ([
                (["item" => "existing"] : Map<String, Dynamic>),
                "kept",
                // This comment trails the first pair.
            ] : Array<Dynamic>),
            ([(["item" => "next"] : Map<String, Dynamic>), "also kept"] : Array<Dynamic>),
            // This comment describes the last pair.
            ([(["item" => "last"] : Map<String, Dynamic>), "kept too"] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
