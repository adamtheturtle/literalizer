class Fixture_call_dotted_receiver_parameter_collisions_Haxe_call {
    public static function main() {
        var api = { worker: { process: function(self:Dynamic, self_:Dynamic):Dynamic return null } };
        api.worker.process(([] : Map<String, Dynamic>), ([] : Map<String, Dynamic>));
    }
}
