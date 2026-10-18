with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- comment ending backslash \ .
        AEntry ("x", AInt (1))
    ];
begin
    null;
end Main;
