class Fixture_call_comments_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        // Test cases
        process("hello");  // single word
        process("hello world");  // two words
        // trailing comment
    }
}
