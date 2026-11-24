with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- server
        AEntry ("host", AStr ("localhost"))  -- default
    ];
begin
    null;
end Main;
