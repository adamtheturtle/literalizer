class Fixture_call_shared_comments_csharp_escaped_braces_plain_new_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = ($"{{payload}} {1://}").Length >= 0 ? make_widget(42) : make_widget(42);
    }
}
