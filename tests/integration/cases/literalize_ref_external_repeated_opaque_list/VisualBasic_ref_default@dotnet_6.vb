Imports System.Collections.Generic
Module Check
    Function consume_widget(arg_value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = New Object() {}
        Dim my_data = New Object() {
            item,
            item
        }
        consume_widget(my_data)
    End Sub
End Module
