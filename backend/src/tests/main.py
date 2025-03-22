from random import choice, randint
from typing import Dict, List

from faker import Faker
from faker.providers import BaseProvider

from backend.api.depends.repository import subject_repository, teacher_repository
from backend.core.database import session_manager as sm
from backend.entities.student_group.schemas import StudentGroupCreateRequest
from backend.entities.subject.schemas import SubjectCreateRequest
from backend.entities.teacher.schemas import TeacherCreateRequest

TEACHERS_COUNT = 10
fake = Faker("ru_RU")


class RussianPatronymicProvider(BaseProvider):
    patronymics = [
        f"Александров",
        "Алексеев",
        "Дмитриев",
        "Иванов",
        "Сергеев",
        "Павлов",
        "Владимиров",
        "Михайлов",
        "Олегов",
    ]

    def patronymic_male(self):
        return str(self.random_element(self.patronymics) + "ич")

    def patronymic_female(self):
        return str(self.random_element(self.patronymics) + "на")


fake.add_provider(RussianPatronymicProvider)


class F:
    subject_names = [
        "Математика",
        "Физика",
        "Химия",
        "Биология",
        "История",
        "Литература",
        "География",
        "Информатика",
        "Английский язык",
        "Обществознание",
    ]

    @classmethod
    def _rand_subject_id(cls):
        return randint(1, len(cls.subject_names))

    @classmethod
    def _rand_hours(cls):
        return randint(10, 60)

    @classmethod
    def _get_teacher_names(cls, count: int) -> List:
        full_name_list = []
        full_name_set = set()
        while len(full_name_list) < count:
            is_male = choice([True, False])
            first_name = fake.first_name_male() if is_male else fake.first_name_female()
            last_name = fake.last_name_male() if is_male else fake.last_name_female()
            patronymic = fake.patronymic_male() if is_male else fake.patronymic_female()

            full_name = f"{first_name} {last_name} {patronymic}"

            if full_name not in full_name_set:
                full_name_set.add(full_name)
                full_name_list.append(
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "patronymic": patronymic,
                    }
                )

        return full_name_list

    @classmethod
    def _make_teacher_subjects(cls):
        _list = []
        _set = set()
        target_size = randint(1, 3)
        while len(_list) < target_size:
            id = cls._rand_subject_id()
            if id not in _set:
                _set.add(id)
                _list.append({"id": id, "teaching_hours": cls._rand_hours()})

        return _list

    @classmethod
    async def fake_subjects(cls):
        async for session in sm.get_async_session():
            request_data_list = [
                SubjectCreateRequest(name=name) for name in cls.subject_names
            ]
            await subject_repository.create_many(session, request_data_list)

    @classmethod
    async def fake_teachers(cls, count: int):
        async for session in sm.get_async_session():
            teacher_names: List[Dict] = cls._get_teacher_names(count)
            request_data_list = [
                TeacherCreateRequest(
                    first_name=full_name["first_name"],
                    last_name=full_name["last_name"],
                    patronymic=full_name["patronymic"],
                    subjects=cls._make_teacher_subjects(),
                )
                for full_name in teacher_names
            ]

            await teacher_repository.create_many(session, request_data_list)

    # @classmethod
    # async def fake_student_groups(cls, count: int):
    #     async for session in sm.get_async_session():
    #         StudentGroupCreateRequest(
    #             name="",
    #             capacity=33,
    #             subjects=[]
    #
    #         )

    @classmethod
    async def fake_classrooms(cls, session):
        pass

    @classmethod
    async def fake_lessons(cls, session):
        pass

    @classmethod
    async def generate_fake_data(cls):
        await cls.fake_subjects()
        await cls.fake_teachers(count=TEACHERS_COUNT)
        # await cls.fake_student_groups(session)
        # await cls.fake_classrooms(session)
        # await cls.fake_lessons(session)
