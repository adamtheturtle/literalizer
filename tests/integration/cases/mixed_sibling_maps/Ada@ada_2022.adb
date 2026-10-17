with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AMap'[AEntry ("a", AInt (1))], AMap'[AEntry ("a", ANull)], AInt (42)],
        AList'[AMap'[AEntry ("a", AInt (1))], AMap'[AEntry ("a", AStr ("s"))], AInt (42)],
        AList'[AMap'[AEntry ("a", AInt (1))], AMap'[AEntry ("a", ANull)]],
        AList'[AMap'[AEntry ("a", AInt (1))], AMap'[AEntry ("a", AStr ("s"))]]
    ];
begin
    null;
end Main;
