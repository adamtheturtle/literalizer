with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AList'[AInt (1), AStr ("value")], AList'[]],
        AList'[AList'[], AList'[AInt (2), AStr ("other")]]
    ];
begin
    null;
end Main;
