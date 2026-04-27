procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            -- comment
            AEntry ("name", AStr ("Alice")),
            AEntry ("score", ANull)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            -- comment
            AEntry ("name", AStr ("Alice")),
            AEntry ("score", ANull)
        );
    end Check_Assignment;
begin
    null;
end Check;
