with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        -- Server configuration
        AEntry ("host", AStr ("localhost")),  -- default host
        AEntry ("port", AInt (8080)),
        -- Enable debug mode
        AEntry ("debug", ABool (True))
    ];
begin
    my_data := AMap'[
        -- Server configuration
        AEntry ("host", AStr ("localhost")),  -- default host
        AEntry ("port", AInt (8080)),
        -- Enable debug mode
        AEntry ("debug", ABool (True))
    ];
end Check;
