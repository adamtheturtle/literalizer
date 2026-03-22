procedure Check is
   X : A_Val := ASet'(
       AStr ("apple"),  -- inline comment
       -- before banana
       AStr ("banana")
       -- trailing
   );
begin
   null;
end Check;
