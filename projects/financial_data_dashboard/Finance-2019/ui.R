shinyUI(dashboardPage(
  dashboardHeader(title = 'Financial Data'),
  dashboardSidebar(sidebarMenu(
    menuItem('Stocks', tabName = 'tab1', icon = icon('line-chart')),
    menuItem('Macro', tabName = 'tab2', icon = icon('globe')),
    menuItem("Forex", tabName = "fx", icon = icon("usd", lib = "glyphicon"))
  )),
  dashboardBody(
    tags$head(tags$link(rel = "stylesheet", type = "text/css", href = "style.css")
              #,tags$style(HTML('#button1{background-color:#2b3438; color:#ffffff}'))
              #,tags$script(src = "script.js")
    ),
    tabItems(
      # Stock Tab      
      tabItem(tabName = 'tab1', 
              # Stock Tab - Box 1
              fluidRow(
                box(title = 'Daily Candlestick Chart', status = 'primary', width = 12, collapsible = T, solidHeader = T, column(width = 1, tags$div(class = "div_button", actionButton(inputId = "button1", label = "Go", icon = icon("refresh")))), column(width = 11, textInput("ticker1", label = "Enter Ticker", value = 'nflx')), sliderInput("slider1", label = 'Number of Days (adjust date range with slider below chart)', min = 1, max = 10000, value = 100), plotlyOutput('plotly1'))),
              fluidRow(
                box(title = "Metrics", status = 'primary', width = 12, collapsible = T, solidHeader = T, dataTableOutput("otherMetricsOutput")))
      ),
      
      # GDP Tab
      tabItem(tabName = 'tab2',
              # GDP Tab - Box 1
              fluidRow(box(title = 'GDP', status = 'primary', width = 12, collapsible = T, solidHeader = T, selectInput('aggGDP', label = 'Choose a country', choices = unlist(country.df$country), selected = "United States of America"), plotlyOutput("gdpPlotly"))),
              
              # Bond Yield
              fluidRow(box(title = "US Treasure Bond Yield", status = 'primary', width = 12, collapsible = T, solidHeader = T, checkboxGroupInput("bondInput", label = "Select Bond Yields", choices = names(bond.data)[-1], selected = c("1 YR","2 YR","10 YR"), inline = TRUE), dateRangeInput("bondDateInput", "Date Range (Data go from 1990-01-01 to Present)", start = as.Date("2018-01-01", format = "%Y-%m-%d"), end = as.Date(unlist(bond.data[1,1])), min = as.Date(unlist(bond.data[nrow(bond.data),1])), max = as.Date(unlist(bond.data[1,1])), format = "yyyy-mm-dd", startview = "month", weekstart = 0, language = "en", separator = " to ", width = '50%'), plotlyOutput("bondPlot")))
      ),
      
      # Forex tab
      tabItem(tabName = "fx",
              fluidRow(box(title = "Forex", status = 'success', width = 12, collapsible = T, solidHeader = T, 
                           bootstrapPage(
                             div(class="container",
                                 p(strong(paste0("Current time (", zone, "):")),
                                   textOutput("currentTime")
                                 ),
                                 p(strong("Latest FX Quotes:"),
                                   tableOutput("fxdata"),
                                   checkboxInput("pause", "Pause updates", FALSE))
                             ))
              )))
    ))))