library(tidyverse)

file <- "E:\\wgs_gene_coverage\\gene-coverage-goodgc.tabular"

df <- read.delim(file, header = FALSE)

df

df$V1 <- factor(df$V1, levels=c(str_c("chr", 1:22), "chrX", "chrY"))

ggplot(df, aes(x=V1, y=V16, col=V8)) +
  geom_jitter(position=position_jitter(width=0.3, height=0), stroke=0.3, size=0.3) +
  scale_y_continuous(limits=c(0, 15), expand=c(0, 0)) +
  scale_color_gradient2(midpoint=0.5, low='#ce0e2d', mid='#ffffff', high='#005cb9') +
  theme_bw() +
  theme(axis.text.x=element_text(angle=90, hjust=1, vjust=0.45)) +
  labs(x='Chromosome', y='Mean Coverage Depth', col='%GC')

ggsave('plot.png', device=png(), dpi=2000, width=20, height=10, units='cm')