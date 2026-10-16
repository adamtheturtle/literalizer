class Fixture_call_nim_dotted_mixed_empty_arguments_Haxe_call {
    public static function main() {
        var thing = { go: function(before:Dynamic, populated:Dynamic, after:Dynamic):Dynamic return null };
        thing.go(([] : Array<Dynamic>), ([1] : Array<Dynamic>), ([] : Array<Dynamic>));
        thing.go((["text"] : Array<Dynamic>), ([2] : Array<Dynamic>), ([] : Array<Dynamic>));
        thing.go(([] : Array<Dynamic>), (["text"] : Array<Dynamic>), ([] : Array<Dynamic>));
        thing.go((["text"] : Array<Dynamic>), ([2] : Array<Dynamic>), ([3] : Array<Dynamic>));
    }
}
