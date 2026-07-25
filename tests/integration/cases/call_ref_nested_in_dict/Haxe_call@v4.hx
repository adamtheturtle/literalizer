class Fixture_call_ref_nested_in_dict_Haxe_call {
    public static function main() {
        function process(data:Dynamic):Dynamic return null;
        final my_var = 42;
        process((["key" => my_var, "count" => 42, "label" => "example"] : Map<String, Dynamic>));
    }
}
