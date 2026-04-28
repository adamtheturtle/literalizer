with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("host", AStr ("localhost")),
        AEntry ("port", ANull),  -- not configured yet
        AEntry ("debug", ABool (True))
    ];
begin
    my_data := AMap'[
        AEntry ("host", AStr ("localhost")),
        AEntry ("port", ANull),  -- not configured yet
        AEntry ("debug", ABool (True))
    ];
end Main;
