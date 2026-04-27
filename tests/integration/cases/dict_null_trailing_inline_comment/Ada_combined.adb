with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("host", AStr ("localhost")),
        AEntry ("port", ANull)  -- not configured yet
    ];
begin
    my_data := AMap'[
        AEntry ("host", AStr ("localhost")),
        AEntry ("port", ANull)  -- not configured yet
    ];
end Check;
