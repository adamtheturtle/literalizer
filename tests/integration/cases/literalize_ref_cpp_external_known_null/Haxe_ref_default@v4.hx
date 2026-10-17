class Fixture_literalize_ref_cpp_external_known_null_Haxe_ref_default {
    public static function main() {
        function consume_widget(_arg:Dynamic):Dynamic return null;
        final item = null;
        final my_data = null;
        consume_widget(my_data);
        my_data = item;
        consume_widget(my_data);
    }
}
