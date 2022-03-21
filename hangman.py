import random
import os


def check_player(player_name, saved_file):
    file = open(saved_file, "r")
    for line in file:
        for word in line.split():
            if word == player_name:
                return True


def messages(lives, many_messages):
    """function for printing a message
     when you lose one life"""
    msg = random.choice(many_messages)
    print("Down to {0} lives, {1}".format(lives, msg))


def hangman(hang, count, letter):
    """putting the letters on the noose
    will probably change"""
    hang[1 + count].pop(-2)
    hang[1 + count].insert(-1, letter)
    return hang


def picker(words):
    """picking the word for each
    round of the game"""
    pick = random.randint(0, len(words) - 1)
    return pick


dif_messages = ("don't worry, you will find it", "come on there is still chance",
                "keep it up and you will get it", "come on, don't give up")
# encouraging messages

words = ("green", "manifesto", "multitouch", "intermediate", "framework",
         "extensive", "foundation", "application", "interface", "distribution",
         "environment", "elements", "exercise", "foundation", "enterprise", "revolution",
         "resolution", "case", "bookshelf", "closet", "bookkeeper", "chance", "evaluation")
# list of words for the game
score = 0
# greet player
# input player name and then greet
player = input("Type your name ")
print("Hello {0}".format(player))

if os.path.isfile("player_stats"):
    save = "player_stats"
    if check_player(player, save):
        print("Welcome back {0}".format(player))
    else:
        print("Here for the first time? Welcome!")
        file = open("player_stats", "a")
        file.write("\n")
        file.write(player)
        file.write(" ")
        file.write(str(score))
        file.close()
else:
    print("First time in this game? Welcome {0}".format(player))
    file = open("player_stats", "w")
    file.write(player)
    file.write(" ")
    file.write(str(score))
    file.close()

game = "Yes"
while game == "Yes":
    print("Lets start!!!")
    hang = [["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", "|", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["/", "/", "/", "/", "/", "/", "/", "/", "/", "/", "/", "/"]]  # primitive hang and noose
    """
    setting the lives to 8 by default, might change
    the counter is useful for the hanging of letters
    """

    counter = 0
    lives = 8
    word = words[picker(words)]
    # word = "green"
    word_list = []  # listing the letters for the word
    word_dash = []
    """
    list of word with dashes
        instead of letters for player
        """

    used_letters = []  # letters already played
    hanger = ""  # used to print joined hang
    dashed = ""  # used to print joined word_dash list
    found = 0
    space_count = 0

    for i in range(len(word)):
        word_dash.append(" _")

    for i in word:
        word_list.append(i)

    for letter in word:
        if letter == " ":
            space_count += 1

    if space_count != 0:
        print("hmm it's a name")
    word_dash.pop(0)
    word_dash.insert(0, word_list[0])
    word_dash.pop(-1)
    word_dash.insert(len(word), word_list[-1])
    word_list[0], word_list[-1] = " _", " _"

    """print(count)
    print(word_list)"""
    for i in range(12):
        print(hanger.join(hang[i]))

    file = open("player_stats", "r+")
    lines = file.readlines()

    for num, line in enumerate(lines):
        if player in line:
            player_line = lines.pop(num)
            for grammh in player_line.split():
                if grammh.isdigit():
                    old_score = int(grammh)
                    print("old_score is {0}".format(old_score))


    while lives > 0:
        print(dashed.join(word_dash))
        # print("You have {0} lives".format(lives))

        letter = input("Try one letter: ")
        while len(letter) > 1 and lives > 0:
            if letter.strip() == word:
                print("won")
                lives = -1
                score += (len(word) * 10)*2
                new_score = str(old_score + score)
                new_save = player + " " + new_score + "\n"
                lines.append(new_save)
            else:
                print("oops choose more than one letters,")
                print("how about trying again.")
                letter = input()

        if lives > 0:
            while letter == "" or letter in used_letters:  # self explanatory
                letter = input("You've played this already, try another: ")

            if letter not in word_list and letter.title() not in word_list:
                lives -= 1
                counter += 1
                messages(lives, dif_messages)
                hangman(hang, counter, letter)
                for i in range(12):
                    print(hanger.join(hang[i]))
                # print(lives)

            for i in word[1:-1]:
                if letter == i.lower():
                    ind = word_list.index(i)
                    word_list.pop(ind)
                    word_list.insert(ind, "-")
                    word_dash.pop(ind)
                    if ind == "":
                        word_dash.insert(ind, i.title())
                    else:
                        word_dash.insert(ind, i)
                    found += 1
                used_letters.append(letter)
            """
            last for: keep index of the found letter
            remove it from word_list, insert '_'
            and put the letter in dashed
            """

            if space_count != 0:
                if found == len(word) - space_count - 2:
                    print("won")
                    print(dashed.join(word_dash))
                    lives = -1
                    score = len(word)*10
                elif lives == 0:
                    print("You did not found the word '{0}', better luck next time!".format(word))
            else:
                if found == len(word) - 2:
                    print("won")
                    print(dashed.join(word_dash))
                    lives = -1
                    score = len(word)*10
                elif lives == 0:
                    print("You did not found the word '{0}', better luck next time!".format(word))

    new_score = str(old_score + score)
    new_save = player + " " + new_score + "\n"
    lines.append(new_save)

    for num, el in enumerate(lines):
        if num == 0:
            file = open("player_stats", "w")
            file.writelines(el)
            file.close()
        else:
            file = open("player_stats", "a")
            file.writelines(el)
            file.close()

    print("Wanna play again?")
    game = input("Press y to continue or n to stop: ").title()
    if game == "Y":
        game = "Yes"
        print("Yes, let's go again")
    elif game == "N":
        game = "No"
    print("\n")
