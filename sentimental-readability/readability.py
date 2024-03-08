from cs50 import get_string


def main():
    text = get_string("Text: ")

    # Calculate the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate L (average number of letters per 100 words) and S (average number of sentences per 100 words)
    L = (letters / words) * 100
    S = (sentences / words) * 100

    # Calculate the Coleman-Liau index
    index = 0.0588 * L - 0.296 * S - 15.8

    # Output the grade level based on the calculated index
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(index)}")


def count_letters(text):
    return sum(c.isalpha() for c in text)


def count_words(text):
    return len(text.split())


def count_sentences(text):
    sentence_endings = [".", "!", "?"]
    return sum(text.count(end) for end in sentence_endings)


if __name__ == "__main__":
    main()
