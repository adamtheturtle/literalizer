with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AMap'[AEntry ("$ref", AStr ("repeated_var"))], AInt (1)],
        AList'[AMap'[AEntry ("$ref", AStr ("single_var"))], AInt (0)],
        AList'[AMap'[AEntry ("$ref", AStr ("repeated_var"))], AInt (8)]
    ];
begin
    my_data := AList'[
        AList'[AMap'[AEntry ("$ref", AStr ("repeated_var"))], AInt (1)],
        AList'[AMap'[AEntry ("$ref", AStr ("single_var"))], AInt (0)],
        AList'[AMap'[AEntry ("$ref", AStr ("repeated_var"))], AInt (8)]
    ];
end Main;
