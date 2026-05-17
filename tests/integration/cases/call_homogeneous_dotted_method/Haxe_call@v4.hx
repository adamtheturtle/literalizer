class Fixture_call_homogeneous_dotted_method_Haxe_call {
    public static function main() {
        var app = { client: { fetch: function(value:Dynamic):Dynamic return null } };
        app.client.fetch("hello");
        app.client.fetch("world");
    }
}
