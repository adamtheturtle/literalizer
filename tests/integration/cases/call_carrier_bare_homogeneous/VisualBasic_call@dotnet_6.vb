Imports System.Collections.Generic
Module Check
    Function make_widget(first_value As Object, second_value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        make_widget(New Integer() {1}, New Integer() {2})
    End Sub
End Module
