class Fixture_call_ref_nested_in_list_Haxe_call {
    public static function main() {
        function process(data:Dynamic):Dynamic return null;
        final my_var = 42;
        final my_other = 7;
        process(([my_var, 42, "static"] : Array<Dynamic>));
        process(([my_other, 7, "label"] : Array<Dynamic>));
    }
}
