class Fixture_call_nullable_object_conditional_existing_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume(count:Dynamic):Dynamic return null;
        var my_data = make_widget(7);
        consume(my_data);
        my_data = make_widget(13) != null ?
        make_widget(13) // inner
        : null; // trailing
        consume(my_data);
    }
}
