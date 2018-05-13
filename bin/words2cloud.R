#!/usr/bin/env Rscript

# configure
WORDS = '../tmp/words.tsv'
CLOUD = '../tmp/cloud.png'

# require
library( methods )
library( RColorBrewer )
library( wordcloud )

# frequency
words <- read.table( WORDS, sep = "\t" )
png( filename = CLOUD )
wordcloud( words$V1, words$V2, max.words = 50, random.order=FALSE, rot.per=0.0, colors=brewer.pal(8, "Dark2")  )
