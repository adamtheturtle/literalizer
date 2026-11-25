module fval_m
  use, intrinsic :: iso_fortran_env, only: int64, real64
  implicit none
  integer, parameter :: tag_null = 0
  integer, parameter :: tag_bool = 1
  integer, parameter :: tag_int = 2
  integer, parameter :: tag_real = 3
  integer, parameter :: tag_str = 4
  integer, parameter :: tag_list = 5
  integer, parameter :: tag_map = 6
  integer, parameter :: tag_set = 7
  integer, parameter :: tag_entry = 8
  type :: fval_t
    integer :: tag = tag_null
    logical :: bv = .false.
    integer(kind=int64) :: iv = 0_int64
    real(kind=real64) :: rv = 0.0_real64
    character(len=:), pointer :: sv => null()
    type(fval_t), pointer :: items(:) => null()
  end type fval_t
contains
  function jnull() result(v)
    type(fval_t) :: v
    v%tag = tag_null
  end function jnull
  function jbool(b) result(v)
    logical, intent(in) :: b
    type(fval_t) :: v
    v%tag = tag_bool
    v%bv = b
  end function jbool
  function jint(n) result(v)
    integer(kind=int64), intent(in) :: n
    type(fval_t) :: v
    v%tag = tag_int
    v%iv = n
  end function jint
  function jreal(x) result(v)
    real(kind=real64), intent(in) :: x
    type(fval_t) :: v
    v%tag = tag_real
    v%rv = x
  end function jreal
  function jstr(s) result(v)
    character(len=*), intent(in) :: s
    type(fval_t) :: v
    v%tag = tag_str
    allocate(character(len=len(s)) :: v%sv)
    v%sv = s
  end function jstr
  function jlist(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_list
    allocate(v%items(size(a)))
    v%items = a
  end function jlist
  function jmap(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_map
    allocate(v%items(size(a)))
    v%items = a
  end function jmap
  function jset(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_set
    allocate(v%items(size(a)))
    v%items = a
  end function jset
  function jentry(k, u) result(v)
    character(len=*), intent(in) :: k
    type(fval_t), intent(in) :: u
    type(fval_t) :: v
    v%tag = tag_entry
    allocate(character(len=len(k)) :: v%sv)
    v%sv = k
    allocate(v%items(1))
    v%items(1) = u
  end function jentry
end module fval_m
program main
    use fval_m
    implicit none
    type(fval_t) :: my_data
    my_data = jmap([fval_t :: &
        jentry('name', jstr('Alice')), &
        jentry('age', jint(30_int64)), &
        jentry('active', jbool(.true.)), &
        jentry('score', jnull()) &
    ])
end program main
