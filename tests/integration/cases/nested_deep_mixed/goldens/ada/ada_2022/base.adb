with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AList'[AInt (1), AInt (2)], AList'[AStr ("a"), AStr ("b")]]
    ];
begin
    null;
end Main;
