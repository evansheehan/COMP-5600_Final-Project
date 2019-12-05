import training_and_test_set_generator as generator
import naive_bayes_log as nb_log
import numpy as np
import matplotlib.pyplot as plt

accuracy_results = []
accuracy_results_mean = []

for i in range(50):
    liked_training_ratio, disliked_training_ratio = generator.reset_data()
    accuracy_results.append(nb_log.run_nb_log())
    accuracy_results_mean.append(np.mean(accuracy_results))

plt.plot(accuracy_results)
plt.plot(accuracy_results_mean)
plt.show()
print("Variance is: " + str(np.var(accuracy_results)))
print("debug")