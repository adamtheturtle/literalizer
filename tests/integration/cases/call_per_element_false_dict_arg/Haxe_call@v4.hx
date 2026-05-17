class Fixture_call_per_element_false_dict_arg_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process((["a" => 1, "b" => "x"] : Map<String, Dynamic>));
    }
}
