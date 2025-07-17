import random
friends = {
    "David": {
        "personality": "Calm",
        "favourite_food": "Anything",
        "hobby": "Playing Football"
    },
    "Joshua": {
        "personality": "outgoing",
        "favourite_food": "Beans",
        "hobby": "Drawing"
    },
    "Grace": {
        "personality": "Thoughtful",
        "favourite_food": "Salt",
        "hobby": "Thinking"
    },
    "Julia": {
        "personality": "Determined",
        "favourite_food": "Bread",
        "hobby": "Swimming"
    },
    "Soala": {
        "personality": "unknown",
        "favourite_food": "Plantian",
        "hobby": "Coding"
    },  
    "Mr.Emma": {
        "personality": "Godly",
        "favourite_food": "Yam",
        "hobby": "Coding"
    }   
}

traits = ["personality", "favourite_food", "hobby"]

score = 0

print("🎯 How well do you know your friends?\n")

for name in friends:
   
    if "" in friends[name].values():
        continue

    print(f"🧠 Quiz for {name}:\n")

    for trait in traits:
        correct_answer = friends[name][trait]

        wrong_answers = []
        for other_name in friends:
            if other_name != name and friends[other_name][trait] != "":
                wrong_answers.append(friends[other_name][trait])

        option1 = random.choice(wrong_answers)
        option2 = random.choice(wrong_answers)
        while option2 == option1:
            option2 = random.choice(wrong_answers)

        all_options = [correct_answer, option1, option2]
        random.shuffle(all_options)

        print(f"👉 What is {name}'s {trait.replace('_', ' ')}?")
        print("1.", all_options[0])
        print("2.", all_options[1])
        print("3.", all_options[2])

        answer = input("Your answer (1/2/3): ")

        if answer in ["1", "2", "3"]:
            picked = all_options[int(answer) - 1]
            if picked == correct_answer:
                print("✅ Correct!\n")
                score += 1
            else:
                print(f"❌ Wrong! The correct answer was '{correct_answer}'.\n")
        else:
            print("⚠️ Invalid input. Moving on...\n")

total_questions = len([f for f in friends if "" not in friends[f].values()]) * len(traits)
print(f"\n🏁 Final Score: {score} out of {total_questions}")

if score == total_questions:
    print("🎉 You’re the ultimate friend expert!")
elif score >= total_questions // 2:
    print("👍 Not bad! You know your friends decently well.")
else:
    print("😅 Oof. Time to schedule some friend catch-ups!")
