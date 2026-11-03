import json
from pathlib import Path
from quiz import Quiz
from questions import create_default_quizzes


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = 0
        self.load_state()

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

    def add_quiz(self):
        question = input("새 문제를 입력하세요: ").strip()
        while not question:
            print("문제 내용을 입력해 주세요.")
            question = input("새 문제를 입력하세요: ").strip()

        choices = []
        for number in range(1, 5):
            choice = input(f"보기 {number}: ").strip()
            while not choice:
                print("빈 보기 대신 내용을 입력해 주세요.")
                choice = input(f"보기 {number}: ").strip()
            choices.append(choice)

        while True:
            answer = input("정답 번호 (1~4): ").strip()
            if answer in ["1", "2", "3", "4"]:
                break
            print("1~4 중 하나를 입력해 주세요.")

        quiz = Quiz(question, choices, int(answer))
        self.quizzes.append(quiz)
        print("퀴즈가 추가되었습니다!")
        self.save_state()

        import json
        from pathlib import Path

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": getattr(self, "best_score", 0),
        }

        path = Path(__file__).resolve().parent / "state.json"

        try:
            with path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            print("문제와 점수를 저장했습니다.")
        except OSError:
            print("파일을 저장하지 못했습니다. 폴더 권한을 확인해 주세요.")
    def load_state(self):
        path = Path(__file__).resolve().parent / "state.json"

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes = []
            for item in data["quizzes"]:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if not isinstance(question, str) or not question.strip():
                    raise ValueError
                if not isinstance(choices, list) or len(choices) != 4:
                    raise ValueError
                if any(not isinstance(c, str) or not c.strip() for c in choices):
                    raise ValueError
                if type(answer) is not int or answer not in range(1, 5):
                    raise ValueError

                quizzes.append(Quiz(question, choices, answer))

            best_score = data["best_score"]
            if type(best_score) is not int or best_score < 0:
                raise ValueError

            self.quizzes = quizzes
            self.best_score = best_score
            print("저장된 문제와 점수를 불러왔습니다.")

        except FileNotFoundError:
            print("첫 실행입니다. 기본 문제로 시작합니다.")
        except (ValueError, KeyError, TypeError, OSError):
            print("저장 파일을 읽을 수 없어 기본 문제로 시작합니다.")