// Query FCT_SALES_SECTOR (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "fct_sales_sector.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"YEAR", "CUSTOMER_CLASS", "SALES_MWH", "CUSTOMERS", "REVENUE_USD", "MWH_PER_CUSTOMER", "DELIVERY_ONLY_MWH"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"YEAR", Int64.Type}, {"CUSTOMER_CLASS", type text}, {"SALES_MWH", type number}, {"CUSTOMERS", type number}, {"REVENUE_USD", type number}, {"MWH_PER_CUSTOMER", type number}, {"DELIVERY_ONLY_MWH", type number}}, "en-US")
in
    Typed
