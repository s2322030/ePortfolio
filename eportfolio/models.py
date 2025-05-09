class User:
    def __init__(self, id: int = None, username: str = None, password: str = None, role: str = None):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}, role={self.role}>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id and self.username == other.username
        return False


class Subject:
    def __init__(self, teacher_id=None, subjectname=None, subject_id=None, student_id=None, teachername=None):
        self.id = subject_id
        self.teacher_id = teacher_id
        self.subjectname = subjectname
        self.student_id = student_id
        self.teachername = teachername

    def __repr__(self):
        return f"<Subject id={self.id}, subjectname={self.subjectname}>"

    def __eq__(self, other):
        if isinstance(other, Subject):
            return self.id == other.id and self.subjectname == other.subjectname
        return False


class Report:
    def __init__(self, report_code=None, user_id=None, subject_id=None, memo=None, report_id=None):
        self.id = report_id
        self.report_code = report_code
        self.user_id = user_id
        self.subject_id = subject_id
        self.memo = memo

    def __repr__(self):
        return f"<Report id={self.id}, report_code={self.report_code}>"

    def __eq__(self, other):
        if isinstance(other, Report):
            return (self.id == other.id and
                    self.report_code == other.report_code and
                    self.user_id == other.user_id and
                    self.subject_id == other.subject_id and
                    self.memo == other.memo)
        return False