procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("age", AInt (30)),
            AEntry ("active", ABool (True))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("age", AInt (30)),
            AEntry ("active", ABool (True))
        );
    end Check_Assignment;
begin
    null;
end Check;
