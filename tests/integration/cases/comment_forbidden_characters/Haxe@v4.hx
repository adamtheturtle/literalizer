class Fixture_comment_forbidden_characters_Haxe {
    public static function main() {
        final my_data = ([
            "a" => 1,  // tab	here and bidi <U+202E>after
            "b" => 2,
        ] : Map<String, Dynamic>);
    }
}
