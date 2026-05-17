class Fixture_call_deep_dotted_method_Haxe_call {
    public static function main() {
        var obj = { api: { client: { post: function(data:Dynamic):Dynamic return null } } };
        obj.api.client.post("hello");
        obj.api.client.post(42);
        obj.api.client.post(true);
    }
}
