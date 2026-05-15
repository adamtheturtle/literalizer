with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("call", AStr ("send")), AEntry ("args", AList'[AInt (1), AStr ("email"), AStr ("a@gmail.com"), AInt (100)])],
        AMap'[AEntry ("call", AStr ("recv")), AEntry ("args", AList'[AInt (2), AStr ("sms"), AStr ("b@example.com"), AInt (200)])]
    ];
begin
    null;
end Main;
