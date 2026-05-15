module fval_m
  implicit none
  integer, parameter :: int64 = selected_int_kind(18)
  type :: fval_t
    integer :: t = 0
  end type fval_t
contains
  function fnull() result(v); type(fval_t) :: v; end function
  function fbool(b) result(v); logical, intent(in) :: b; type(fval_t) :: v; end function
  function fint(n) result(v); integer(kind=int64), intent(in) :: n; type(fval_t) :: v; end function
  function freal(x) result(v); real, intent(in) :: x; type(fval_t) :: v; end function
  function fstr(s) result(v); character(len=*), intent(in) :: s; type(fval_t) :: v; end function
  function flist(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fmap(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fset(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fentry(k, u) result(v); character(len=*), intent(in) :: k; type(fval_t), intent(in) :: u; type(fval_t) :: v; end function
end module fval_m
program main
    use fval_m
    implicit none
    type(fval_t) :: my_data
    my_data = fmap([fval_t :: &
        fentry('level1', fmap([fval_t :: fentry('level2', fmap([fval_t :: fentry('level3', fmap([fval_t :: fentry('level4', fmap([fval_t :: fentry('value', fstr('deep')), fentry('items', flist([fval_t :: fstr('a'), fstr('b')]))]))])), fentry('sibling', fint(42_int64))])), fentry('tags', flist([fval_t :: fmap([fval_t :: fentry('name', fstr('tag1')), fentry('meta', fmap([fval_t :: fentry('priority', fint(1_int64)), fentry('labels', flist([fval_t :: fstr('x'), fstr('y')]))]))])]))])) &
    ])
end program main
