procedure Check is
   procedure Check_Declaration is
      my_data : A_Val := AInt (42  -- note);
   begin
      null;
   end Check_Declaration;
   procedure Check_Assignment is
   begin
      my_data := AInt (42  -- note);
   end Check_Assignment;
begin
   null;
end Check;
