def generate_error_rate(liked_test_set, disliked_test_set, results):

    total_correct = 0
    for movie in results:
        movie_title = movie[0]
        if movie[3] > 0:
            if movie[0] in liked_test_set:
                total_correct += 1
        elif movie[3] < 0:
            if movie[0] in disliked_test_set:
                total_correct += 1

    print("Accuracy: " + str(total_correct/(len(liked_test_set) + len(disliked_test_set))))
    return  total_correct/(len(liked_test_set) + len(disliked_test_set))
