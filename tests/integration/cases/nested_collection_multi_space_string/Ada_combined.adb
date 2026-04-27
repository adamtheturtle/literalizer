procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AMap'(AEntry ("key", AStr ("hello   world")), AEntry ("value", AInt (1)))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AMap'(AEntry ("key", AStr ("hello   world")), AEntry ("value", AInt (1)))
        );
    end Check_Assignment;
begin
    null;
end Check;
