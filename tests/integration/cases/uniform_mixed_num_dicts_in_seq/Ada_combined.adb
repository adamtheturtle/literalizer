procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AMap'(AEntry ("x", AInt (1)), AEntry ("y", AFloat (2.5))),
            AMap'(AEntry ("x", AInt (3)), AEntry ("y", AFloat (4.0)))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AMap'(AEntry ("x", AInt (1)), AEntry ("y", AFloat (2.5))),
            AMap'(AEntry ("x", AInt (3)), AEntry ("y", AFloat (4.0)))
        );
    end Check_Assignment;
begin
    null;
end Check;
