procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("a", AMap'(AEntry ("x", AInt (1)))),
            AEntry ("b", AInt (2))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("a", AMap'(AEntry ("x", AInt (1)))),
            AEntry ("b", AInt (2))
        );
    end Check_Assignment;
begin
    null;
end Check;
