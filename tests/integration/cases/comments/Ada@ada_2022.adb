with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- Server configuration
        AEntry ("host", AStr ("localhost")),  -- default host
        AEntry ("port", AInt (8080)),
        -- Enable debug mode
        AEntry ("debug", ABool (True))
    ];
begin
    null;
end Main;
