class Fixture_call_ref_nested_in_collection_Haxe_call {
    public static function main() {
        function process(a:Dynamic, b:Dynamic):Dynamic return null;
        final big_list = ([
            "x",
        ] : Array<Dynamic>);
        process((["k" => big_list] : Map<String, Dynamic>), (["m" => big_list] : Map<String, Dynamic>));
    }
}
