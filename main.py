import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> list[str]:
    matches: list = get_close_matches(user_question, questions, n=3, cutoff=0.6)
    return matches

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    conversation_history: list[tuple[str, str]] = []
    unknown_questions: dict = knowledge_base.get("unknown_questions", {})

    print("Bot: Hello! I'm your friendly chatbot. Ask me anything or type 'quit' to exit.")

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            print("Bot: Goodbye! Have a great day!")
            break
        elif user_input.lower() == 'help':
            print("Bot: You can ask me any question. Type 'history' to see the conversation history. Type 'unknowns' to see frequently asked unknown questions.")
            continue
        elif user_input.lower() == 'history':
            print("Bot: Here is the conversation history:")
            for i, (user_q, bot_a) in enumerate(conversation_history, 1):
                print(f"{i}. You: {user_q} | Bot: {bot_a}")
            continue
        elif user_input.lower() == 'unknowns':
            print("Bot: Here are the frequently asked unknown questions:")
            for question, count in unknown_questions.items():
                print(f"{question} (asked {count} times)")
            continue

        best_matches: list[str] = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_matches:
            if len(best_matches) > 1:
                print("Bot: I found multiple questions that might match. Please choose the best one:")
                for i, match in enumerate(best_matches, 1):
                    print(f"{i}. {match}")
                choice: str = input("Your choice (number): ")
                try:
                    chosen_question = best_matches[int(choice) - 1]
                except (IndexError, ValueError):
                    print("Bot: Invalid choice. Please try again.")
                    continue
            else:
                chosen_question = best_matches[0]

            answer: str = get_answer_for_question(chosen_question, knowledge_base)
            print(f'Bot: {answer}')
            conversation_history.append((user_input, answer))
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer: str = input("Type the answer or 'skip' to skip: ")

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')
            else:
                unknown_questions[user_input] = unknown_questions.get(user_input, 0) + 1

        # Save the unknown questions for future reference
        knowledge_base["unknown_questions"] = unknown_questions
        save_knowledge_base('knowledge_base.json', knowledge_base)

if __name__ == '__main__':
    chat_bot()
