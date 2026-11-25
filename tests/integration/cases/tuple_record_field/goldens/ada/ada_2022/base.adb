with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("call", AStr ("send")),
        AEntry ("args", AList'[AInt (1), AStr ("email"), AStr ("a@gmail.com"), AInt (100)])
    ];
begin
    null;
end Main;
