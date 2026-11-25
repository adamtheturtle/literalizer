with A_Stub; use A_Stub;
procedure Main is
    floating_value : A_Val := AFloat (1.5);
    integer_value : A_Val := AFloat (2.0);
    my_data : A_Val := AList'[
        floating_value,
        integer_value
    ];
begin
    null;
end Main;
