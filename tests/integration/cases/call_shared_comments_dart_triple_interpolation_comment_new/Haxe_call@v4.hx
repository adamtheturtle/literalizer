class Fixture_call_shared_comments_dart_triple_interpolation_comment_new_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = ('''prefix ${'// payload'}''').length >= 0 ? make_widget(42) : make_widget(42); // trailing
        // extra
    }
}
