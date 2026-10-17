class Fixture_call_carrier_member_separate_Haxe_call {
    public static function main() {
        var app = { go: function(first_value:Dynamic, second_value:Dynamic):Dynamic return null };
        app.go(([1] : Array<Dynamic>), (["text"] : Array<Dynamic>));
    }
}
