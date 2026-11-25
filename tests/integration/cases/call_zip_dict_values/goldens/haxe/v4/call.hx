class Fixture_call_zip_dict_values_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        function emit(_call:Dynamic, _zip:Dynamic):Dynamic return null;
        emit(process("hello"), (["a" => 1, "b" => 2] : Map<String, Dynamic>));
        emit(process(42), (["c" => 3, "d" => 4] : Map<String, Dynamic>));
    }
}
