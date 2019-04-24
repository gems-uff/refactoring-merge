library(arules)

project <- read.csv("~/Documents/git/merge-effort-mining/aux/finished-output.csv")
#project_numeric <- project[sapply(project, is.numeric)]

# loop over column *names* instead of actual columns
sapply(names(project), function(cname){
  # (make sure we only plot the numeric columns)
  if (is.numeric(project[[cname]]))
    # use the `main` param to put column name as plot title
    hist(project[[cname]], main=cname, breaks=20)
})
