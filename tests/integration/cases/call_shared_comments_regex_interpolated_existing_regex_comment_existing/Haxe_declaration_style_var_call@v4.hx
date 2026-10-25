class Fixture_call_shared_comments_regex_interpolated_existing_regex_comment_existing_Haxe_declaration_style_var_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        var my_data = make_widget(42);
        my_data = (~/\//).match("/") ? make_widget(42) : null; // trailing
    }
}
