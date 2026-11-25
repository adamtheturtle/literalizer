class Fixture_toml_comments_Haxe {
    public static function main() {
        final my_data = ([
            // before
            "answer" => 42,  // inline
            "plain" => "ok",
            // trailing
        ] : Map<String, Dynamic>);
    }
}
