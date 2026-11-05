class Fixture_call_nullable_conditional_collection_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(([1, 2] : Array<Dynamic>)) != null ?
        make_widget(([1, 2] : Array<Dynamic>)) // inner
        : null; // trailing
    }
}
