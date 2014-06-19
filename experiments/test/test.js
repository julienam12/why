var an_experiment_data_object = {
	"trials": [
	  {
	  	"trial_type": "posterior_predictive",
	  	"response": 0.5,
	  	"rt": 1234,
	  	"color": "red"
	  },
	  {
	  	"trial_type": "posterior_predictive",
	  	"response": 0,
	  	"rt": 1357,
	  	"color": "blue"
	  },
	  {
	  	"trial_type": "truth_judgement",
	  	"response": 1,
	  	"rt": 382,
	  	"color": "red"
	  }
	],
	"check_trials": [
	  {
	  	"actual_color": "red",
	  	"response": "red",
	  	"correct": true,
	  	"rt": 234
	  },
	  {
	  	"actual_color": "blue",
	  	"response": "blue",
	  	"correct": true,
	  	"rt": 234
	  }
	],
	"condition": {
		"proportion_red": 0.5,
		"num_examples": 3
	},
	"subject_information": {
		"age": 44,
		"language": "english",
		"comments": "hi!"
	},
	"system": {
		"os": "linux",
		"browser": "chrome"
	}
}

$("#submit").click(function() {
  setTimeout(function() { turk.submit(an_experiment_data_object) }, 1000);
})