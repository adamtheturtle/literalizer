class Fixture_call_whole_input_comment_Haxe_call {
    public static function main() {
        function f(a:Dynamic):Dynamic return null;
        f(([1] : Array<Dynamic>));  // note
    }
}
