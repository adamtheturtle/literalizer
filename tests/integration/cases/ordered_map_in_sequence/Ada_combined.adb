procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AMap'(AEntry ("a", AInt (1))),
            AStr ("hello")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AMap'(AEntry ("a", AInt (1))),
            AStr ("hello")
        );
    end Check_Assignment;
begin
    null;
end Check;
