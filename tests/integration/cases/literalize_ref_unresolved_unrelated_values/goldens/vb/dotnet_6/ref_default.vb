Imports System.Collections.Generic
Module Check
    Function consume_widget(arg_value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim a = 0
        Dim my_data = New Integer() {
            a,
            1
        }
        consume_widget(my_data)
    End Sub
End Module
