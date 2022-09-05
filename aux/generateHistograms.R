library(arules)

project <- read.csv("~/Documents/git/merge-effort-mining/result/output.csv")
#project_numeric <- project[sapply(project, is.numeric)]

# loop over column *names* instead of actual columns
sapply(names(project), function(cname){
  # (make sure we only plot the numeric columns)
  if (is.numeric(project[[cname]]))
    # use the `main` param to put column name as plot title
    #mean_project = mean(project[[cname]])
    
    # pode ser main = "Equal Frequency",  "Equal Interval length", "K-Means", 
    hist(project[[cname]], main=cname, breaks=10)
    abline(v = mean(project[[cname]]), col="red", lwd=3, lty=2)
})



