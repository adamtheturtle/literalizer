class Fixture_call_ref_in_ordered_map_Haxe_call {
    public static function main() {
        function process(a:Dynamic):Dynamic return null;
        final big_list = ([
            "x",
        ] : Array<Dynamic>);
        process((["m" => big_list] : Map<String, Dynamic>));
    }
}
