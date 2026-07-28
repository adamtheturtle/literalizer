class Fixture_call_unknown_ref_nested_dict_Haxe_call {
    public static function main() {
        function process(data:Dynamic):Dynamic return null;
        final my_list = ([] : Array<Dynamic>);
        process(([([(["inner" => my_list] : Map<String, Dynamic>)] : Array<Dynamic>)] : Array<Dynamic>));
    }
}
