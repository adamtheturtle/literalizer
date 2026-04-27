procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("outer", AMap'(AEntry ("a", AInt (1)), AEntry ("b", AStr ("x")), AEntry ("c", ANull)))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("outer", AMap'(AEntry ("a", AInt (1)), AEntry ("b", AStr ("x")), AEntry ("c", ANull)))
        );
    end Check_Assignment;
begin
    null;
end Check;
