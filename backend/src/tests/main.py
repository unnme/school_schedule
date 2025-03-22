from random import choice, randint
from typing import List

from faker import Faker
from faker.providers import BaseProvider

from backend.api.depends.repository import subject_repository, teacher_repository
from backend.core.database import session_manager as sm
from backend.entities.subject.schemas import SubjectCreateRequest
from backend.entities.teacher.schemas import TeacherCreateRequest


class RussianPatronymicProvider(BaseProvider):
    def patronymic_male(self):
        patronymics = [
            "Александрович",
            "Алексеевич",
            "Дмитриевич",
            "Иванович",
            "Сергеевич",
            "Павлович",
            "Владимирович",
            "Михайлович",
        ]
        return self.random_element(patronymics)

    def patronymic_female(self):
        patronymics = [
            "Александровна",
            "Алексеевна",
            "Дмитриевна",
            "Ивановна",
            "Сергеевна",
            "Павловна",
            "Владимировна",
            "Михайловна",
        ]
        return self.random_element(patronymics)


class F:
    # TODO: субжекты не могут быть одинаковыми! дабовь проверку!
    subjects = [
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

    fake = Faker("ru_RU")
    fake.add_provider(RussianPatronymicProvider)

    @classmethod
    def _rand_id(cls):
        return randint(1, len(cls.subjects))

    @classmethod
    def _rand_hours(cls):
        return randint(10, 60)

    @classmethod
    async def fake_subjects(cls):
        async for session in sm.get_async_session():
            for subject in cls.subjects:
                request_data = SubjectCreateRequest(name=subject)
                await subject_repository.create(session, request_data)

    @classmethod
    async def _get_list_teachers(cls, count: int) -> List:
        teacher_list = []
        teacher_full_name_set = set()
        while len(teacher_list) < count:
            is_male = choice([True, False])
            first_name = (
                cls.fake.first_name_male() if is_male else cls.fake.first_name_female()
            )
            last_name = (
                cls.fake.last_name_male() if is_male else cls.fake.last_name_female()
            )
            patronymic = (
                cls.fake.patronymic_male() if is_male else cls.fake.patronymic_female()
            )

            full_name = f"{first_name} {last_name} {patronymic}"

            if full_name not in teacher_full_name_set:
                teacher_full_name_set.add(full_name)
                teacher_list.append(
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "patronymic": patronymic,
                    }
                )

        return teacher_list

    @classmethod
    async def fake_teachers(cls, count=5):
        class_list = await cls._get_list_teachers(count)
        for d in class_list:
            async for session in sm.get_async_session():
                request_data = TeacherCreateRequest(
                    first_name=d["first_name"],
                    last_name=d["last_name"],
                    patronymic=d["patronymic"],
                    subjects=[
                        {"id": cls._rand_id(), "teaching_hours": cls._rand_hours()}
                        for _ in range(randint(1, 3)) #BUG: HERE!
                    ],  # pyright: ignore
                )

                await teacher_repository.create(session, request_data)

    @classmethod
    async def fake_student_groups(cls, session):
        pass

    @classmethod
    async def fake_classrooms(cls, session):
        pass

    @classmethod
    async def fake_lessons(cls, session):
        pass

    @classmethod
    async def to_fake(cls):
        await cls.fake_subjects()
        await cls.fake_teachers(count=5)
        # await cls.fake_student_groups(session)
        # await cls.fake_classrooms(session)
        # await cls.fake_lessons(session)
