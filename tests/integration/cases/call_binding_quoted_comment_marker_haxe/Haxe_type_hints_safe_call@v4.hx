class Fixture_call_binding_quoted_comment_marker_haxe_Haxe_type_hints_safe_call {
    public static function main() {
        function make_widget(text:Dynamic):Dynamic return null;
        final my_data = make_widget("first \"quote\"\n// string body"); // note
        // extra
    }
}
