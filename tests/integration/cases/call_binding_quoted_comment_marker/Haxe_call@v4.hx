class Fixture_call_binding_quoted_comment_marker_Haxe_call {
    public static function main() {
        function make_widget(text:Dynamic):Dynamic return null;
        final my_data = make_widget("first \"quote\"\n// string body"); // note
        // extra
    }
}
