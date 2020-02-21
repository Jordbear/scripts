library(tidyverse)

data <- mpg

data$avg <- with(data, (cty+hwy)/2)



data



ggplot(data, aes(x=manufacturer, y=avg, col=manufacturer)) +
  geom_jitter(position=position_jitter(width=0.2, height=0), size=1.5) +
  theme(axis.text.x=element_text(angle=90, hjust=1, vjust=0.3)) +
  theme(legend.position='None') +
  labs(x='Manufacturer', y='Mean MPG') +
  facet_wrap(data$cyl, nrow=1)


aggregate(data$avg, list(data$manufacturer), mean)

