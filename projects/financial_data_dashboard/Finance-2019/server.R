
#source("global.r") 

shinyServer(function(input, output, session) {
  
  # Candlestick chart
  candle.reactive <- eventReactive(input$button1, {
    tCandleStick(input$ticker1, input$slider1)
  })
  output$plotly1 <- renderPlotly({
    candle.reactive()
  })
  
  
  # Financials
  shortDF.reactive <- eventReactive(input$button1, {short.df.fun(input$ticker1)})
  output$shortDfOutput <- renderDataTable({
    shortDF.reactive()
  })
  metrics.reactive <- eventReactive(input$button1, {
    thedf <- all.metrics(input$ticker1)
    cbind(thedf[1:12,], thedf[13:24,])
  })
  output$otherMetricsOutput <- renderDataTable({
    metrics.reactive()
  }, options = list(pageLength = 12))
  
  
  #GDP plot
  output$gdpPlotly <- renderPlotly({
    df <- aggGDP(input$aggGDP)
    plot_ly(data = df, x = ~date, y = ~ get(input$aggGDP), type = 'scatter', mode = 'lines') %>% layout(title = input$aggGDP,  yaxis = list(title = "Annual GDP"))
  })
  
  #T bill plot
  output$bondPlot <- renderPlotly({
    ggbond.plot(variables = input$bondInput, begDate = input$bondDateInput[1], endDate = input$bondDateInput[2])
  })
  
  
  # forex
  output$currentTime <- renderText({
    # Forces invalidation in 1000 milliseconds
    invalidateLater(1000, session)
    as.character(Sys.time())
  })
  
  fetchData <- reactive({
    if (!input$pause)
      invalidateLater(750)
    qtf <- QueryTrueFX()
    qtf$TimeStamp <- as.character(qtf$TimeStamp)
    names(qtf)[6] <- "TimeStamp (GMT)"
    qtf[, c(6, 1:3, 5:4)]
  })
  
  output$fxdata <- renderTable({
    fetchData()
  }, digits=5, row.names=FALSE)
  
})