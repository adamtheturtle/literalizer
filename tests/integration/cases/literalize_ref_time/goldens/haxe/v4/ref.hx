class Fixture_literalize_ref_time_Haxe_ref {
    public static function main() {
        final myTime = "01:02:03";
        final my_data = ([
            "x" => myTime,
        ] : Map<String, Dynamic>);
    }
}
