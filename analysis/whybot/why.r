library(ggplot2)
r = read.table("whybot-no-punctuation.results", sep="\t", header=T)
r$level = as.numeric(r$level) + 1
all_levels = unique(as.character(r$level))
all_seeds = unique(as.character(r$seeds))
r$is_max = sapply(1:nrow(r), function(i) {
  level = r$level[i]
  seed = r$seed[i]
  subject = r$subject[i]
  nrow(r[r$subject == subject & r$seed == seed & r$level > level,]) == 0
})
r_has_response = r[r$explanation != "NO_RESPONSE",]
r_max = r_has_response[r_has_response$is_max,]
#r_max = r_max[r_max$is_max,]
#r_max = r_max[r$explanation != "NO_RESPONSE",]
# r_max = r[r$is_max & (as.character(r$explanation) != "NO_RESPONSE"),]
#graph average max depth
r_mean_max_depth = aggregate(level~seed, data=r_max, FUN=mean)
r_mean_max_depth$seed = factor(r_mean_max_depth$seed, labels=c("Alex", "Amy", "Jack", "Jane", "John", "Maya", "Meg", "Sam", "Tom"))
ggplot(r_mean_max_depth, aes(x=seed, y=level, fill=seed)) +
  geom_bar(width=.5, stat="identity") +
  xlab("") +
  ggtitle("How Many Levels Down The Rabbit Hole...") +
  ylab("Final Depth (out of 5)") +
  theme_gray(24)

r$percent = sapply(1:nrow(r), function(i) {
  level = r$level[i]
  seed = r$seed[i]
  subject = r$subject[i]
  explanation = r$explanation[i]
  if (nrow(r[r$subject == subject & r$seed == seed & r$level > level,]) == 0) {
    if (explanation == "NO_RESPONSE") {
      return((level-1)/5*100)
    } else {
      return(100)
    }
  } else {
    return(NA)
  }
})

r_percent = r[!is.na(r$percent),]
r_mean_percent = aggregate(percent ~ seed, data=r_percent, FUN=mean)
r_mean_percent$seed = factor(r_mean_percent$seed, labels=c("Alex", "Amy", "Jack", "Jane", "John", "Maya", "Meg", "Sam", "Tom"))

ggplot(r_mean_percent, aes(x=seed, y=percent, fill=seed)) +
  geom_bar(width=.5, stat="identity") +
  xlab("") +
  ggtitle("Out of Possible Depth...") +
  ylab("Percent Finished") +
  theme_gray(24)

# r = read.table("whybot-with-cavemanese.results", sep="\t", header=T)
# d = r[r$tel.vs.cause == "cause" | r$tel.vs.cause == "teleological",]
# d = d[!is.na(d$tel.vs.cause),]
# ggplot(d, aes(tel.vs.cause, fill=tel.vs.cause)) +
#   geom_bar(width=.5) +
#   xlab("categorization") +
#   theme_gray(24)
# 
# cc = unlist(sapply(1:nrow(r), function(i) {
#   if (r$explanation[i] != "NO_RESPONSE") {
#     kind = as.character(r$tel.vs.cause[i])
#     if (kind == "cause") {
#       level = r$level[i]
#       if (i != nrow(r)) {
#         nxt.kind = as.character(r$tel.vs.cause[i+1])
#         nxt.level = r$level[i+1]
#         if (!is.na(nxt.kind)) {
#           if (nxt.kind == "cause") {
#             "cause|cause"
#           } else if (nxt.kind == "teleological") {
#             "cause|teleological"
#           } else {
#             NA
#           }
#         } else {
#           NA
#         }
#       } else {
#         NA
#       }
#     } else if (kind == "teleological") {
#       level = r$level[i]
#       if (i != nrow(r)) {
#         nxt.kind = as.character(r$tel.vs.cause[i+1])
#         if (!is.na(nxt.kind)) {
#           nxt.level = r$level[i+1]
#           if (nxt.kind == "cause") {
#             "teleological|cause"
#           } else if (nxt.kind == "teleological") {
#             "teleological|teleological"
#           } else {
#             NA
#           }
#         } else {
#           NA
#         }
#       } else {
#         NA
#       }
#     }
#   } else {
#     NA
#   }
# }))
# 
# cc = data.frame(x=as.factor(cc[!is.na(cc)]))
# ggplot(cc, aes(x, fill=x)) +
#   geom_bar(width=.5) +
#   theme_gray(24)
# # 
# # repeated.obj = sapply(1:nrow(r), function(i) {
# #   if (r$explanation[i] != "NO_RESPONSE") {
# #     obj = as.character(r$obj[i])
# #     if (obj != "") {
# #       level = r$level[i]
# #       subject = as.character(r$subject[i])
# #       if (i != nrow(r)) {
# #         nxt.subj = as.character(r$subj[i+1])
# #         nxt.obj = as.character(r$obj[i+1])
# #         nxt.pobj = as.character(r$pobj[i+1])
# #         nxt.subject = as.character(r$subject[i+1])
# #         nxt.level = r$level[i+1]
# #         if (subject == nxt.subject) {
# #           if (obj %in% c(nxt.subj, nxt.obj, nxt.pobj)) {
# #             1
# #           } else {
# #             0
# #           }
# #         } else {
# #           NA
# #         }
# #       } else {
# #         NA
# #       }
# #     } else {
# #       NA
# #     }
# #   } else {
# #     NA
# #   }
# # })
# # 
# # repeated.pobj = sapply(1:nrow(r), function(i) {
# #   if (r$explanation[i] != "NO_RESPONSE") {
# #     pobj = as.character(r$pobj[i])
# #     if (pobj != "") {
# #       level = r$level[i]
# #       subject = as.character(r$subject[i])
# #       if (i != nrow(r)) {
# #         nxt.subj = as.character(r$subj[i+1])
# #         nxt.obj = as.character(r$obj[i+1])
# #         nxt.pobj = as.character(r$pobj[i+1])
# #         nxt.subject = as.character(r$subject[i+1])
# #         nxt.level = r$level[i+1]
# #         if (subject == nxt.subject) {
# #           if (pobj %in% c(nxt.subj, nxt.obj, nxt.pobj)) {
# #             1
# #           } else {
# #             0
# #           }
# #         } else {
# #           NA
# #         }
# #       } else {
# #         NA
# #       }
# #     } else {
# #       NA
# #     }
# #   } else {
# #     NA
# #   }
# # })
# # 
# # pred.pairs = sapply(1:nrow(r), function(i) {
# #   if (r$explanation[i] != "NO_RESPONSE") {
# #     pred = as.character(r$pred[i])
# #     if (pred != "") {
# #       level = r$level[i]
# #       subject = as.character(r$subject[i])
# #       if (i != nrow(r)) {
# #         nxt.pred = as.character(r$pred[i+1])
# #         nxt.subject = as.character(r$subject[i+1])
# #         nxt.level = r$level[i+1]
# #         if (subject == nxt.subject) {
# #           if (nxt.pred != "") {
# #             paste(pred, nxt.pred)
# #           } else {
# #             NA
# #           }
# #         } else {
# #           NA
# #         }
# #       } else {
# #         NA
# #       }
# #     } else {
# #       NA
# #     }
# #   } else {
# #     NA
# #   }
# # })
# # 
# # s = sum(repeated.subj, na.rm=T) / length(repeated.subj[!is.na(repeated.subj)])
# # o = sum(repeated.obj, na.rm=T) / length(repeated.obj[!is.na(repeated.obj)])
# # p = sum(repeated.pobj, na.rm=T) / length(repeated.pobj[!is.na(repeated.pobj)])
# # 
# # pp=sapply(pred.pairs, function(p) {
# #   if (is.na(p)) {
# #     NA
# #   } else {
# #     if (table(pred.pairs)[p] > 3) {
# #       p
# #     } else {
# #       NA
# #     }
# #   }
# # })
# # pp = pp[!is.na(pp)]
# # df = data.frame(pred.pairs=pp)
# # 
# # ggplot(df, aes(pred.pairs, fill=pred.pairs)) +
# #   geom_bar(width=.5) +
# #   theme_gray(24)
# # 
# # entities = data.frame(part.of.speech=c("subj", "obj", "prep-obj"),
# #                       percent.repetitions=c(s, o, p))
# # 
# # ggplot(entities, aes(x=part.of.speech, y=percent.repetitions, fill=part.of.speech)) +
# #   geom_bar(width=.5, stat="identity") +
# #   theme_gray(30)