class Fixture_call_unicode_line_separator_comments_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process(1);  // note<U+2028>still commented<U+2029>done
    }
}
