class Fixture_call_sv_macro_binding_comment_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = (`__LINE__ > 0) ? make_widget(42) : make_widget(42); // trailing `marker
    }
}
