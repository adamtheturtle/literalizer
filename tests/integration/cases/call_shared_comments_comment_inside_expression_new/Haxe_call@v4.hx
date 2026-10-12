class Fixture_call_shared_comments_comment_inside_expression_new_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(42) // inner
         + 1;
    }
}
