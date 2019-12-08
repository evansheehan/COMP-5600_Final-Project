def generate_error_rate(liked_test_set, disliked_test_set, results):

    guessed_like = 0
    guessed_dislike = 0

    guessed_like_correctly = 0
    guessed_dislike_correctly = 0
    total_correct = 0

    guessed_like_correctly_ratio = 0
    guessed_dislike_correctly_ratio = 0

    for movie in results:
        movie_title = movie[0]
        #if movie[3] > 0 and movie[0] in liked_test_set:
        if movie[3] > 0:
            if movie[0] in liked_test_set:
                guessed_like_correctly += 1
                total_correct += 1
            guessed_like += 1

        #elif movie[3] < 0 and movie[0] in disliked_test_set:
        elif movie[3] < 0:
            if movie[0] in disliked_test_set:
                guessed_dislike_correctly += 1
                total_correct += 1
            guessed_dislike += 1

    # guessed_like_correctly_ratio = guessed_like_correctly/len(liked_test_set)
    # guessed_dislike_correctly_ratio = guessed_dislike_correctly/len(disliked_test_set)

    #Smoothing so we don't divide by 0
    if guessed_like < 1: guessed_like += 1
    if guessed_dislike < 1: guessed_dislike += 1

    guessed_like_correctly_ratio = guessed_like_correctly/guessed_like
    guessed_dislike_correctly_ratio = guessed_dislike_correctly/guessed_dislike
    accuracy = total_correct/(len(liked_test_set) + len(disliked_test_set))
    print("Accuracy: " + str(accuracy))
    return  results, accuracy
