procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("a", AInt (1)),
            AEntry ("b", AInt (3000000000)),
            AEntry ("c", AStr ("x"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("a", AInt (1)),
            AEntry ("b", AInt (3000000000)),
            AEntry ("c", AStr ("x"))
        );
    end Check_Assignment;
begin
    null;
end Check;
