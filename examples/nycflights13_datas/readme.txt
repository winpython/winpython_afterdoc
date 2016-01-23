this file is an extraction of famous R package 'nycflights13' dataset example of Hadley Wickham

https://cran.r-project.org/web/packages/nycflights13

Method (if you have R):
***********************
%%R
install.packages("nycflights13", repos='http://cran.us.r-project.org')

%%R
library(nycflights13)
write.csv(flights, "flights.csv")

