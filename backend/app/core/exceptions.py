from fastapi import HTTPException


class BaseAPIException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class SubjectNameExistsException(BaseAPIException):
    def __init__(self, subject_name: str):
        super().__init__(
            status_code=409,
            detail=f"Предмет с названием '{subject_name}' уже существует",
        )


class NotFoundException(BaseAPIException):
    def __init__(self, entity: str, entity_id: int):
        super().__init__(
            status_code=404,
            detail=f"Объект '{entity}' с идентификатором '{entity_id}' не найден",
        )


class DuplicateSubjectException(BaseAPIException):
    def __init__(self, duplicated_ids: list[int]):
        super().__init__(
            status_code=400,
            detail=f"Обнаружены дублирующиеся идентификаторы: {duplicated_ids}",
        )


class DuplicateTeacherException(BaseAPIException):
    def __init__(self, teacher_name: str):
        super().__init__(
            status_code=400, detail=f"Преподаватель '{teacher_name}' уже существует."
        )


class InvalidSubjectIDException(BaseAPIException):
    def __init__(self, missing_ids: list[int]):
        super().__init__(
            status_code=400,
            detail=f"Обнаружены неверные идентификаторы предметов: {missing_ids}",
        )


class DuplicateStudentGroupException(BaseAPIException):
    def __init__(self, student_group_name: str):
        super().__init__(
            status_code=400,
            detail=f"Ученическая группа '{student_group_name}' уже существует.",
        )


class RequestDataMissingException(BaseAPIException):
    def __init__(self):
        super().__init__(status_code=400, detail="Отсутствуют данные запроса")
