procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            -- Server configuration
            AEntry ("host", AStr ("localhost")),  -- default host
            AEntry ("port", AInt (8080)),
            -- Enable debug mode
            AEntry ("debug", ABool (True))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            -- Server configuration
            AEntry ("host", AStr ("localhost")),  -- default host
            AEntry ("port", AInt (8080)),
            -- Enable debug mode
            AEntry ("debug", ABool (True))
        );
    end Check_Assignment;
begin
    null;
end Check;
