with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("value", AList'[ABool (True), ABool (False), AInt (0), AInt (1)])
    ];
begin
    null;
end Main;
