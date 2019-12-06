def generate_error_rate(liked_test_set, disliked_test_set, results):
    guessed_like_correctly = 0
    guessed_dislike_correctly = 0
    total_correct = 0

    for movie in results:
        movie_title = movie[0]
        if movie[3] > 0 and movie[0] in liked_test_set:
            guessed_like_correctly += 1
            total_correct += 1
            # movie[4]("Correct!")

        #Something very wrong, this elif statement is NEVER entered
        #Will never guess dislike on a movie and be correct???
        elif movie[3] < 0 and movie[0] in disliked_test_set:
            guessed_dislike_correctly += 1
            total_correct += 1
            # movie[4]("Correct!")

        # movie[4]("Not Correct!")

    guessed_like_correctly_ratio = guessed_like_correctly/len(liked_test_set)
    guessed_dislike_correctly_ratio = guessed_dislike_correctly/len(disliked_test_set)
    accuracy = total_correct/(len(liked_test_set) + len(disliked_test_set))
    print("Accuracy: " + str(accuracy))
    return  results, accuracy
