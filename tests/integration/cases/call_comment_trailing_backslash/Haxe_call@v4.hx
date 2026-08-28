class Fixture_call_comment_trailing_backslash_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process(1);  // trail \ .
        process(2);  // second
    }
}
