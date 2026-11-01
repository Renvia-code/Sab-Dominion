// Query RESTORATION_CURVE (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "fct_restoration_curve.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"EVENT_KEY", "PEAK_UTC", "PEAK_CUSTOMERS_OUT", "BACKGROUND_CUSTOMERS_OUT", "HOUR_SINCE_PEAK", "CUSTOMERS_OUT", "SHARE_RESTORED"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"EVENT_KEY", type text}, {"PEAK_UTC", type datetime}, {"PEAK_CUSTOMERS_OUT", type number}, {"BACKGROUND_CUSTOMERS_OUT", type number}, {"HOUR_SINCE_PEAK", type number}, {"CUSTOMERS_OUT", type number}, {"SHARE_RESTORED", type number}}, "en-US")
in
    Typed
