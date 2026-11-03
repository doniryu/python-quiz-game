import json
import shutil
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

        if score > self.best_score:
            self.best_score = score
            print("새로운 최고 기록입니다!")

        self.save_state()

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

        self.quizzes.append(Quiz(question, choices, int(answer)))
        print("퀴즈가 추가되었습니다!")
        self.save_state()

    def save_state(self):
        path = Path(__file__).resolve().parent / "state.json"
        backup = path.with_name("state.json.bak")
        temp = path.with_name("state.json.tmp")
        backup_temp = path.with_name("state.json.bak.tmp")

        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }

        try:
            with temp.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

            shutil.copyfile(temp, backup_temp)
            temp.replace(path)
            backup_temp.replace(backup)
            print("문제와 점수를 저장하고 백업했습니다.")
        except OSError:
            print("저장 또는 백업에 실패했습니다.")
            print("폴더 권한과 저장 공간을 확인해 주세요.")

    def read_state_file(self, path):
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("잘못된 저장 형식")
        if not isinstance(data.get("quizzes"), list):
            raise ValueError("잘못된 퀴즈 목록")

        quizzes = []
        for item in data["quizzes"]:
            if not isinstance(item, dict):
                raise ValueError("잘못된 문제 형식")

            question = item["question"]
            choices = item["choices"]
            answer = item["answer"]

            if not isinstance(question, str) or not question.strip():
                raise ValueError("빈 문제")
            if not isinstance(choices, list) or len(choices) != 4:
                raise ValueError("보기는 4개 필요")
            if any(
                not isinstance(choice, str) or not choice.strip()
                for choice in choices
            ):
                raise ValueError("잘못된 보기")
            if type(answer) is not int or answer not in range(1, 5):
                raise ValueError("잘못된 정답")

            quizzes.append(Quiz(question, choices, answer))

        best_score = data["best_score"]
        if type(best_score) is not int or best_score < 0:
            raise ValueError("잘못된 점수")

        return quizzes, best_score

    def load_state(self):
        path = Path(__file__).resolve().parent / "state.json"
        backup = path.with_name("state.json.bak")
        errors = (OSError, ValueError, KeyError, TypeError)

        try:
            self.quizzes, self.best_score = self.read_state_file(path)
            print("저장된 문제와 점수를 불러왔습니다.")
            return
        except errors:
            pass

        try:
            self.quizzes, self.best_score = self.read_state_file(backup)
            print("저장 파일이 없거나 손상되어 백업에서 복구했습니다.")
            return
        except errors:
            pass

        self.quizzes = create_default_quizzes()
        self.best_score = 0
        print("사용 가능한 저장 파일이 없어 기본 문제로 시작합니다.")

    def show_score(self):
        if self.best_score == 0:
            print("아직 정답 기록이 없습니다. 퀴즈에 도전해 보세요!")
        else:
            print(f"최고 기록: {self.best_score}문제 정답!")