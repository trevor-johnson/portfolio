# Stock 

# things I want:
# upcoming comp earnings (quickFS.net, stockrow.com) (earnings calendar)
# maybe a sentiment scrapper on stocktwits?
# earnings charts, w/ next earnings forecast arima model?
# fix metrics data table to say "No info" or something when error for searching VIX or SPY


# Packages
packages <- c("quantmod", "ggplot2", "dplyr", "data.table", "plotly", "Quandl", "shiny", "shinydashboard", "rvest", "DT", "TFX")
sapply(packages, require, character.only = T)
library(Quandl)
library(shinydashboard)
require(TFX)

# setting Quandl api
my_key = readLines("api_key.txt")
Quandl.api_key(my_key)

# candlestick function
tCandleStick <- function(ticker, nrows = 100){
  quantmod::getSymbols(paste0(ticker), src = 'yahoo')
  data <- data.frame(date = index(get(toupper(ticker))), get(toupper(ticker)))
  vals <- c('date', 'open', 'high', 'low', 'close', 'volume', 'adjusted')
  names(data) <- vals
  plotly::plot_ly(tail(data, nrows), x = ~date, type = 'candlestick', open = ~open, close = ~close, high = ~high, low = ~low) %>% layout(title = paste0(ticker, " Candlestick Chart"))
}

# pulling gdp data
#countryCodes <- fread("C:/Users/trev_/Documents/R/cool/countryCodes.csv")

aggGDP <- function(x){
  code <- country.df[country == x,]$code
  b1 <- "MKTGDP"
  b2 <- "A646NWDB"
  full <- paste0(b1, code, b2)
  quantmod::getSymbols(full, src = 'FRED')
  df <- data.frame(date = index(get(full)), gdp = get(full))
  names(df) <- c('date', x)
  df
}


# financials
all.metrics <- function(x){
  # short squeeze
  ur <- c("http://shortsqueeze.com/?symbol=")
  l <- c("&submit=Short+Quote%E2%84%A2")
  shortUrl <- paste0(ur, x, l)
  dd <- rvest::html_text(rvest::html_nodes(xml2::read_html(shortUrl), ".style12 div , tr+ tr .style12+ td"))
  dd2 <- dd[14:41]
  short.df <- data.frame(Metric = dd2[seq(1,28, by = 2)], Value = gsub("\\s", "", dd2[seq(2,28, by = 2)]))
  short.df <- short.df[c(-9,-12,-13,-14),]
  
  # barchart.com
  url <- paste0(c("https://www.barchart.com/stocks/quotes/"), x)
  output.df <- html_text(html_nodes(read_html(url), "#main-content-column li"))
  out <- trimws(output.df)
  out <- strsplit(out, "  ")
  metric <- c()
  value <- c()
  for(i in 1:14){
    metric[i] <- trimws(gsub("K", "", gsub("\\$", "", gsub("\\,", "", out[[i]][1])))) 
    value[i] <- trimws(out[[i]][2])
  }
  value[1] <- paste0(value[1], " K")
  value[2] <- paste0(value[2], " K")
  out.df <- data.frame(Metric = metric, Value = value)
  
  total.df <- rbind(out.df, short.df)
  total.df
  
}


# Forex
Sys.setenv(TZ="America/New_York")
zones <- attr(as.POSIXlt(Sys.time()), "tzone")
zone <- if (zones[[1]] == "") {
  paste(zones[-1], collapse="/")
} else zones[[1]]


# US T Bond
bond.data <- Quandl("USTREASURY/YIELD") %>% data.table()
bond.data.melt <- melt.data.table(bond.data, id.vars = c("Date"))
ggbond.plot <- function(variables = c("10 YR", "1 MO"), begDate = bond.data.melt$Date[length(bond.data.melt$Date)], endDate = bond.data.melt$Date[1]){
  begDate <- as.Date(begDate, "%Y-%m-%d")
  endDate <- as.Date(endDate, "%Y-%m-%d")
  ggbond <- bond.data.melt %>% arrange(desc(Date)) %>% filter(variable %in% variables, Date >= as.numeric(begDate), Date <= as.numeric(endDate))
  p <- ggplot(ggbond, aes(x = Date, y = value, col = factor(variable))) + geom_line() + labs(y = "Yield") + theme_bw() + theme(legend.title=element_blank(), panel.border = element_blank())
  return(ggplotly(p))
}



# Country codes for FRED gdp ----
countries <- c('Afghanistan
               Albania
               Algeria
               Andorra
               Angola
               Antigua and Barbuda
               Argentina
               Armenia
               Aruba
               Australia
               Austria
               Azerbaijan
               Bahamas
               Bahrain
               Bangladesh
               Barbados
               Belarus
               Belgium
               Belize
               Benin
               Bermuda
               Bhutan
               Bolivia
               Bosnia and Herzegovina
               Botswana
               Brazil
               Brunei Darussalam
               Bulgaria
               Burkina Faso
               Burundi
               Cambodia
               Cameroon
               Canada
               Cape Verde
               Cayman Islands
               Central African Republic
               Chad
               Chile
               China
               Hong Kong, SAR China
               Macao, SAR China
               Colombia
               Comoros
               Congo (Brazzaville)
               Congo, (Kinshasa)
               Costa Rica
               Cote d Ivoire
               Croatia
               Cuba
               Cyprus
               Czech Republic
               Denmark
               Djibouti
               Dominica
               Dominican Republic
               Ecuador
               Egypt
               El Salvador
               Equatorial Guinea
               Eritrea
               Estonia
               Ethiopia
               Faroe Islands
               Fiji
               Finland
               France
               French Polynesia
               Gabon
               Gambia
               Georgia
               Germany
               Ghana
               Greece
               Greenland
               Grenada
               Guatemala
               Guinea
               Guinea-Bissau
               Guyana
               Haiti
               Honduras
               Hungary
               Iceland
               India
               Indonesia
               Iran, Islamic Republic of
               Iraq
               Ireland
               Isle of Man
               Israel
               Italy
               Jamaica
               Japan
               Jordan
               Kazakhstan
               Kenya
               Kiribati
               Korea (South)
               Kuwait
               Kyrgyzstan
               Lao PDR
               Latvia
               Lebanon
               Lesotho
               Liberia
               Libya
               Liechtenstein
               Lithuania
               Luxembourg
               Macedonia, Republic of
               Madagascar
               Malawi
               Malaysia
               Maldives
               Mali
               Malta
               Marshall Islands
               Mauritania
               Mauritius
               Mexico
               Micronesia, Federated States of
               Moldova
               Monaco
               Mongolia
               Montenegro
               Morocco
               Mozambique
               Namibia
               Nepal
               Netherlands
               New Caledonia
               New Zealand
               Nicaragua
               Niger
               Nigeria
               Norway
               Oman
               Pakistan
               Palau
               Panama
               Papua New Guinea
               Paraguay
               Peru
               Philippines
               Poland
               Portugal
               Puerto Rico
               Qatar
               Romania
               Russian Federation
               Rwanda
               Saint Kitts and Nevis
               Saint Lucia
               Saint Vincent and Grenadines
               Samoa
               San Marino
               Sao Tome and Principe
               Saudi Arabia
               Senegal
               Serbia
               Seychelles
               Sierra Leone
               Singapore
               Slovakia
               Slovenia
               Solomon Islands
               Somalia
               South Africa
               Spain
               Sri Lanka
               Sudan
               Suriname
               Swaziland
               Sweden
               Switzerland
               Syrian Arab Republic (Syria)
               Tajikistan
               Tanzania, United Republic of
               Thailand
               Timor-Leste
               Togo
               Tonga
               Trinidad and Tobago
               Tunisia
               Turkey
               Turkmenistan
               Tuvalu
               Uganda
               Ukraine
               United Arab Emirates
               United Kingdom
               United States of America
               Uruguay
               Uzbekistan
               Vanuatu
               Venezuela (Bolivarian Republic)
               Viet Nam
               Virgin Islands, US
               Yemen
               Zambia
               Zimbabwe')
countries <- unlist(strsplit(countries, "\n")) %>% trimws()
codes <- c('AF
           AL
           DZ
           AD
           AO
           AG
           AR
           AM
           AW
           AU
           AT
           AZ
           BS
           BH
           BD
           BB
           BY
           BE
           BZ
           BJ
           BM
           BT
           BO
           BA
           BW
           BR
           BN
           BG
           BF
           BI
           KH
           CM
           CA
           CV
           KY
           CF
           TD
           CL
           CN
           HK
           MO
           CO
           KM
           CG
           CD
           CR
           CI
           HR
           CU
           CY
           CZ
           DK
           DJ
           DM
           DO
           EC
           EG
           SV
           GQ
           ER
           EE
           ET
           FO
           FJ
           FI
           FR
           PF
           GA
           GM
           GE
           DE
           GH
           GR
           GL
           GD
           GT
           GN
           GW
           GY
           HT
           HN
           HU
           IS
           IN
           ID
           IR
           IQ
           IE
           IM
           IL
           IT
           JM
           JP
           JO
           KZ
           KE
           KI
           KR
           KW
           KG
           LA
           LV
           LB
           LS
           LR
           LY
           LI
           LT
           LU
           MK
           MG
           MW
           MY
           MV
           ML
           MT
           MH
           MR
           MU
           MX
           FM
           MD
           MC
           MN
           ME
           MA
           MZ
           NA
           NP
           NL
           NC
           NZ
           NI
           NE
           NG
           NO
           OM
           PK
           PW
           PA
           PG
           PY
           PE
           PH
           PL
           PT
           PR
           QA
           RO
           RU
           RW
           KN
           LC
           VC
           WS
           SM
           ST
           SA
           SN
           RS
           SC
           SL
           SG
           SK
           SI
           SB
           SO
           ZA
           ES
           LK
           SD
           SR
           SZ
           SE
           CH
           SY
           TJ
           TZ
           TH
           TL
           TG
           TO
           TT
           TN
           TR
           TM
           TV
           UG
           UA
           AE
           GB
           US
           UY
           UZ
           VU
           VE
           VN
           VI
           YE
           ZM
           ZW')
codes <- strsplit(codes, "\n") %>% unlist() %>% trimws()
country.df <- data.frame(country = countries, code = codes) %>% data.table()
# ----



