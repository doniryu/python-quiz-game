from game import QuizGame


def main():
    game = QuizGame()

    try:
        while True:
            print("\n=== 반전 상식 퀴즈 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 최고 점수")
            print("5. 종료")

            choice = input("번호를 선택하세요: ").strip()

            if choice == "1":
                game.play()
            elif choice == "2":
                game.add_quiz()
            elif choice == "3":
                game.show_quizzes()
            elif choice == "4":
                game.show_score()
            elif choice == "5":
                print("게임을 종료합니다.")
                break
            else:
                print("1~5 중 하나를 입력해 주세요.")

    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")
    finally:
        game.save_state()


if __name__ == "__main__":
    main()
    