class Fixture_call_binding_existing_comment_next_line_declaration_variants_Haxe_declaration_style_var_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume(count:Dynamic):Dynamic return null;
        var my_data = make_widget(42);
        consume(my_data);
        my_data = make_widget(42);
        // note
        consume(my_data);
    }
}
