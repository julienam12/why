#### the following demonstrates that the only difference between these is the fact that
####in the quick and dirty one, i fixed the spelling mistakes and something really weird
####is going on in the larger model one for some sentences...

# quick.and.dirty = read.table("whybot-with-pron-res-quick-and-disrty.results", sep="\t", header=T, quote="")
# larger.model = read.table("whybot-with-pron-res-larger-model.results", sep="\t", header=T, quote="")
# quick.and.dirty$sent_with_corefs = as.character(quick.and.dirty$sent_with_corefs)
# larger.model$sent_with_corefs = as.character(larger.model$sent_with_corefs)
# interesting = quick.and.dirty$sent_with_corefs != larger.model$sent_with_corefs
# for (i in 1:sum(interesting)) {
#   print(quick.and.dirty$sent_with_corefs[interesting][i])
#   print(larger.model$sent_with_corefs[interesting][i])
# }

# r = read.table("whybot-explanandum.results", sep="\t", header=T, quote="")
# # seed = "Amy ate a sandwich"
# # seed = "Tom cooked dinner"
# # seed = "Sam repaired his bicycle"
# # seed = "Alex did the dishes"
# # seed = "Meg bought a new computer"
# # seed = "Jack read a book about gardening"
# # seed = "Jane went to the post office"
# # seed = "John went to the store"
# # seed = "Maya drove to work"
# seed_hist = r[r$seed == seed & r$level == 0,]
# ggplot(seed_hist, aes(baby_cavemanese, fill=baby_cavemanese)) +
#   geom_bar(width=.5) +
#   xlab("") +
#   ggtitle(seed) +
#   theme_gray(24)

# r = read.table("whybot-explanandum.results", sep="\t", header=T, quote="")
# # seed = "Amy ate a sandwich"
# # seed = "Tom cooked dinner"
# # seed = "Sam repaired his bicycle"
# # seed = "Alex did the dishes"
# # seed = "Meg bought a new computer"
# # seed = "Jack read a book about gardening"
# # seed = "Jane went to the post office"
# # seed = "John went to the store"
# # seed = "Maya drove to work"
# seed_hist = r[r$seed == seed & r$level == 0,]
# ggplot(seed_hist, aes(baby_cavemanese, fill=baby_cavemanese)) +
#   geom_bar(width=.5) +
#   xlab("") +
#   ggtitle(seed) +
#   theme_gray(24)

r = read.table("whybot-explanandum-take2.results", sep="\t", header=T, quote="")
# r$pred_pairs = paste(r$e_p, r$P)
# good_ones = sapply(r$pred_pairs, function(pair) {
#   table(r$pred_pairs)[pair] > 5
# })
# r = r[good_ones,]
# ggplot(r, aes(pred_pairs, fill=pred_pairs)) +
#   geom_bar(width=.5) +
#   xlab("") +
#   ggtitle("Predicates") +
#   theme_gray(24)

#print(summary(r$tense))
# ggplot(r, aes(tense, fill=tense)) +
#   geom_bar(width=.5) +
#   xlab("") +
#   ggtitle("Tenses") +
#   theme_gray(24)

r$tense.change = sapply(1:nrow(r), function(i) {
  tense = r$tense[i]
  level = r$level[i]
  if (i == 1 || level == 0) {
    return(NA)
  } else {
    past.tense = r$tense[i-1]
    return(tense == past.tense)
  }
})
r.tense = r[!is.na(r$tense.change),]
r.tense$tense.change = factor(r.tense$tense.change, labels=c("Yes", "No"))
ggplot(r.tense, aes(tense.change, fill=tense.change)) +
  geom_bar(width=.5) +
  xlab("") +
  ylab("") +
  ggtitle("Does Tense Change?") +
  theme_gray(24)
ggplot(r.tense, aes(x = tense.change, fill=tense.change)) + 
  geom_bar(width=.5) +#, aes(y = (..count..)/sum(..count..))) + 
  #scale_y_continuous(formatter = 'percent') +
  xlab("") +
  ylab("") +
  ggtitle("Does Tense Change?") +
  theme_gray(24)  + facet_grid(. ~ tense)