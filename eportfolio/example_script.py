# example_script.py

from dataaccess import add_subject, search_subjects

# 表示情報を定義
subject_name = "Japanese"
teacher_id = 1  # 例として teacher_id = 1 を指定

# 関数を正しく呼び出して処理を行う
add_subject(subject_name, teacher_id)

# その後で subjects を取得する場合の例
subjects = search_subjects()

# 取得した subjects を表示
print(subjects)

# 実行例:
# python example_script.py

# 出力例:
# [{'id': 1, 'subjectname': 'Japanese', 'teacher_id': 1}]