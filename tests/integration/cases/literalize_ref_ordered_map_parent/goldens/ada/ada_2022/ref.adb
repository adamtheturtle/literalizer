with A_Stub; use A_Stub;
procedure Main is
    bound : A_Val := AInt (2);
    my_data : A_Val := AMap'[
        AEntry ("value", bound)
    ];
begin
    null;
end Main;
