from questions import create_default_quizzes


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        for quiz in self.quizzes:
            quiz.display()

            while True:
                answer = input("정답 번호를 입력하세요 (1~4): ").strip()

                if answer in ["1", "2", "3", "4"]:
                    break

                print("1~4 중 하나를 입력해 주세요.")

            if quiz.check_answer(int(answer)):
                print("정답입니다!\n")
                score += 1
            else:
                print(f"아쉽네요! 정답은 {quiz.answer}번입니다.\n")

        print(f"결과: {len(self.quizzes)}문제 중 {score}문제 정답!")

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n=== 등록된 퀴즈 목록 ===")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

            