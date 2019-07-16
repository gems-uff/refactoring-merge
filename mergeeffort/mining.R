library(arules)

project <- read.csv("~/Documents/git/merge-effort-mining/result/output.csv")

#projectDisc <- discretizeDF(project, default = list(method = "fixed", breaks = c(-Inf, 6, Inf), 
#                                             labels = c("small", "large")))


  
  
projectDisc <- discretizeDF(project, methods = list(
  branch1 = list(method = "fixed", breaks = c(0,1,45.5,278.5, 1391.5,10753.5, Inf), 
                 labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  branch2 = list(method = "fixed", breaks = c(0,1,5.5,19.5,60.5, 282.5, Inf), 
                 labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  merge = list(method = "fixed", breaks = c(0,1,120.5,554.5,2282.5,14317.5, Inf), 
               labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_changed_b1 = list(method = "fixed", breaks = c(0,1,3.5,14.5, 52.5, 259.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_changed_b2 = list(method = "fixed", breaks = c(0,1,1.5,2.5, 5.5, 18.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_changed_intersection = list(method = "fixed", breaks = c(0,1,1.5,3.5, Inf), 
                    labels = c("nenhum", "pouco","médio","muito")),
  files_changed_union = list(method = "fixed", breaks = c(0,1,8.5,26.5,79.5,340.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_edited_b1 = list(method = "fixed", breaks = c(0,1,3.5,12.5,42.5,188.5,Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_edited_b2 = list(method = "fixed", breaks = c(0,1,1.5,2.5,4.5,14.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_edited_intersection = list(method = "fixed", breaks = c(0,1,1.5,2.5,3.5,7.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_edited_union = list(method = "fixed", breaks = c(0,1,7.5,21.5,60.5,230.5,Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_add_b1 = list(method = "fixed", breaks = c(0,1,2.5,7.5,23.5,121.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_add_b2 = list(method = "fixed", breaks = c(0,1,1.5,2.5,5.5,22.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_add_intersection = list(method = "fixed", breaks = c(0,1,1.5,2.5,6.5,26.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_add_union = list(method = "fixed", breaks = c(0,1,2.5,7.5, 23.5,110.5,Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_rm_b1 = list(method = "fixed", breaks = c(0,1,1.5,3.5,9.5,41.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  files_rm_b2 = list(method = "fixed", breaks = c(0,1,1.5,8.5, Inf), 
                    labels = c("nenhum", "pouco","médio","muito")),
  files_rm_intersection = list(method = "fixed", breaks = c(0,1,1.5,8.5, Inf), 
                    labels = c("nenhum", "pouco","médio","muito")),
  files_rm_union = list(method = "fixed", breaks = c(0,1,1.5,4.5,15.5,82.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  commits_b1 = list(method = "fixed", breaks = c(0,1,1.5,4.5,14.5,55.5, Inf), 
                        labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  commits_b2 = list(method = "fixed", breaks = c(0,1,1.5,2.5,4.5,14.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  commits_total = list(method = "fixed", breaks = c(0,1,3.5,8.5,22.5,73.5, Inf), 
                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  authors_b1 = list(method = "fixed", breaks = c(0,1,1.5,6.5, Inf), 
                    labels = c("nenhum", "pouco","médio","muito")),
  authors_b2 = list(method = "fixed", breaks = c(0,1,1.5,3.5, Inf), 
                    labels = c("nenhum", "pouco","médio","muito")),
  authors_intersection = list(method = "fixed", breaks = c(0,1,3.5,2.5, Inf), 
                    labels = c("nenhum", "pouco","médio","muito")),
  authors_union = list(method = "fixed", breaks = c(0,1,3.5,10.5, Inf), 
                    labels = c("nenhum", "pouco","médio","muito")),
  committers_b1 = list(method = "fixed", breaks = c(0,1,1.5,5.5,Inf), 
                        labels = c("nenhum", "pouco","médio","muito")),
  committers_b2 = list(method = "fixed", breaks = c(0,1,1.5,3.5, Inf), 
                       labels = c("nenhum", "pouco","médio","muito")),
  committers_intersection = list(method = "fixed", breaks = c(0,1,1.5,2.5, Inf), 
                                 labels = c("nenhum", "pouco","médio","muito")),
  committers_union = list(method = "fixed", breaks = c(0,1,2.5,6.5, Inf), 
                                 labels = c("nenhum", "pouco","médio","muito")),
  lines_changed_b1 = list(method = "fixed", breaks = c(0,1,45.5,276.5,1379.5,10605.5, Inf), 
                                 labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_changed_b2 = list(method = "fixed", breaks = c(0,1,5.5,19.5,60.5,281.5, Inf), 
                                 labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_changed_intersection = list(method = "fixed", breaks = c(0,1,2.5,11.5, Inf), 
                                 labels = c("nenhum", "pouco","médio","muito")),
  lines_changed_union = list(method = "fixed", breaks = c(0,1,119.5,552.5,2295.5,14711.5, Inf), 
                                    labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_add_b1 = list(method = "fixed", breaks = c(0,1,30.5,180.5,894.5,6143.5, Inf), 
                             labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_add_b2 = list(method = "fixed", breaks = c(0,1,3.5,13.5,43.5,193.5, Inf), 
                      labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_add_intersection = list(method = "fixed", breaks = c(0,1,1.5,5.5, Inf), 
                                    labels = c("nenhum", "pouco","médio","muito")),
  lines_add_union = list(method = "fixed", breaks = c(0,1,77.5,351.5,1439.5,8539.5, Inf), 
                      labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_rm_b1 = list(method = "fixed", breaks = c(0,1,12.5,84.5,466.5,3904.5, Inf), 
                         labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_rm_b2 = list(method = "fixed", breaks = c(0,1,1.5,4.5,16.5,97.5, Inf), 
                     labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  lines_rm_intersection = list(method = "fixed", breaks = c(0,1,1.5,9.5, Inf), 
                                labels = c("nenhum", "pouco","médio","muito")),
  lines_rm_union = list(method = "fixed", breaks = c(0,1,31.5,163.5,745.5,5216.5, Inf), 
                     labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  rework = list(method = "fixed", breaks = c(0,1,2.5,13.5, Inf), 
                labels = c("nenhum", "pouco","médio","muito")),
  wasted = list(method = "fixed", breaks = c(0,1,5.5,59.5, Inf), 
                labels = c("nenhum", "pouco","médio","muito")),
  extra = list(method = "fixed", breaks = c(0,1,2.5,10.5, Inf), 
                labels = c("nenhum", "pouco","médio","muito")),
  project_commits = list(method = "fixed", breaks = c(0,1,6756.5,14484.5,25697.5,48966.5, Inf), 
                        labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  merge_commits_count = list(method = "fixed", breaks = c(0,1,1312.5,2986.5,5456.5,10337.5, Inf), 
                         labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  developer_commits_until_merge = list(method = "fixed", breaks = c(0,1,186.5,622.5,1592.5,4320.5, Inf), 
                             labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  developer_merges_until_merge = list(method = "fixed", breaks = c(0,1,48.5,190.5,519.5,1680.5, Inf), 
                                       labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  developer_commits_in_window_of_time = list(method = "fixed", breaks = c(0,1,20.5,51.5,98.5,180.5, Inf), 
                                       labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante")),
  developer_merges_in_window_of_time = list(method = "fixed", breaks = c(0,1,186.5,622.5,1592.5,4320.5, Inf), 
                                       labels = c("nenhum", "muito pouco", "pouco","médio","muito", "bastante"))
  
),
default = list(method = "fixed", breaks = c(-Inf, 6, Inf), 
labels = c("small", "large"))
)

projectDisc$project <- NULL
head(projectDisc)

write.csv(projectDisc, "~/Documents/studying R/project_discretized_R.csv")


#project_discretized <- read.csv("~/Documents/studying R/project_discretized.csv")

#maxtime=0 disables time limit
rules <- apriori(projectDisc, parameter = list(supp=0.01, conf=0.5, target = "rules", maxtime=0,maxlen=2))
#inspect(rules)
rulesLift <- sort(subset(rules, subset = rhs %pin% "wasted=" & lift>1), by="lift") 
inspect(rulesLift)
write.csv(rulesLift, "~/Documents/studying R/positive_lift.csv")

rulesNegativeLift <- sort(subset(rules, subset = rhs %pin% "wasted=" & lift<1), by="lift", decreasing= FALSE) 
inspect(rulesNegativeLift)

write.csv(rulesNegativeLift, "~/Documents/studying R/negative_lift.csv")

#wasted, extra, rework

## non-redundant rules
#inspect(rules_subset[!is.redundant(rules_subset)], by ="lift")








