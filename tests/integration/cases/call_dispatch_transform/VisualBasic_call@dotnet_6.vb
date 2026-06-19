Imports System.Collections.Generic
Module Check
    Function record_value(value As Object) As Object
        Return Nothing
    End Function
    Function flush_buffer(count As Object) As Object
        Return Nothing
    End Function
    Function emit(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(record_value(42))
        flush_buffer(3)
    End Sub
End Module
