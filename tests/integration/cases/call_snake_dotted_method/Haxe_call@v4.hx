class Fixture_call_snake_dotted_method_Haxe_call {
    public static function main() {
        var my_app = { http_client: { fetch: function(payload:Dynamic):Dynamic return null } };
        my_app.http_client.fetch("hello");
        my_app.http_client.fetch(42);
        my_app.http_client.fetch(true);
    }
}
