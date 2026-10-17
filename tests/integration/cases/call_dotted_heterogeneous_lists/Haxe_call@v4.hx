class Fixture_call_dotted_heterogeneous_lists_Haxe_call {
    public static function main() {
        var app = { client: { go: function(first_value:Dynamic, second_value:Dynamic):Dynamic return null } };
        app.client.go(([1] : Array<Dynamic>), (["text"] : Array<Dynamic>));
    }
}
