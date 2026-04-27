procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("a", AInt (1)),
            AEntry ("b", AFloat (2.5)),
            AEntry ("c", AInt (3))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("a", AInt (1)),
            AEntry ("b", AFloat (2.5)),
            AEntry ("c", AInt (3))
        );
    end Check_Assignment;
begin
    null;
end Check;
