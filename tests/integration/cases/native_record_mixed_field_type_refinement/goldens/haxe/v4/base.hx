class Fixture_native_record_mixed_field_type_refinement_Haxe {
    public static function main() {
        final my_data = ([
            "first" => (["items" => ([1, (["value" => 2] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
            "second" => (["items" => ([1, (["value" => "s"] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
