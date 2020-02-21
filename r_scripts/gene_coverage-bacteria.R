library(tidyverse)

files <- list.files(path='.', pattern='genes.tsv')
files

names <- substring(files, first=14, last=20)
names

names2 <- c('CAP 6', 'AND 5', 'CAP 5', 'AND 6', 'CAP 7', 'AND 7')

df_list <- lapply(files, read.csv, sep='\t', header=FALSE)

df_list_labeled <- list()
count=1
for (i in df_list){
  i$sample <- names2[count]
  df_list_labeled[[count]] <- data.frame(i)
  count <- count+1
}

df <- do.call('rbind', df_list_labeled)
as_tibble(df)


ggplot(df, aes(x=sample, y=V20, col=V12)) +
  geom_jitter(position=position_jitter(width=0.3, height=0), stroke=0.3, size=0.3) +
  scale_y_continuous(limits=c(0, 500), expand=c(0, 0)) +
  scale_color_gradient2(midpoint=0.5, low='#ce0e2d', mid='#ffffff', high='#005cb9') +
  theme_bw() +
  theme(axis.text.x=element_text(angle=90, hjust=1, vjust=0.45)) +
  labs(x='Libraries', y='Mean Coverage Depth', col='%GC')

ggsave('gene_coverage.png', device=png(), dpi=2000, width=20, height=10, units='cm')