module fval_m
  implicit none
  integer, parameter :: int64 = selected_int_kind(18)
  integer, parameter :: real64 = selected_real_kind(15, 307)
  type :: fval_t
    integer :: t = 0
  end type fval_t
contains
  function fnull() result(v); type(fval_t) :: v; end function
  function fbool(b) result(v); logical, intent(in) :: b; type(fval_t) :: v; end function
  function fint(n) result(v); integer(kind=int64), intent(in) :: n; type(fval_t) :: v; end function
  function freal(x) result(v); real(kind=real64), intent(in) :: x; type(fval_t) :: v; end function
  function fstr(s) result(v); character(len=*), intent(in) :: s; type(fval_t) :: v; end function
  function flist(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fmap(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fset(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fentry(k, u) result(v); character(len=*), intent(in) :: k; type(fval_t), intent(in) :: u; type(fval_t) :: v; end function
end module fval_m
subroutine main_declaration()
    use fval_m
    implicit none
    type(fval_t) :: my_data
    my_data = fmap([fval_t :: &
        fentry('assert', fint(1_int64)), &
        fentry('else', fint(1_int64)), &
        fentry('error', fint(1_int64)), &
        fentry('false', fint(1_int64)), &
        fentry('for', fint(1_int64)), &
        fentry('function', fint(1_int64)), &
        fentry('if', fint(1_int64)), &
        fentry('import', fint(1_int64)), &
        fentry('importbin', fint(1_int64)), &
        fentry('importstr', fint(1_int64)), &
        fentry('in', fint(1_int64)), &
        fentry('local', fint(1_int64)), &
        fentry('null', fint(1_int64)), &
        fentry('self', fint(1_int64)), &
        fentry('super', fint(1_int64)), &
        fentry('tailstrict', fint(1_int64)), &
        fentry('then', fint(1_int64)), &
        fentry('true', fint(1_int64)), &
        fentry('ordinary', fint(1_int64)) &
    ])
end subroutine main_declaration

subroutine main_assignment()
    use fval_m
    implicit none
    type(fval_t) :: my_data
    my_data = fmap([fval_t :: &
        fentry('assert', fint(1_int64)), &
        fentry('else', fint(1_int64)), &
        fentry('error', fint(1_int64)), &
        fentry('false', fint(1_int64)), &
        fentry('for', fint(1_int64)), &
        fentry('function', fint(1_int64)), &
        fentry('if', fint(1_int64)), &
        fentry('import', fint(1_int64)), &
        fentry('importbin', fint(1_int64)), &
        fentry('importstr', fint(1_int64)), &
        fentry('in', fint(1_int64)), &
        fentry('local', fint(1_int64)), &
        fentry('null', fint(1_int64)), &
        fentry('self', fint(1_int64)), &
        fentry('super', fint(1_int64)), &
        fentry('tailstrict', fint(1_int64)), &
        fentry('then', fint(1_int64)), &
        fentry('true', fint(1_int64)), &
        fentry('ordinary', fint(1_int64)) &
    ])
end subroutine main_assignment

program main
    call main_declaration()
    call main_assignment()
end program main
