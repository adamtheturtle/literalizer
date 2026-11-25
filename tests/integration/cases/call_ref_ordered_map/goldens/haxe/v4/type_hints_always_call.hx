class Fixture_call_ref_ordered_map_Haxe_type_hints_always_call {
    public static function main() {
        function process(a:Dynamic):Dynamic return null;
        final big_list:Array<Dynamic> = ([
            "x",
        ] : Array<Dynamic>);
        process((["m" => big_list] : Map<String, Dynamic>));
    }
}
