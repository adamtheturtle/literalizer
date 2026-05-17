class Fixture_record_epoch_datetime_i32_overflow_Haxe {
    public static function main() {
        final my_data = ([
            "within_i32" => "2024-01-15T12:00:00",
            "beyond_i32" => "2099-06-15T08:30:00",
        ] : Map<String, Dynamic>);
    }
}
