class Fixture_tuple_record_sequence_Haxe {
    public static function main() {
        final my_data = ([
            (["call" => "send", "args" => ([1, "email", "a@gmail.com", 100] : Array<Dynamic>)] : Map<String, Dynamic>),
            (["call" => "recv", "args" => ([2, "sms", "b@example.com", 200] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
