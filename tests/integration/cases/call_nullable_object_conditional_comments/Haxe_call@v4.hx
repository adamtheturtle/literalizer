class Fixture_call_nullable_object_conditional_comments_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(42) != null ?
        make_widget(42) // inner
        : null; // trailing
    }
}
