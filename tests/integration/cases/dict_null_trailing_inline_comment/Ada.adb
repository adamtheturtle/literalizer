with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("host", AStr ("localhost")),
        AEntry ("port", ANull)  -- not configured yet
    ];
begin
    null;
end Main;
