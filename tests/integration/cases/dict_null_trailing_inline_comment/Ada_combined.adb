procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("host", AStr ("localhost")),
            AEntry ("port", ANull)  -- not configured yet
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("host", AStr ("localhost")),
            AEntry ("port", ANull)  -- not configured yet
        );
    end Check_Assignment;
begin
    null;
end Check;
