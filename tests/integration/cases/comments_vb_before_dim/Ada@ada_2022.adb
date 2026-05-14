with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- Configuration
        AEntry ("name", AStr ("app")),
        -- Port setting
        AEntry ("port", AInt (3000))
    ];
begin
    null;
end Main;
