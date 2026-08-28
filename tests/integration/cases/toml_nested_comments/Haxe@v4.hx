class Fixture_toml_nested_comments_Haxe {
    public static function main() {
        final my_data = ([
            // About the first dotted key.
            // About the second dotted key.
            "dotted" => (["first" => 1, "second" => 2] : Map<String, Dynamic>),
            "plain" => 3,  // About the plain key.
            // Before the first entry.
            // Before the second entry.
            "entries" => ([(["name" => "one"] : Map<String, Dynamic>), (["name" => "two"] : Map<String, Dynamic>)] : Array<Dynamic>),
            // Inside the table.
            "table" => (["inner" => 4] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
