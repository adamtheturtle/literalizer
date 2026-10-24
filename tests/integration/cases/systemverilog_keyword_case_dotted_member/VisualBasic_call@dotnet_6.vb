Module Check
    Class ThingType_0_
        Public Function Before(value As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim thing As New ThingType_0_()
    Sub _calls()
        thing.Before(1)
    End Sub
End Module
