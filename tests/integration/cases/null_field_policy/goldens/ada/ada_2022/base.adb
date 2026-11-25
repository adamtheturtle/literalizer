with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("drop", ANull),
        AEntry ("keep", AInt (1))
    ];
begin
    null;
end Main;
