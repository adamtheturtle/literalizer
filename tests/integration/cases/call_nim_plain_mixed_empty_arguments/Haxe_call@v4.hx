class Fixture_call_nim_plain_mixed_empty_arguments_Haxe_call {
    public static function main() {
        function make_widget(before:Dynamic, populated:Dynamic, after:Dynamic):Dynamic return null;
        make_widget(([] : Array<Dynamic>), ([1] : Array<Dynamic>), ([] : Array<Dynamic>));
        make_widget((["text"] : Array<Dynamic>), ([2] : Array<Dynamic>), ([] : Array<Dynamic>));
        make_widget(([] : Array<Dynamic>), (["text"] : Array<Dynamic>), ([] : Array<Dynamic>));
        make_widget((["text"] : Array<Dynamic>), ([2] : Array<Dynamic>), ([3] : Array<Dynamic>));
    }
}
