"""终端聊天入口，直接运行: python chat.py"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app.core import RagService

def main():
    rag = RagService()
    print('RAG 聊天助手已启动')
    print('输入问题后回车，输入 q 退出')
    print('-' * 40)

    while True:
        question = input('你: ').strip()
        if question.lower() == 'q':
            print('再见！')
            break
        if not question:
            continue

        print('AI: ', end='', flush=True)
        try:
            for token in rag.ask_stream(question):
                print(token, end='', flush=True)
        except Exception as e:
            print(f'[ERROR] {e}', end='')
        print()
        print('-' * 40)

if __name__ == '__main__':
    main()
