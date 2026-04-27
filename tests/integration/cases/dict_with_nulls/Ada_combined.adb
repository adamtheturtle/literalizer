procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("score", ANull),
            AEntry ("age", AInt (30))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("score", ANull),
            AEntry ("age", AInt (30))
        );
    end Check_Assignment;
begin
    null;
end Check;
