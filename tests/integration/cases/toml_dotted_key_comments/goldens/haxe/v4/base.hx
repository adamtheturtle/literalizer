class Fixture_toml_dotted_key_comments_Haxe {
    public static function main() {
        final my_data = ([
            // first dotted key
            // second dotted key
            "a" => (["b" => 1, "c" => 2] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
