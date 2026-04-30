with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AList'[AMap'[AEntry ("$ref", AStr ("myVar"))], AInt (42), AStr ("static")]]
    ];
begin
    my_data := AList'[
        AList'[AList'[AMap'[AEntry ("$ref", AStr ("myVar"))], AInt (42), AStr ("static")]]
    ];
end Main;
