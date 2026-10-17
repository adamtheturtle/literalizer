with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AFloat (5.0e-324),
        AFloat (-5.0e-324),
        AFloat (1.0e-310)
    ];
begin
    null;
end Main;
