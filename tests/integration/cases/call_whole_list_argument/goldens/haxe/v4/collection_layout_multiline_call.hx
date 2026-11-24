class Fixture_call_whole_list_argument_Haxe_collection_layout_multiline_call {
    public static function main() {
        function f(a:Dynamic):Dynamic return null;
        f(([
            1,
        ] : Array<Dynamic>));
    }
}
