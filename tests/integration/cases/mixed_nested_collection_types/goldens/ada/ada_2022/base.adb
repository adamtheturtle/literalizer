with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("lists", AList'[AList'[AInt (1)], AList'[AStr ("x")], AList'[]]),
        AEntry ("maps", AList'[AMap'[AEntry ("x", AInt (1))], AMap'[AEntry ("x", AStr ("s"))]]),
        AEntry ("empties", AMap'[AEntry ("a", AList'[AInt (1)]), AEntry ("b", AList'[])])
    ];
begin
    null;
end Main;
