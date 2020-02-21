#!/usr/bin/Rscript
library(argparser)

parser <- arg_parser("dataframe for processing")

parser <- add_argument(parser, "dataframe", help="dataframe to process")
parser <- add_argument(parser, "--output", help="Name of output", default="cleaned")

arguments <- parse_args(parser)

a <- arguments$dataframe

a

b <- read.table(a)

b

c <- arguments$output

c

multiply <- function(i) {
  i$multiply <- i[, 1] * i[, 2]
  write.table(i, file="output", quote=FALSE, row.names=FALSE)
}

remove_na <- function(i) {
  cleaned <- na.omit(i)
  write.table(cleaned, file=c, quote=FALSE, row.names=FALSE)
}


remove_na(b)