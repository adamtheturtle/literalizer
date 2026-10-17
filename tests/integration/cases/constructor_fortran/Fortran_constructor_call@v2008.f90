module constructor_types
  implicit none
  type fval_t
    integer :: value = 42
  end type
contains
  function Playlist() result(value)
    type(fval_t) :: value
  end function
end module

program constructor_binding
  use constructor_types
  implicit none
type(fval_t) :: p
p = Playlist()
if (p%value /= 42) stop 1
end program
