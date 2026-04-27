procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AMap'(AEntry ("name", AStr ("Alice")), AEntry ("age", AInt (30))),
            AMap'(AEntry ("name", AStr ("Bob")), AEntry ("age", AInt (25)))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AMap'(AEntry ("name", AStr ("Alice")), AEntry ("age", AInt (30))),
            AMap'(AEntry ("name", AStr ("Bob")), AEntry ("age", AInt (25)))
        );
    end Check_Assignment;
begin
    null;
end Check;
