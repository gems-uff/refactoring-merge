library(arules)

alternativeFunction <-function(){
  print("alternative")
}

project <- read.csv("~/Documents/studying R/project.csv")

projectDisc <- discretizeDF(project, default = list(method = "fixed", breaks = c(-Inf, 6, Inf), 
                                             labels = c("small", "large")))

head(projectDisc)

write.csv(projectDisc, "~/Documents/studying R/project_discretized_R.csv")


#project_discretized <- read.csv("~/Documents/studying R/project_discretized.csv")
rules <- apriori(projectDisc, parameter = list(supp=0.1, conf=0.9, target = "rules", maxtime=10,maxlen=2))
rules_subset <- subset(rules, subset = rhs %pin% "extra=" & lift>1)
inspect(rules_subset)
## non-redundant rules
#inspect(rules_subset[!is.redundant(rules_subset)], by ="lift")








