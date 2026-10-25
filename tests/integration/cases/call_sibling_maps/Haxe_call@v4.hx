class Fixture_call_sibling_maps_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process((["value" => 1] : Map<String, Dynamic>));
        process((["value" => "hello"] : Map<String, Dynamic>));
    }
}
