with A_Stub; use A_Stub;
procedure Main is
    existing : A_Val := AInt (1);
    my_data : A_Val := AMap'[
        AEntry ("nested", AList'[AInt (0), existing])
    ];
begin
    null;
end Main;
