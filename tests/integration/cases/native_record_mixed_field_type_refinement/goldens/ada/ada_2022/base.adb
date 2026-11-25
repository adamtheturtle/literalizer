with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("first", AMap'[AEntry ("items", AList'[AInt (1), AMap'[AEntry ("value", AInt (2))]])]),
        AEntry ("second", AMap'[AEntry ("items", AList'[AInt (1), AMap'[AEntry ("value", AStr ("s"))]])])
    ];
begin
    null;
end Main;
