class Fixture_call_nested_inline_between_comments_Haxe_call {
    public static function main() {
        function f(a:Dynamic, b:Dynamic):Dynamic return null;
        f(2, "hello");  // trailing note
        // next element
        f(3, "world");
    }
}
