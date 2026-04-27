procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("a", ANull),
            AEntry ("b", ANull)
            -- trailing
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("a", ANull),
            AEntry ("b", ANull)
            -- trailing
        );
    end Check_Assignment;
begin
    null;
end Check;
